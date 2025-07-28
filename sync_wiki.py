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

# Paths
LOCAL_WIKI_SOURCE = Path("docs/wiki")                  # Where local .md pages are stored
LOCAL_WIKI_REPO = Path("video-pipeline.wiki")          # Where the GitHub wiki repo is cloned

def sync_wiki():
    """
    Copies markdown files from the local wiki source into the cloned wiki repo
    and pushes the changes to GitHub.
    """
    if not LOCAL_WIKI_REPO.exists():
        print("❌ Wiki repo not found. Clone it using:")
        print("   git clone https://github.com/LCS-Gramps/video-pipeline.wiki.git")
        return

    print("📄 Syncing wiki markdown files...")
    for md_file in LOCAL_WIKI_SOURCE.glob("*.md"):
        target = LOCAL_WIKI_REPO / md_file.name
        shutil.copy2(md_file, target)
        print(f"✅ Synced: {md_file.name}")

    # Change directory to the cloned wiki repo for Git operations
    os.chdir(LOCAL_WIKI_REPO)

    try:
        print("📚 Committing changes...")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "📚 Sync updated wiki pages from docs/wiki"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Wiki updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")
        print("💡 Tip: You may need to mark the repo as safe:")
        print("    git config --global --add safe.directory '//chong/LCS/Videos/eklipse/video-pipeline.wiki'")

if __name__ == "__main__":
    sync_wiki()
