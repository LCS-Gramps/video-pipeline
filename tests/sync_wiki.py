#!/usr/bin/env python3
"""
sync_wiki.py

Synchronizes local markdown files in docs/wiki/ to the GitHub wiki
for the Llama Chile Shop video pipeline project.

Requires the GitHub wiki repo to be cloned into ./video-pipeline.wiki/.

Author: gramps@llamachile.shop
"""

import os
import shutil
import subprocess
from pathlib import Path
print("🧠 THIS IS THE CORRECT sync_wiki.py")

# Correct paths for wiki sync
LOCAL_WIKI_SOURCE = Path("docs/wiki")
LOCAL_WIKI_REPO = Path("video-pipeline.wiki")
print("🔍 Executing: sync_wiki.py from", __file__)

def sync_wiki():
    if not LOCAL_WIKI_REPO.exists():
        print("❌ Wiki repo not found. Clone it using:")
        print("   git clone https://github.com/LCS-Gramps/video-pipeline.wiki.git")
        return

    # Copy .md files to the local wiki repo
    for md_file in LOCAL_WIKI_SOURCE.glob("*.md"):
        target = LOCAL_WIKI_REPO / md_file.name
        shutil.copy2(md_file, target)
        print(f"✅ Synced: {md_file.name}")

    # Commit and push changes
    os.chdir(LOCAL_WIKI_REPO)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "📚 Sync updated wiki pages from docs/wiki"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("🚀 Wiki updated successfully.")

if __name__ == "__main__":
    sync_wiki()
