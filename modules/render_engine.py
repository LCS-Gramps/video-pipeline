import subprocess
from pathlib import Path
from modules.config import DEBUG

def render_montage_clip(
    title_card_path: Path,
    montage_path: Path,
    output_path: Path,
    intro_path: Path,
    outro_path: Path,
    music_path: Path,
    is_vertical: bool = False,
):
    """
    Combines intro (with title), montage, and outro into a final video.
    Uses ffmpeg for concatenation and audio overlay.
    """

    if not title_card_path.exists():
        raise FileNotFoundError(f"[ERROR] Title card not found: {title_card_path}")
    if not montage_path.exists():
        raise FileNotFoundError(f"[ERROR] Montage clip not found: {montage_path}")
    if not intro_path.exists():
        raise FileNotFoundError(f"[ERROR] Intro file not found: {intro_path}")
    if not outro_path.exists():
        raise FileNotFoundError(f"[ERROR] Outro file not found: {outro_path}")
    if not music_path.exists():
        raise FileNotFoundError(f"[ERROR] Music track not found: {music_path}")

    filter_complex = (
        "[0:v:0]fps=30,setsar=1[v0];"
        "[1:v:0]fps=30,setsar=1[v1];"
        "[1:a:0]anull[a1];"
        "[3:v:0]fps=30,setsar=1[v3];"
        "[v0][v1][v3]concat=n=3:v=1:a=0[outv];"
        "[a1][2:a:0]amix=inputs=2:duration=first[outa]"
    )

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i", str(title_card_path),   # 0 = intro with title baked in
        "-i", str(montage_path),      # 1 = montage content
        "-i", str(music_path),        # 2 = background music
        "-i", str(outro_path),        # 3 = static outro
        "-filter_complex", filter_complex,
        "-map", "[outv]",
        "-map", "[outa]",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "192k",
        str(output_path)
    ]

    if DEBUG:
        print(f"[DEBUG] Starting render_montage_clip")
        print(f"[DEBUG] Input files:")
        print(f"  title_card_path:   {title_card_path} → {title_card_path.exists()}")
        print(f"  montage_path:      {montage_path} → {montage_path.exists()}")
        print(f"  output_path:       {output_path}")
        print(f"  output_dir exists? {output_path.parent.exists()}")
        print(f"[DEBUG] subprocess command: {ffmpeg_cmd}")

    subprocess.run(ffmpeg_cmd, check=True)
