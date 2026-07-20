#!/usr/bin/env bash
# Create today's note from the template.
# Usage: scripts/new-day.sh [date]   (defaults to today)
set -euo pipefail
cd "$(dirname "$0")/.."

DATE="${1:-$(date +%F)}"
NOTE="notes/${DATE}.md"

if [[ -f "${NOTE}" ]]; then
  echo "${NOTE} already exists."
  exit 0
fi

cat > "${NOTE}" <<EOF
---
date: ${DATE}
summary:
hours: 0
---

# Session log — ${DATE}

## ML foundations (Math Academy) — 2h

-

## Mechanistic interpretability — 2h

-

## Philosophy (evening reading) — 1h

-

## Lessons learned

-
EOF

echo "Created ${NOTE}"
