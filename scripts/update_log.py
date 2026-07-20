#!/usr/bin/env python3
"""Update data/log.json from a day's note frontmatter.

Usage: python3 scripts/update_log.py [YYYY-MM-DD]
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm


def main() -> None:
    day = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()

    note_path = ROOT / "notes" / f"{day}.md"
    if not note_path.exists():
        sys.exit(f"No note found at {note_path}")

    fm = parse_frontmatter(note_path.read_text())
    summary = fm.get("summary", "")
    try:
        hours = float(fm.get("hours", 0) or 0)
    except ValueError:
        hours = 0

    if not summary:
        print("WARNING: the note's `summary:` frontmatter is empty — "
              "the timeline tooltip and X post will be blank.")

    video_path = ROOT / "media" / f"{day}.mp4"
    entry = {
        "date": day,
        "summary": summary,
        "hours": hours,
        "video": f"media/{day}.mp4" if video_path.exists() else None,
    }

    log_path = ROOT / "data" / "log.json"
    entries = json.loads(log_path.read_text()) if log_path.exists() else []
    entries = [e for e in entries if e["date"] != day]
    entries.append(entry)
    entries.sort(key=lambda e: e["date"])
    log_path.write_text(json.dumps(entries, indent=2) + "\n")
    print(f"Updated data/log.json ({len(entries)} entries)")


if __name__ == "__main__":
    main()
