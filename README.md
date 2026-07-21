# AI Safety Study Plan & Public Log

A self-study program for pivoting into AI safety research, with a public accountability log. Live site: **https://cayblood.github.io/ai-safety-study-plan/**

- **Study plan:** [overview](plan/00-overview.md) · [ML foundations](plan/01-ml-foundations.md) · [mech interp](plan/02-mech-interp.md) · [philosophy](plan/03-philosophy.md)
- **Log:** one note per day in [`notes/`](notes/), one timelapse per session in [`media/`](media/), indexed by [`data/log.json`](data/log.json), rendered as a GitHub-style weekday streak grid on the site.

## Daily workflow

```bash
# Morning: start the note and the screen recording
scripts/new-day.sh          # creates notes/YYYY-MM-DD.md from the template
scripts/record-session.sh   # low-fps screen capture (press q to stop)

# During the day: fill in the note; set `summary:` and `hours:` in its frontmatter

# Evening: wrap up
scripts/end-day.sh          # timelapse → log.json → commit+push → X post
```

Each step is also runnable on its own: `make-timelapse.sh`, `update_log.py`, `post_to_x.py` all take an optional `YYYY-MM-DD` argument.

## Flashcards

Capture quizzable facts as one-liners anywhere in a daily note (the template has a `## Cards` section):

```markdown
- What does activation patching measure? :: Causal effect of swapping in a corrupted activation
- cloze :: The {{c1::residual stream}} carries information between layers
- SVD of M :: $U \Sigma V^T$
```

`scripts/make_deck.py` (run automatically by `end-day.sh`) sweeps every note into `data/study-deck.apkg` — import into [Anki](https://apps.ankiweb.net) with File → Import. Card identity is keyed on the question, so re-importing updates cards instead of duplicating them, and scheduling progress is preserved. Weekly ritual: have an LLM draft cards from the day's note, and run a harsh-grader oral quiz on Fridays (prompts documented in CLAUDE.md).

## One-time setup

1. **ffmpeg** — `brew install ffmpeg` (screen-capture permission: System Settings → Privacy & Security → Screen Recording → allow your terminal).
2. **Python deps** — `pip3 install -r scripts/requirements.txt`
3. **X API** — create an app at [developer.x.com](https://developer.x.com) (free tier: 500 posts/month), set permissions to *Read and write*, generate OAuth 1.0a keys, then `cp .env.example .env` and fill them in. `.env` is gitignored.

## Notes on the timelapse pipeline

- Raw recordings go to `recordings/` (gitignored) at 0.5 fps; `make-timelapse.sh` compresses to a ~100-second 720p+ mp4 (safely under X's 140 s video limit), typically a few MB.
- Committed timelapses live in `media/`. At ~5 MB/day this stays manageable for a long time; if the repo grows too large, move older videos to a release asset or external storage and update `data/log.json` paths.

## Site

Plain static HTML/JS on GitHub Pages — no build step. `index.html` renders the streak grid from `data/log.json`; `day.html?date=YYYY-MM-DD` shows a day's timelapse and notes; `plan.html?doc=…` renders the plan documents.
