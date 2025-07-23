from pathlib import Path
from datetime import datetime
from modules.yt_poster import upload_to_youtube, generate_description

# Manually define the clip path and its stream folder
clip_path = Path("//chong/LCS/Videos/eklipse/2025.06.20/rendered/AI_Compilation___19x_kills,_downs-vert.mp4")
stream_folder = clip_path.parent.parent  # Goes up to 2025.06.20

# Extract stream date from folder name
stream_date = datetime.strptime(stream_folder.name, "%Y.%m.%d")

# Determine if vertical format
is_vert = clip_path.stem.endswith("-vert") or clip_path.stem.endswith("-vertical")

# Generate YouTube description
description = generate_description(
    clip_path=clip_path,
    stream_date=stream_date,
    is_montage=True
)

# Upload to YouTube
youtube_url = upload_to_youtube(
    video_path=clip_path,
    title=clip_path.stem,
    description=description,
    is_short=is_vert
)

# Print social previews
print("🔗 Uploaded to YouTube:", youtube_url)

print("\n--- Mastodon Preview ---")
print(f"New video posted! {clip_path.stem} — now live on YouTube! {youtube_url} 🦙\n\n{description}")

print("\n--- Bluesky Preview ---")
print(f"Catch the latest from Gramps 🦙: {clip_path.stem} — now up on YouTube!\n\n{youtube_url} #Fortnite #LlamaChileShop")
