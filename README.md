# 🎬 LCS Pipeline

**Automated livestream highlight rendering and publishing for Fortnite content featuring Gramps.**

This project powers the backend of [Llama Chile Shop](https://www.youtube.com/@llamachileshop), transforming raw livestream clips into polished, uploaded videos — complete with titles, thumbnails, intros/outros, and social metadata.

---

## ⚙️ Features

* ✅ Daily folder scan for new stream sessions
* 🎬 Clip classification (`hits/`, `misses/`, `montages/`, etc.)
* 🧠 AI-generated titles and descriptions via OpenAI
* 🪄 Auto-stitched intro + title card + outro
* 🖼️ Dynamic thumbnail creation with Fortnite styling
* ⬆️ Uploads to YouTube (and PeerTube if enabled)
* 🧾 Metadata archive and session history
* 🐘 (Planned) Social posts to Mastodon and Bluesky

---

## 🚀 Quick Start

```bash
git clone https://github.com/LCS-Gramps/video-pipeline.git
cd video-pipeline
pip install -r requirements.txt
cp .env.example .env  # Fill in your API keys and config
python main.py
```

> Requires Python 3.13+ and access to mapped NAS directory (e.g. `Z:\2025.08.05\hits\`).

---

## 🗂️ Folder Structure

```
video-pipeline/
├── main.py
├── config.py
├── .env.example
├── modules/
│   ├── render_engine.py
│   ├── title_utils.py
│   ├── thumbnail_utils.py
│   ├── yt_poster.py
│   └── ...
├── assets/         # Branding assets (intros, fonts, logos)
├── logs/           # Sync logs, wiki publish logs, etc.
└── metadata/
    └── history/    # Per-clip metadata archive
```

---

## 📚 Documentation

Full documentation is hosted in the GitHub Wiki:
👉 [📖 LCS Pipeline Wiki](https://github.com/LCS-Gramps/video-pipeline/wiki)

Recommended pages:

* [`Home`](https://github.com/LCS-Gramps/video-pipeline/wiki)
* [`Clip Handling Logic`](https://github.com/LCS-Gramps/video-pipeline/wiki/Clip-Handling-Logic)
* [`Metadata Extraction`](https://github.com/LCS-Gramps/video-pipeline/wiki/Metadata-Extraction)
* [`YouTube Upload Logic`](https://github.com/LCS-Gramps/video-pipeline/wiki/YouTube-Upload-Logic)

---

## 🧪 Development Mode

* `DEBUG=True` in `.env` disables destructive operations
* All modules can be run/tested independently
* Wiki editing is supported via local Markdown and `wiki_publish.log`

---

## 🧙 About

Created by **Gramps** for Llama Chile Shop — a custom content pipeline for old-school gaming chaos.

> Maintainer: `gramps@llamachile.shop`
> Contributions welcome in the form of bug reports, pull requests, or Fortnite gifts. 🎁
