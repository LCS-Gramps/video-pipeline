#!/usr/bin/env python3
"""
yt_poster.py

This module handles the upload of videos to YouTube using the YouTube Data API v3.
It supports setting metadata such as title, description, tags, category, and privacy settings.
It also ensures that the game title "Fortnite" is included in the metadata to trigger proper categorization.

Author: gramps@llamachile.shop
"""

import os
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from modules.config import OPENAI_API_KEY, DEBUG
from modules.archive import save_metadata_record

# Category ID for "Gaming" on YouTube (required for accurate categorization)
CATEGORY_ID = "20"

# Default tags to include if none are provided
DEFAULT_TAGS = [
    "Fortnite", "Zero Build", "Gramps", "CoolHandGramps",
    "funny", "gaming", "highlights"
]

# Default visibility setting
DEFAULT_PRIVACY = "public"

def ensure_fortnite_tag(metadata):
    """
    Ensures that the word 'Fortnite' appears in at least one of the following:
    - Title
    - Description
    - Tags list

    This helps YouTube automatically detect the game and associate the video
    with Fortnite gameplay.
    """
    if "fortnite" not in metadata["title"].lower() and \
       "fortnite" not in metadata["description"].lower() and \
       not any("fortnite" in tag.lower() for tag in metadata.get("tags", [])):
        metadata.setdefault("tags", []).append("Fortnite")

def upload_video(youtube, video_path, metadata):
    """
    Uploads a video to YouTube with the provided metadata.

    Args:
        youtube: Authenticated YouTube API service object.
        video_path: Path to the video file to be uploaded.
        metadata: Dictionary containing video metadata fields.

    Returns:
        str: URL of the uploaded YouTube video.
    """

    # Ensure the 'Fortnite' keyword is present somewhere in metadata
    ensure_fortnite_tag(metadata)

    # Construct the request body for YouTube API
    request_body = {
        "snippet": {
            "title": metadata["title"],
            "description": metadata["description"],
            "tags": metadata.get("tags", DEFAULT_TAGS),
            "categoryId": CATEGORY_ID  # Set to "Gaming"
        },
        "status": {
            "privacyStatus": metadata.get("privacy", DEFAULT_PRIVACY)
        }
    }

    # Wrap the video file in a MediaFileUpload object
    media = MediaFileUpload(video_path, mimetype="video/*", resumable=True)

    print(f"📤 Uploading {video_path} to YouTube...")

    # Execute the video insert request
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()
    video_id = response["id"]
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    print(f"✅ Uploaded to YouTube: {youtube_url}")

    # Record the YouTube URL in the metadata for archive history
    metadata.setdefault("youtube_url", []).append(youtube_url)

    # Persist the metadata archive only if we're not in DEBUG mode
    if not DEBUG:
        save_metadata_record(video_path, metadata)

    return youtube_url

def get_authenticated_service():
    """
    Returns an authenticated YouTube API service using Application Default Credentials.
    This requires that `gcloud auth application-default login` has been run successfully,
    or that a service account token is available in the environment.

    Returns:
        googleapiclient.discovery.Resource: The YouTube API client object.
    """
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
    return build("youtube", "v3", credentials=credentials)
