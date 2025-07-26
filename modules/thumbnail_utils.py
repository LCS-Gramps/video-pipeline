import subprocess
import os
from pathlib import Path

def generate_thumbnail(video_path: str, output_path: str) -> str:
    """
    Generate a thumbnail image from the midpoint of the given video.

    Parameters:
        video_path (str): Path to the input video file.
        output_path (str): Path where the thumbnail image (JPEG) should be saved.

    Returns:
        str: Path to the generated thumbnail image.

    Notes:
    - Uses FFmpeg to extract a frame using the 'thumbnail' filter.
    - Thumbnail will be scaled to 1280x720 resolution (16:9).
    - Overwrites the output file if it already exists.
    """
    video_path = Path(video_path)
    output_path = Path(output_path)

    if not video_path.exists():
        raise FileNotFoundError(f"Video file not found: {video_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg", "-y",  # Overwrite output if exists
        "-i", str(video_path),
        "-vf", "thumbnail,scale=1280:720",
        "-frames:v", "1",
        str(output_path)
    ]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to generate thumbnail: {e}") from e

    if not output_path.exists():
        raise RuntimeError(f"Thumbnail was not created: {output_path}")

    return str(output_path)


def generate_thumbnail_prompt(notes: str) -> str:
    """
    Generate a rich thumbnail prompt from a descriptive sentence.

    Args:
        notes (str): A brief sentence describing the video content.

    Returns:
        str: A thumbnail generation prompt for OpenAI or DALL·E.
    """
    return (
        f"Create a Fortnite-style gaming thumbnail based on the moment: \"{notes.strip()}\" "
        f"featuring a stylized llama character with bold comic-style colors. Include dramatic or humorous elements "
        f"(e.g., explosions, dance emotes, intense lighting), and text like 'HIGHLIGHT' or 'VICTORY ROYALE'. "
        f"Use the Llama Chile Shop color palette (f7338f, 10abba, 1c0c38). The vibe should be fun, exaggerated, "
        f"and chill — inviting viewers to laugh and enjoy the moment."
    )
