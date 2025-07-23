from pathlib import Path
import subprocess
from datetime import datetime


def parse_stream_date(clip_path: Path) -> datetime:
    """
    Extracts the stream date from a montage clip path by parsing its grandparent directory name.
    Assumes format: YYYY.MM.DD or YYYY.MM.DD.N
    """
    parent_dir = clip_path.parents[1]
    dir_name = parent_dir.name.split(".")
    if len(dir_name) < 3:
        raise ValueError(f"Invalid directory name format: {parent_dir.name}")
    year, month, day = map(int, dir_name[:3])
    return datetime(year, month, day)


def extract_session_metadata(clip_path: Path) -> str:
    """
    Returns the session directory name as metadata tag (e.g. '2025.07.01' or '2025.07.01.2')
    """
    return clip_path.parents[1].name


def generate_output_filename(clip_path: Path) -> str:
    """
    Generates output filename from the session name, following rules:
    - Vertical clips get suffix `-vert`
    - Suffix .N in session becomes `-videoN`
    """
    session_name = extract_session_metadata(clip_path)
    date_parts = session_name.split(".")
    base_date = "".join(date_parts[:3])  # e.g., 20250701
    suffix = f"-video{date_parts[3]}" if len(date_parts) > 3 else ""
    vert = "-vert" if clip_path.stem.endswith(("-vert", "-vertical")) else ""
    return f"Fortnite-montage-{base_date}{suffix}{vert}.mp4"


def format_overlay_text(title: str, subtitle: str, date_str: str) -> list[str]:
    """
    Returns three lines for the overlay text.
    """
    return [title, subtitle, date_str]


def generate_title_overlay(
    intro_path: Path,
    overlay_text: list[str],
    output_path: Path,
    font_path: Path,
    is_vertical: bool = False,
):
    """
    Overlays title text on top of the intro clip and creates a new video segment.
    The text fades out completely 0.5 seconds before the intro ends.
    """
    width, height = (1080, 1920) if is_vertical else (1920, 1080)
    fade_start = 4.5
    fade_duration = 0.5

    # Uniform visual settings
    fontcolor = "#f7338f"
    shadowcolor = "0x1c0c38"
    boxcolor = "0x10abba@0.5"
    fontsize = 64
    y_offsets = [0, 80, 160]  # vertical positions for each line

    # Escape Windows-style font path
    escaped_font_path = str(font_path).replace("\\", "\\\\")

    drawtext_filters = []
    for i, (line, y_offset) in enumerate(zip(overlay_text, y_offsets)):
        drawtext = (
            f"drawtext=text='{line}':"
            f"fontfile='{escaped_font_path}':"
            f"x=(w-text_w)/2:"
            f"y=(h/2)-90+{y_offset}:"
            f"fontsize={fontsize}:"
            f"fontcolor={fontcolor}:"
            f"shadowcolor={shadowcolor}:"
            f"shadowx=2:shadowy=2:"
            f"box=1:boxcolor={boxcolor}"
        )
        drawtext_filters.append(drawtext)

    drawtext_filters.append(f"fade=t=out:st={fade_start}:d={fade_duration}:alpha=1")
    drawtext_filter = ",".join(drawtext_filters)

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i", str(intro_path),
        "-vf", drawtext_filter,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-t", "5",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ]

    subprocess.run(ffmpeg_cmd, check=True)


def generate_montage_title(session_name: str) -> str:
    """
    Generates YouTube/PeerTube title for montage videos.
    Example:
    '#Fortnite #Solo #Zerobuild #Highlights with Gramps from July 1, 2025'
    """
    parts = session_name.split(".")
    year, month, day = map(int, parts[:3])
    suffix = f" Video {parts[3]}" if len(parts) > 3 else ""
    date_str = datetime(year, month, day).strftime("%B %-d, %Y")
    return f"#Fortnite #Solo #Zerobuild #Highlights with Gramps from {date_str}{suffix}"
