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
from pathlib import Path   
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from modules.title_utils import generate_montage_title, generate_output_filename
from modules.description_utils import generate_montage_description
from modules.config import DEBUG


def upload_video(file_path: Path, is_vertical: bool, stream_date: str, description: str = None, private: bool = DEBUG) -> str:
    """
    Uploads a video file to YouTube.

    Args:
        file_path (str): Full path to the rendered video file.
        is_vertical (bool): True if video is vertical format (9:16), else widescreen (16:9).
        stream_date (str): Date of the stream in YYYY.MM.DD or YYYY.MM.DD.N format.

    Returns:
        str: URL of the uploaded YouTube video.
    """
    try:
        # Build title I have this:"and description
        file_path = str(file_path)
        session_name = Path(file_path).parents[1].name
        title = generate_montage_title(session_name)
        
        if not description:
            description = str(generate_montage_description())

        # Construct tags and privacy status
        tags = ["Fortnite", "Zero Build", "Solo", "Gramps", "CoolHandGramps"]
        privacy_status = "private" if private else "public"

        # Authenticate
        from authorize_youtube import get_authenticated_service
        youtube = get_authenticated_service()

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

        # media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
        media = MediaFileUpload(str(file_path), chunksize=-1, resumable=True)

        if DEBUG:
            print("🔍 DEBUGGING upload_video")
            print(f"  • file_path: {file_path} ({type(file_path)})")
            print(f"  • is_vertical: {is_vertical}")
            print(f"  • stream_date: {stream_date}")
            print(f"  • private: {private}")
            print(f"  • title: {title}")
            print(f"  • description: {description}")
            print(f"  • tags: {tags}")
            print(f"  • categoryId: {'20'} (should be int or str)")


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

        print(f"✅ Upload complete: https://youtu.be/{response['id']}")
        return f"https://youtu.be/{response['id']}"

    except HttpError as e:
        print(f"❌ YouTube API error: {e}")
        return ""

    except Exception as e:
        print(f"❌ Unexpected error during upload: {e}")
        return ""
