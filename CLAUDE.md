# AI Safety Study Plan repo

Public study log + three-track curriculum (see `plan/`). Static site on GitHub Pages, no build step. Daily workflow: `scripts/new-day.sh` → fill `notes/YYYY-MM-DD.md` → `scripts/end-day.sh` (timelapse → log.json → Anki deck → push → X post).

## Conventions

- Daily notes: `notes/YYYY-MM-DD.md` with frontmatter `summary:` (one line, becomes tooltip + X post) and `hours:` (drives streak-dot intensity).
- Flashcards: `- question :: answer` lines in notes (cloze: `- cloze :: {{c1::...}}`); `scripts/make_deck.py` sweeps them into `data/study-deck.apkg`.
- Raw recordings are gitignored; only compressed timelapses in `media/` are committed.
- `.env` holds X API keys — never commit it.

## Quizzing (Friday consolidation & card generation)

When asked to **generate cards** from a day's note: emit `- question :: answer` lines in the note's Cards section format — atomic (one fact each), reversible where sensible, inline math as `$...$`. Don't create cards for Math Academy content (it has its own spaced repetition); mech interp and philosophy only.

When asked to **quiz** ("quiz me", "Friday quiz"): read the last 5–10 daily notes' Cards sections and the week's note content, then run an oral exam — one question at a time, wait for the answer, grade harshly, probe follow-ups on anything shaky, no praise inflation. Prioritize items answered poorly in previous quizzes (check `## Lessons learned` sections for recorded misses) and conceptual "why" questions over pure recall. End with a summary of weak spots, and suggest the user record them in today's Lessons learned.
