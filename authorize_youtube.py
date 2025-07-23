import os
import sys

# Automatically locate this file's directory (e.g., \\chong\LCS\Videos\eklipse)
project_root = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(project_root, "modules")

# Add modules directory to the Python path
sys.path.insert(0, modules_dir)

# Change working directory so relative paths (like client_secrets.json) resolve
os.chdir(modules_dir)

# Import from yt_poster in modules
from yt_poster import authenticate_youtube

# Run the OAuth flow
print("🔐 Starting YouTube OAuth authorization...")


try:
    service = authenticate_youtube()
    print("✅ YouTube authorization complete.")
except Exception as e:
    print(f"❌ Authorization failed: {e}")
