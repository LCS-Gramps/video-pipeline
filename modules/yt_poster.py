"""
yt_poster.py

Handles video uploads to YouTube using the YouTube Data API.

This module includes logic for setting titles, descriptions, tags, and
privacy status. It integrates with description generation tools and supports
automatic metadata based on the video type (e.g., montage).

Requires authentication via OAuth 2.0 and expects a valid token.pickle file.

Author: Llama Chile Shop
"""

import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from modules.title_utils import generate_montage_title
from modules.description_utils import generate_montage_description
from modules.thumbnail_utils import generate_thumbnail, generate_thumbnail_prompt
from modules.config import DEBUG
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

load_dotenv()


def upload_video(file_path: Path, is_vertical: bool, stream_date: str, description: str = None, private: bool = DEBUG) -> str:
    """
    Uploads a video to YouTube, assigns to playlist, sets recording date, and optionally uploads a thumbnail.

    Args:
        file_path (Path): Full path to the rendered video file.
        is_vertical (bool): True if video is vertical.
        stream_date (str): Stream session date in YYYY.MM.DD[.N] format.
        description (str): Optional description. Generated if None.
        private (bool): If True, uploads as private (used for debug mode).

    Returns:
        str: YouTube video URL.
    """
    try:
        from authorize_youtube import get_authenticated_service
        youtube = get_authenticated_service()

        title = generate_montage_title(stream_date)
        if not description:
            description = generate_montage_description()

        tags = ["Fortnite", "Zero Build", "Solo", "Gramps", "CoolHandGramps"]
        privacy_status = "private" if private else "public"

        # Upload video
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": "20",  # Gaming
            },
            "status": {
                "privacyStatus": privacy_status,
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

        # ✅ Generate thumbnail if widescreen
        if not is_vertical:
            # Load notes.txt if present
            notes_file = file_path.with_name("notes.txt")
            if notes_file.exists():
                with open(notes_file, "r", encoding="utf-8") as f:
                    notes_text = f.read().strip()
            else:
                notes_text = "A funny Fortnite moment with Gramps."

            # Build prompt (future use for AI image generation)
            thumbnail_prompt = generate_thumbnail_prompt(notes_text)
            print(f"🧠 Thumbnail prompt: {thumbnail_prompt}")

            # Generate local thumbnail via ffmpeg
            thumbnail_path = generate_thumbnail(file_path, output_path=f"{file_path.stem}_thumb.jpg")
            if thumbnail_path:
                youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=str(thumbnail_path)
                ).execute()
                print("✅ Custom thumbnail generated and set.")

        # ✅ Add to playlist
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

        # ✅ Set recording date
        parts = stream_date.split(".")
        date_obj = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
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

        return video_url

    except HttpError as e:
        print(f"❌ YouTube API error: {e}")
        return ""

    except Exception as e:
        print(f"❌ Unexpected error during upload: {e}")
        return ""
