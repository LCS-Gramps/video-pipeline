import os
import pickle, logging
from pathlib import Path
from datetime import datetime

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from modules.title_utils import get_output_filename, generate_montage_title

# Define OAuth scopes and token paths
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_PATH = Path("token.pickle")
CLIENT_SECRETS_FILE = Path("client_secrets.json")

def authenticate_youtube():
    """Handles YouTube OAuth flow and returns a service client."""
    creds = None

    if TOKEN_PATH.exists():
        with open(TOKEN_PATH, "rb") as token_file:
            creds = pickle.load(token_file)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRETS_FILE.exists():
                raise FileNotFoundError("client_secrets.json not found.")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRETS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "wb") as token_file:
            pickle.dump(creds, token_file)

    return build("youtube", "v3", credentials=creds)

def generate_description(clip_path: Path, stream_date: datetime, is_montage: bool = False) -> str:
    """Creates a dynamic and fun YouTube description."""
    kill_count_guess = sum(word.isdigit() for word in clip_path.stem.split())
    date_str = stream_date.strftime("%B %d, %Y")

    intro = "Gramps is back in Fortnite with another spicy highlight! 🦥"
    if is_montage:
        body = (
            f"This reel features an outrageous compilation of top plays from our {date_str} stream.\n"
            f"{kill_count_guess} eliminations of stupendous magnitude that must be seen to be believed!"
        )
    else:
        body = (
            f"Recorded live on {date_str}, this clip captures one of many wild moments "
            "from the battlefield. Grab your popcorn. 🎮"
        )

    hashtags = "#Fortnite #Gaming #SeniorGamer #LlamaChileShop #EpicMoments"

    return f"{intro}\n\n{body}\n\nSubscribe for more: https://youtube.com/@llamachileshop\n{hashtags}"

def upload_to_youtube(video_path: Path, title: str, description: str, is_short: bool = False) -> str:
    """Uploads the video to YouTube and returns the video URL."""
    youtube = authenticate_youtube()

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": ["Fortnite", "Gaming", "Senior Gamer", "LlamaChileShop"],
            "categoryId": "20",  # Gaming
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False,
        }
    }

    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()
    video_id = response["id"]
    return f"https://youtu.be/{video_id}"
