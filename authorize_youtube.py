"""
authorize_youtube.py

Handles OAuth2 authorization for the YouTube Data API.

This module loads the client_secrets.json file and generates an authorized
YouTube API service object for use by other modules. The token is cached
in token.pickle to avoid repeated authorization.

Author: gramps@llamachile.shop
"""

import os
import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes define what access is requested from the YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Default token and client secret filenames
TOKEN_PATH = "token.pickle"
CLIENT_SECRET_FILE = "client_secrets.json"


def get_authenticated_service():
    """
    Returns an authorized YouTube API client.

    If the token does not exist or is expired, initiates the OAuth flow.
    Requires client_secrets.json in project root.

    Returns:
        googleapiclient.discovery.Resource: Authenticated YouTube service
    """
    creds = None

    # Check if token.pickle exists
    if Path(TOKEN_PATH).exists():
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    # If no valid creds, go through OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("🔐 Starting YouTube OAuth authorization...")
            if not Path(CLIENT_SECRET_FILE).exists():
                raise FileNotFoundError(f"Missing required file: {CLIENT_SECRET_FILE}")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)
