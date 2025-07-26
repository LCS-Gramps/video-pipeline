"""
yt_poster.py

Handles video uploads to YouTube using the YouTube Data API.

This module manages:
- Title and description generation
- Playlist assignment
- Custom thumbnail generation (widescreen only)
- Upload record persistence
- Session cleanup on success

Author: Llama Chile Shop
"""

import os
import shutil
from datetime import datetime
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from modules.title_utils import generate_montage_title
from modules.description_utils import generate_montage_description, generate_clip_description
from modules.thumbnail_utils import generate_thumbnail, generate_thumbnail_prompt
from modules.metadata_utils import derive_session_metadata, save_metadata_record
from modules.config import DEBUG

from dotenv import load_dotenv
load_dotenv()

HISTORY_DIR = Path("Z:/LCS/Logs/processed")


def count_existing_uploads(session_date: str) -> int:
    """
    Returns the number of existing metadata records for a given session date.
    Used to compute title suffixes (e.g., "Video 2").
    """
    session_folder = HISTORY_DIR / session_date.replace("-", ".")
    return len(list(session_folder.glob("*.json"))) if session_folder.exists() else 0


def upload_video(file_path: Path, session_dir: Path, is_vertical: bool) -> str:
    """
    Uploads a single video to YouTube, with title/description/thumbnail handling.

    Args:
        file_path (Path): Path to the rendered .mp4 file.
        session_dir (Path): Parent directory of the session (used for metadata).
        is_vertical (bool): Format flag for Shorts logic.

    Returns:
        str: Public YouTube video URL.
    """
    try:
        from authorize_youtube import get_authenticated_service
        youtube = get_authenticated_service()

        # Derive session metadata and isolate the clip record
        session_meta = derive_session_metadata(session_dir)
        session_date = session_meta["session_date"]
        stem = file_path.stem

        clip_record = next(
            (clip for clip in session_meta["clips"] if clip["stem"] == stem),
            None
        )

        if clip_record is None:
            raise RuntimeError(f"Clip {stem} not found in session metadata.")

        metadata = {**session_meta, **clip_record}

        # Title logic with sequential suffixing
        suffix = ""
        existing_count = count_existing_uploads(session_date)
        if existing_count > 0:
            suffix = f"Video {existing_count + 1}"

        title = generate_montage_title(session_date, suffix=suffix)

        # Description
        if metadata["highlight"]:
            description = generate_clip_description(metadata["highlight"])
        else:
            description = generate_montage_description()

        # Upload video
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": metadata.get("tags", []),
                "categoryId": "20",  # Gaming
            },
            "status": {
                "privacyStatus": "private" if DEBUG else "public",
                "selfDeclaredMadeForKids": False,
            }
        }

        print(f"📤 Uploading to YouTube: {file_path.name}")
        media = MediaFileUpload(str(file_path), chunksize=-1, resumable=True)

        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"🟡 Uploading: {int(status.progress() * 100)}%")

        video_id = response["id"]
        video_url = f"https://youtu.be/{video_id}"
        print(f"✅ Upload complete: {video_url}")

        # Upload thumbnail if wide
        if not is_vertical:
            notes = metadata.get("notes", {})
            prompt = generate_thumbnail_prompt(notes.get("highlight", "Fortnite moment"))
            thumbnail_path = generate_thumbnail(file_path, output_path=f"{file_path.stem}_thumb.jpg")
            if thumbnail_path:
                youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=str(thumbnail_path)
                ).execute()
                print("✅ Custom thumbnail uploaded.")

        # Add to playlist
        playlist_id = os.getenv("YT_PLAYLIST_ID_SHORTS" if is_vertical else "YT_PLAYLIST_ID_CLIPS")
        if playlist_id:
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            ).execute()
            print(f"✅ Added to playlist: {playlist_id}")

        # Set recording date
        date_obj = datetime.strptime(session_date, "%Y-%m-%d")
        recording_date = date_obj.strftime("%Y-%m-%dT00:00:00Z")
        youtube.videos().update(
            part="recordingDetails",
            body={
                "id": video_id,
                "recordingDetails": {
                    "recordingDate": recording_date
                }
            }
        ).execute()
        print(f"✅ Recording date set: {recording_date}")

        # Save metadata (include YouTube URL)
        metadata["youtube_urls"] = [video_url]
        save_metadata_record(metadata)

        # Clean up session directory if DEBUG is off
        if not DEBUG:
            try:
                shutil.rmtree(session_dir)
                print(f"🧹 Cleaned up source directory: {session_dir}")
            except Exception as e:
                print(f"⚠️ Cleanup failed: {e}")

        return video_url

    except HttpError as e:
        print(f"❌ YouTube API error: {e}")
        return ""

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return ""
