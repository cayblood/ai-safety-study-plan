#!/usr/bin/env bash
# Record the screen at low framerate for a study-session timelapse.
# Usage: scripts/record-session.sh [date]   (defaults to today)
# Stop with q (in the ffmpeg window) or Ctrl-C. Raw footage lands in
# recordings/<date>-raw.mkv; it is gitignored. Run make-timelapse.sh after.
#
# NOTE: the first run will trigger a macOS Screen Recording permission
# prompt for your terminal app. Grant it in System Settings > Privacy &
# Security > Screen Recording, then re-run.
set -euo pipefail
cd "$(dirname "$0")/.."

DATE="${1:-$(date +%F)}"
OUT="recordings/${DATE}-raw.mkv"
FPS="${RECORD_FPS:-0.5}"   # one frame every 2 seconds

# Find the screen-capture device index on macOS.
DEVICE_INDEX=$(ffmpeg -f avfoundation -list_devices true -i "" 2>&1 |
  grep -m1 "Capture screen" | sed -E 's/.*\[([0-9]+)\].*/\1/') || true

if [[ -z "${DEVICE_INDEX}" ]]; then
  echo "Could not find a screen-capture device. Output of device listing:" >&2
  ffmpeg -f avfoundation -list_devices true -i "" 2>&1 | sed 's/^/  /' >&2
  exit 1
fi

echo "Recording screen (device ${DEVICE_INDEX}) at ${FPS} fps to ${OUT}"
echo "Press q to stop."

ffmpeg -f avfoundation -capture_cursor 1 -framerate "${FPS}" \
  -i "${DEVICE_INDEX}:none" \
  -c:v libx264 -preset ultrafast -crf 23 -pix_fmt yuv420p \
  "${OUT}"
