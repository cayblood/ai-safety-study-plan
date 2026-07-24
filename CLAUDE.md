# AI Safety Study Plan repo

Public study log + three-track curriculum (see `plan/`). Static site on GitHub Pages, no build step. Daily workflow: `scripts/new-day.sh` → fill `notes/YYYY-MM-DD.md` → `scripts/end-day.sh` (timelapse → log.json → Anki deck → push → X post).

## Conventions

- Daily notes: `notes/YYYY-MM-DD.md` with frontmatter `summary:` (one line, becomes tooltip + X post) and `hours:` (drives streak-dot intensity).
- Flashcards: `- question :: answer` lines in notes (cloze: `- cloze :: {{c1::...}}`); `scripts/make_deck.py` sweeps them into `data/study-deck.apkg`.
- Raw recordings are gitignored; only compressed timelapses in `media/` are committed.
- `.env` holds X API keys — never commit it.

## Quizzing (Friday consolidation & card generation)

When asked to **generate cards** from a day's note: emit `- question :: answer` lines in the note's Cards section format — atomic (one fact each), reversible where sensible, inline math as `$...$`. Don't create cards for Math Academy content (it has its own spaced repetition); mech interp and philosophy only.

When asked to **quiz** ("quiz me", "Friday quiz"): 

1. Read the last 2–3 files in `quizzes/` (if any) and the last 5–10 daily notes (Cards sections + content).
2. Run an oral exam — one question at a time, wait for the answer, grade harshly, probe follow-ups on anything shaky, no praise inflation. Prioritize previous `miss`/`shaky` items and conceptual "why" questions over pure recall; skip items marked `pass` in the last two quizzes.
3. Afterwards, write `quizzes/YYYY-MM-DD.md`: a `## Results` list with one line per question — `- <topic/question> — pass|shaky|miss (note)` — and a `## Weak spots` summary. Suggest turning each miss into a new card line in today's note (misses → Anki).

Quizzes should run in a fresh session, not a long-lived one — this file plus `quizzes/` is the memory system; no session context is assumed.
