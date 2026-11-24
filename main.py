#!/usr/bin/env python3
"""Two-Sentence Horror — make.fun bounty
u-suroto-two-sentence-horror-acea9253.

Writes one horror story of exactly two sentences (at most 400
characters) to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

Pure standard library; deterministic — the same bytes on every run.
"""

import os
import sys

# The story: a child's imaginary friend keeps acquiring the trappings of
# a real person — a name, a bedroom, a toothbrush — and the second
# sentence quietly proves the friend was in the bathroom this morning.
# Nothing is explained; the reader fills in the worst of it.
STORY = (
    "My daughter's imaginary friend has a name now, and a bedroom, "
    "and a toothbrush in our bathroom. "
    "This morning the toothbrush was wet."
)

MAX_CHARS = 400


def count_sentences(text: str) -> int:
    """Count sentences by terminal punctuation, ignoring abbreviations."""
    count = 0
    for i, ch in enumerate(text):
        if ch in ".!?":
            # A sentence ends at terminal punctuation followed by a space
            # or the end of the text.
            if i + 1 == len(text) or text[i + 1] == " ":
                count += 1
    return count


def main() -> int:
    story = STORY
    if not story or not story.strip():
        print("entry is empty", file=sys.stderr)
        return 1
    if len(story) > MAX_CHARS:
        print(
            f"entry is {len(story)} chars, over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1
    if story != story.strip():
        print("entry has leading or trailing whitespace", file=sys.stderr)
        return 1
    if count_sentences(story) != 2:
        print(
            f"entry has {count_sentences(story)} sentences, expected exactly 2",
            file=sys.stderr,
        )
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = story.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Re-read and verify the bytes we wrote.
    with open(path, "rb") as f:
        if f.read() != data:
            print("verification failed: entry.txt differs", file=sys.stderr)
            return 1
    print(f"wrote {len(data)} bytes ({len(story)} chars) to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
