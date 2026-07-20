#!/usr/bin/env python3
"""Post the day's timelapse + summary to X.

Usage: python3 scripts/post_to_x.py [YYYY-MM-DD]

Requires a .env file (see .env.example) with OAuth 1.0a user-context
credentials for an X developer app that has Read & Write permissions.
Uses the v1.1 chunked media upload endpoint (still required for video)
and the v2 endpoint for creating the post.

Dependencies: pip install -r scripts/requirements.txt
"""
import os
import re
import sys
import time
from datetime import date
from pathlib import Path

import requests
from requests_oauthlib import OAuth1

ROOT = Path(__file__).resolve().parent.parent
MEDIA_UPLOAD_URL = "https://upload.twitter.com/1.1/media/upload.json"
TWEET_URL = "https://api.twitter.com/2/tweets"
SITE_BASE = os.environ.get(
    "SITE_BASE", "https://cayblood.github.io/ai-safety-study-plan"
)


def load_env() -> None:
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def get_auth() -> OAuth1:
    keys = ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_TOKEN_SECRET"]
    missing = [k for k in keys if not os.environ.get(k)]
    if missing:
        sys.exit(f"Missing credentials in .env: {', '.join(missing)}")
    return OAuth1(
        os.environ["X_API_KEY"],
        os.environ["X_API_SECRET"],
        os.environ["X_ACCESS_TOKEN"],
        os.environ["X_ACCESS_TOKEN_SECRET"],
    )


def upload_video(auth: OAuth1, path: Path) -> str:
    total_bytes = path.stat().st_size
    print(f"Uploading {path.name} ({total_bytes / 1e6:.1f} MB)...")

    r = requests.post(MEDIA_UPLOAD_URL, auth=auth, data={
        "command": "INIT",
        "media_type": "video/mp4",
        "media_category": "tweet_video",
        "total_bytes": total_bytes,
    })
    r.raise_for_status()
    media_id = r.json()["media_id_string"]

    chunk_size = 4 * 1024 * 1024
    with path.open("rb") as f:
        segment = 0
        while chunk := f.read(chunk_size):
            r = requests.post(MEDIA_UPLOAD_URL, auth=auth,
                              data={"command": "APPEND", "media_id": media_id,
                                    "segment_index": segment},
                              files={"media": chunk})
            r.raise_for_status()
            segment += 1

    r = requests.post(MEDIA_UPLOAD_URL, auth=auth,
                      data={"command": "FINALIZE", "media_id": media_id})
    r.raise_for_status()

    # Wait for async video processing.
    info = r.json().get("processing_info")
    while info and info["state"] in ("pending", "in_progress"):
        wait = info.get("check_after_secs", 5)
        print(f"  processing ({info['state']}), waiting {wait}s...")
        time.sleep(wait)
        r = requests.get(MEDIA_UPLOAD_URL, auth=auth,
                         params={"command": "STATUS", "media_id": media_id})
        r.raise_for_status()
        info = r.json().get("processing_info")

    if info and info["state"] == "failed":
        sys.exit(f"Video processing failed: {info.get('error')}")
    return media_id


def build_text(day: str, summary: str) -> str:
    day_url = f"{SITE_BASE}/day.html?date={day}"
    # X wraps links to 23 chars; budget for text + space + link.
    prefix = f"AI safety study log, {day}: "
    budget = 280 - 23 - 1 - len(prefix)
    if len(summary) > budget:
        summary = summary[: budget - 1].rstrip() + "…"
    return f"{prefix}{summary} {day_url}"


def main() -> None:
    day = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    load_env()
    auth = get_auth()

    note_path = ROOT / "notes" / f"{day}.md"
    summary = ""
    if note_path.exists():
        m = re.search(r"^summary:\s*(.+)$", note_path.read_text(), re.MULTILINE)
        if m:
            summary = m.group(1).strip()
    if not summary:
        sys.exit(f"No summary found in {note_path} frontmatter — fill in `summary:` first.")

    payload = {"text": build_text(day, summary)}

    video_path = ROOT / "media" / f"{day}.mp4"
    if video_path.exists():
        media_id = upload_video(auth, video_path)
        payload["media"] = {"media_ids": [media_id]}
    else:
        print(f"No timelapse at {video_path}; posting text only.")

    r = requests.post(TWEET_URL, auth=auth, json=payload)
    if r.status_code >= 400:
        sys.exit(f"Post failed ({r.status_code}): {r.text}")
    tweet_id = r.json()["data"]["id"]
    print(f"Posted: https://x.com/i/status/{tweet_id}")


if __name__ == "__main__":
    main()
