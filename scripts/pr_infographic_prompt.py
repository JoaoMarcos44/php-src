"""Generate the three visual briefs prepared for this PHP audit."""

import argparse
import json


THEMES = {
    "pdo sqlite": {
        "name": "Library checkout cards",
        "art_direction": (
            "A warm, carefully typeset editorial illustration using library "
            "checkout cards and a card drawer as the visual metaphor. Use cream "
            "paper, muted navy and rust, crisp lines and generous whitespace."
        ),
        "story": (
            "A prepared statement is executed again while its previous row is "
            "unread. The next execution has no rows. A stale prefetched-row flag "
            "can cause fetchAll to return a phantom row. Show a before and after "
            "comparison: the buggy result is an array containing one null-valued "
            "row, while the fixed result is an empty array. The fix clears the "
            "pre_fetched flag whenever the cursor resets."
        ),
        "labels": [
            "PDO SQLite: phantom row",
            "UNREAD ROW",
            "EMPTY RESULT",
            'BUG: [{"answer":null}]',
            "FIX: []",
            "CLEAR pre_fetched ON RESET",
        ],
    },
    "array_unshift": {
        "name": "Railway stops",
        "art_direction": (
            "A modern railway-map editorial illustration with sparse track "
            "lines, clear station markers and flat paper texture. Use teal, "
            "saffron, off-white and dark ink."
        ),
        "story": (
            "A reference foreach iterates an array containing a deleted slot. "
            "While visiting b, array_unshift adds x at the front and compacts the "
            "hole. The old iterator position skips c. Show the buggy visit route "
            "b to d and the fixed route b to c to d. The fix remaps the iterator "
            "to the compacted live slots before applying the insertion offset. "
            "Do not show x as a visited value."
        ),
        "labels": [
            "array_unshift(): skipped value",
            "FOREACH BY REFERENCE",
            "ADD x AT FRONT",
            "BUG: b, d",
            "FIX: b, c, d",
            "REMAP ITERATOR",
        ],
    },
    "json": {
        "name": "Botanical specimen catalog",
        "art_direction": (
            "An elegant botanical specimen catalog illustration with pressed "
            "leaves, ruled identification cards, fine linework and ample "
            "whitespace. Use soft ivory, sage green, terracotta and dark ink."
        ),
        "story": (
            "JSON encodes an uninitialized backed typed property with a setter "
            "hook as null by mistake. Compare the buggy object containing id:null "
            "with the fixed empty object. The fix skips the internal uninitialized "
            "sentinel. A separate nullable property explicitly set to null still "
            "appears as id:null, as does a getter that returns null. The blank "
            "specimen card represents an absent field, not a null value."
        ),
        "labels": [
            "JSON: missing is not null",
            "UNINITIALIZED",
            'BUG: {"id":null}',
            "FIX: {}",
            'EXPLICIT NULL: {"id":null}',
            "SKIP UNINITIALIZED",
        ],
    },
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--docs", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    theme = next(
        (value for key, value in THEMES.items() if key in args.title.casefold()),
        None,
    )
    if theme is None:
        parser.error("title must identify PDO SQLite, array_unshift, or JSON")

    labels = "\n".join(f"- {label}" for label in theme["labels"])
    prompt = (
        "Use case: infographic-diagram\n"
        "Asset type: one illustrative infographic for a PHP bug report.\n"
        "Primary request: Explain the observed bug and its proposed fix to PHP "
        "contributors in plain English.\n"
        f"Style and composition: {theme['art_direction']} "
        "Create one landscape poster with a clear visual reading order and a "
        "large, legible before-and-after comparison.\n"
        f"Factual story: {theme['story']}\n"
        "Render only the following text, exactly as written and legible:\n"
        f"{labels}\n"
        "Constraints: Accuracy is more important than decoration. Keep all "
        "examples and punctuation exact. Use no invented numbers, logos, "
        "watermarks or additional text.\n"
        "Background facts for the artist, not additional visible copy:\n"
        f"PR title: {args.title}\n"
        f"Summary: {args.summary}\n"
        f"Validation and documentation: {args.docs}"
    )
    result = {
        "title": args.title,
        "summary": args.summary,
        "docs": args.docs,
        "theme": theme,
        "prompt": prompt,
    }
    print(json.dumps(result, indent=2) if args.json else prompt)


if __name__ == "__main__":
    main()
