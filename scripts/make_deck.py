#!/usr/bin/env python3
"""Extract flashcards from all daily notes into an Anki deck.

Card syntax (anywhere in notes/*.md, one per list line):
    - question :: answer
    - cloze :: text with {{c1::hidden part}} and {{c2::another}}

Inline math: $...$ and display math $$...$$ are converted to Anki's
MathJax delimiters. Card identity is keyed on the question text, so
editing an answer updates the existing card on re-import instead of
duplicating it.

Usage: python3 scripts/make_deck.py   →  writes data/study-deck.apkg
Import the .apkg into Anki (File > Import); re-import after new cards.
"""
import re
import sys
from pathlib import Path

import genanki

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "study-deck.apkg"

# Fixed IDs so re-imports update the same deck/models.
DECK_ID = 1626351913
BASIC_MODEL_ID = 1607392319
CLOZE_MODEL_ID = 1607392320

CARD_RE = re.compile(r"^[-*]\s+(.+?)\s+::\s+(.+)$")

BASIC_MODEL = genanki.Model(
    BASIC_MODEL_ID,
    "Study Log Basic",
    fields=[{"name": "Question"}, {"name": "Answer"}, {"name": "Source"}],
    templates=[{
        "name": "Card 1",
        "qfmt": "{{Question}}",
        "afmt": "{{FrontSide}}<hr id=answer>{{Answer}}"
                "<br><br><span style='font-size:12px;color:#888'>{{Source}}</span>",
    }],
)

CLOZE_MODEL = genanki.Model(
    CLOZE_MODEL_ID,
    "Study Log Cloze",
    model_type=genanki.Model.CLOZE,
    fields=[{"name": "Text"}, {"name": "Source"}],
    templates=[{
        "name": "Cloze",
        "qfmt": "{{cloze:Text}}",
        "afmt": "{{cloze:Text}}"
                "<br><br><span style='font-size:12px;color:#888'>{{Source}}</span>",
    }],
)


def mathjax(text: str) -> str:
    """Convert $...$ / $$...$$ to Anki MathJax delimiters."""
    text = re.sub(r"\$\$(.+?)\$\$", r"\\[\1\\]", text)
    return re.sub(r"\$(.+?)\$", r"\\(\1\\)", text)


def main() -> None:
    deck = genanki.Deck(DECK_ID, "AI Safety Study Log")
    count = 0

    for note_path in sorted((ROOT / "notes").glob("*.md")):
        source = note_path.stem  # the date
        for line in note_path.read_text().splitlines():
            m = CARD_RE.match(line.strip())
            if not m:
                continue
            question, answer = mathjax(m.group(1)), mathjax(m.group(2))
            if question.lower() == "cloze":
                note = genanki.Note(
                    model=CLOZE_MODEL,
                    fields=[answer, source],
                    guid=genanki.guid_for("cloze", answer),
                )
            else:
                note = genanki.Note(
                    model=BASIC_MODEL,
                    fields=[question, answer, source],
                    guid=genanki.guid_for(question),
                )
            deck.add_note(note)
            count += 1

    if count == 0:
        print("No cards found (no '- question :: answer' lines in notes/).")
        return

    genanki.Package(deck).write_to_file(str(OUT))
    print(f"Wrote {OUT.relative_to(ROOT)} ({count} cards)")


if __name__ == "__main__":
    main()
