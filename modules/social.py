import openai
from pathlib import Path

def generate_dynamic_description(notes_text: str, date: str, video_type: str) -> str:
    """
    Generates a YouTube description using OpenAI based on notes (if available),
    video date, and video type.
    """
    base_prompt = (
        f"Write a fun, engaging YouTube description for a Fortnite {video_type} video "
        f"from {date}. Include light humor, emoticons, a call to subscribe, and relevant hashtags. "
        f"Include reference to the host, Gramps, and his whacky senile playstyle in solo zero build gameplay."
    )

    if notes_text.strip():
        prompt = f"{base_prompt}\n\nAdditional context:\n{notes_text.strip()}"
    else:
        prompt = base_prompt

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )

    return response['choices'][0]['message']['content']

def upload_video(video_path: Path, title: str, description: str, is_vertical: bool):
    """
    Main upload dispatcher:
    - Always uploads to YouTube.
    - Uploads to PeerTube only if the video is NOT vertical.
    """
    print(f"📤 Uploading to YouTube: {video_path.name}")
    yt_url = upload_to_youtube(video_path, title, description, is_short=is_vertical)

    pt_url = None
    if not is_vertical:
        print(f"📤 Uploading to PeerTube: {video_path.name}")
        # Placeholder: Implement actual PeerTube upload function.
        pt_url = upload_to_peertube(video_path, title, description)

    return {
        "youtube": yt_url,
        "peertube": pt_url,
    }
