#!/usr/bin/env python3
"""Convert every file in intake/drop/ to plain text in intake/converted/.

Deterministic conversion only -- this script does NOT attempt to parse the
resulting text into structured career data. See CLAUDE.md ("Intake is
manual, not auto-parsed").
"""
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DROP_DIR = REPO_ROOT / "intake" / "drop"
CONVERTED_DIR = REPO_ROOT / "intake" / "converted"

TEXTUTIL_EXTENSIONS = {".doc", ".docx", ".rtf", ".rtfd", ".txt", ".html", ".webarchive"}


def convert_with_textutil(src: Path) -> str:
    result = subprocess.run(
        ["textutil", "-convert", "txt", "-stdout", str(src)],
        capture_output=True, text=True, check=True,
    )
    return result.stdout


def convert_pdf(src: Path) -> str:
    from pdfminer.high_level import extract_text
    return extract_text(str(src))


def main() -> int:
    if not DROP_DIR.exists():
        print(f"No drop folder at {DROP_DIR}", file=sys.stderr)
        return 1

    files = sorted(p for p in DROP_DIR.iterdir() if p.is_file() and p.name != ".gitkeep")
    if not files:
        print(f"Nothing to convert in {DROP_DIR}")
        return 0

    CONVERTED_DIR.mkdir(parents=True, exist_ok=True)

    for src in files:
        ext = src.suffix.lower()
        try:
            if ext in TEXTUTIL_EXTENSIONS:
                text = convert_with_textutil(src)
            elif ext == ".pdf":
                text = convert_pdf(src)
            else:
                print(f"SKIP  {src.name} (unsupported extension {ext!r})")
                continue
        except Exception as exc:
            print(f"FAIL  {src.name}: {exc}", file=sys.stderr)
            continue

        dest = CONVERTED_DIR / (src.stem + ".txt")
        dest.write_text(text)
        note = ""
        if ext == ".pdf" and not text.strip():
            note = "  (empty output -- likely a scanned/image PDF; copy/paste from Preview.app instead)"
        print(f"OK    {src.name} -> {dest.relative_to(REPO_ROOT)}{note}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
