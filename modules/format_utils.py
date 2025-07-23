import os

def detect_format_from_filename(clip_path):
    """
    Determines if a clip is 'wide' or 'vertical' based on its filename.

    Rules:
    - Filenames ending in -vert.mp4 or -vertical.mp4 → 'vertical'
    - All others → 'wide'
    """
    filename = os.path.basename(clip_path).lower()
    if filename.endswith("-vert.mp4") or filename.endswith("-vertical.mp4"):
        return "vertical"
    return "wide"

