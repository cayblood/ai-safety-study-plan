#!/usr/bin/env bash
# Compress a raw session recording into a short timelapse.
# Usage: scripts/make-timelapse.sh [date]   (defaults to today)
# Reads  recordings/<date>-raw.mkv (or .mp4/.mov)
# Writes media/<date>.mp4 — targeted at TARGET_SECONDS (default 100s,
# safely under X's 140s video limit) at 1280px wide.
set -euo pipefail
cd "$(dirname "$0")/.."

DATE="${1:-$(date +%F)}"
TARGET_SECONDS="${TARGET_SECONDS:-100}"
OUT="media/${DATE}.mp4"

RAW=""
for ext in mkv mp4 mov; do
  if [[ -f "recordings/${DATE}-raw.${ext}" ]]; then
    RAW="recordings/${DATE}-raw.${ext}"
    break
  fi
done

if [[ -z "${RAW}" ]]; then
  echo "No raw recording found for ${DATE} (looked for recordings/${DATE}-raw.{mkv,mp4,mov})" >&2
  exit 1
fi

DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "${RAW}")
FACTOR=$(python3 -c "print(max(1.0, ${DURATION} / ${TARGET_SECONDS}))")

echo "Raw duration: ${DURATION%.*}s → timelapse ~${TARGET_SECONDS}s (${FACTOR%.*}x speedup)"

ffmpeg -y -i "${RAW}" \
  -vf "setpts=PTS/${FACTOR},scale=1280:-2,fps=30" \
  -an -c:v libx264 -preset medium -crf 27 -pix_fmt yuv420p -movflags +faststart \
  "${OUT}"

SIZE_MB=$(du -m "${OUT}" | cut -f1)
echo "Wrote ${OUT} (${SIZE_MB} MB)"
if (( SIZE_MB > 20 )); then
  echo "WARNING: ${SIZE_MB} MB is large for a git repo. Consider raising CRF or lowering TARGET_SECONDS." >&2
fi
