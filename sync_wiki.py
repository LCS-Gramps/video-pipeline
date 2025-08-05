# sync_wiki.py
"""
🚨 DEPRECATED: This script was used to manually sync wiki pages via local `.md` files.
It is now kept as a fallback ('parachute') in case automated token-based publishing fails.

✅ DO NOT use this unless instructed.
"""

# This entire file is now considered inactive and will not be maintained unless token publishing breaks.
# All real wiki publishing is handled via automated memory-based GPT-side tools.

import os
import subprocess
import requests
from datetime import datetime

WIKI_DIR = "video-pipeline.wiki"
LOG_FILE = "logs/wiki_publish.log"
GITHUB_REPO = "LCS-Gramps/video-pipeline"
WIKI_BASE_URL = f"https://github.com/{GITHUB_REPO}/wiki"

def log_result(filename, success):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        status = "✅" if success else "❌"
        timestamp = datetime.now().isoformat(timespec='seconds')
        log.write(f"{timestamp} {status} {filename}\n")

def commit_and_push():
    # Explicitly list and add all .md files
    md_files = [f for f in os.listdir(WIKI_DIR) if f.endswith(".md")]
    if not md_files:
        print("⚠️ No markdown files found to commit.")
        return

    try:
        for f in md_files:
            subprocess.run(["git", "add", f], cwd=WIKI_DIR, check=True)
        
        result = subprocess.run(
            ["git", "commit", "-m", "📚 Sync updated wiki pages from docs/wiki"],
            cwd=WIKI_DIR,
            capture_output=True,
            text=True
        )
        
        if "nothing to commit" in result.stdout.lower():
            print("⚠️ Nothing to commit.")
            return
        print(result.stdout.strip())

    except subprocess.CalledProcessError as e:
        print("❌ Git add/commit failed:", e)
        return

    subprocess.run(["git", "push", "origin", "master"], cwd=WIKI_DIR, check=True)


def verify_publish():
    for file in os.listdir(WIKI_DIR):
        if file.endswith(".md"):
            name = file.replace(".md", "").replace(" ", "-")
            url = f"{WIKI_BASE_URL}/{name}"
            try:
                response = requests.get(url)
                success = response.status_code == 200
            except Exception:
                success = False
            log_result(file, success)
            print(f"{'✅' if success else '❌'} {url}")

def main():
    print("📝 Auto-generating wiki content...")
    os.makedirs(WIKI_DIR, exist_ok=True)

    autogen_content = {
        "Architecture-Overview.md": """# Architecture Overview

This page provides an overview of the internal structure of the LCS Pipeline.

## Modules
- `main.py`: Central orchestration logic
- `modules/`: Reusable utilities for title cards, thumbnails, uploads
- `assets/`: Contains branding videos and fonts

## Flow
1. Detect new video sessions
2. Generate metadata, titles, overlays
3. Render videos with intro/title/outro
4. Upload to YouTube and optionally PeerTube
5. Auto-publish wiki and social metadata
"""
    }

    # Only create or update files explicitly listed
    for filename, content in autogen_content.items():
        filepath = os.path.join(WIKI_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content.strip())
        print(f"✅ Created or updated {filename}")

    commit_and_push()
    verify_publish()

if __name__ == "__main__":
    main()
