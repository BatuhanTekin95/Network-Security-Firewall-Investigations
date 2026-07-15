"""Fail when a local Markdown link points to a missing file."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
SKIPPED_PREFIXES = ("http://", "https://", "mailto:", "#")


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if ".git" not in path.parts
    )


def local_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().strip("<>")
    if not target or target.lower().startswith(SKIPPED_PREFIXES):
        return None

    target = unquote(target.split("#", 1)[0])
    if not target:
        return None

    if target.startswith("/"):
        return ROOT / target.lstrip("/")
    return source.parent / target


def main() -> int:
    failures: list[str] = []

    for source in markdown_files():
        text = source.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(text):
            target = local_target(source, match.group(1))
            if target is not None and not target.resolve().exists():
                failures.append(
                    f"{source.relative_to(ROOT)} -> {match.group(1)}"
                )

    if failures:
        print("Broken local Markdown links:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Checked {len(markdown_files())} Markdown files: all local links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
