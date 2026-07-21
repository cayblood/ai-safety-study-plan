#!/usr/bin/env bash
# Wrap up a study day: build the timelapse, update the log index,
# commit + push, and optionally post to X.
# Usage: scripts/end-day.sh [date]   (defaults to today)
#
# Expects notes/<date>.md to exist with frontmatter `summary:` and
# `hours:` filled in. The timelapse step is skipped gracefully if no
# raw recording exists.
set -euo pipefail
cd "$(dirname "$0")/.."

DATE="${1:-$(date +%F)}"
NOTE="notes/${DATE}.md"

if [[ ! -f "${NOTE}" ]]; then
  echo "No note at ${NOTE} — run scripts/new-day.sh first." >&2
  exit 1
fi

# 1. Timelapse (skip if no raw footage).
if ls recordings/${DATE}-raw.* >/dev/null 2>&1; then
  if [[ ! -f "media/${DATE}.mp4" ]]; then
    scripts/make-timelapse.sh "${DATE}"
  else
    echo "media/${DATE}.mp4 already exists — skipping timelapse build."
  fi
else
  echo "No raw recording for ${DATE}; skipping timelapse."
fi

# 2. Update data/log.json from the note's frontmatter.
python3 scripts/update_log.py "${DATE}"

# 2b. Rebuild the Anki deck from all notes' card lines.
python3 scripts/make_deck.py || echo "Deck build failed (is genanki installed?) — continuing."

# 3. Commit and push.
git add -A
if git diff --cached --quiet; then
  echo "Nothing new to commit."
else
  git commit -m "Log: ${DATE}"
  git push
fi

# 4. Post to X (only if credentials are configured).
if [[ -f .env ]]; then
  python3 scripts/post_to_x.py "${DATE}" || echo "X post failed — see above. You can retry with: python3 scripts/post_to_x.py ${DATE}"
else
  echo "No .env found — skipping X post. Copy .env.example to .env and add your X API keys to enable."
fi
