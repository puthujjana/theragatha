import re
import argparse
import glob
from pathlib import Path
from typing import Optional

# ...existing code...

TITLE_RE = re.compile(r'^\s*(\d+\.\d+)\s+(.*\S)\s*$', re.UNICODE)
PAGE_HEADING_RE = re.compile(r'^\s*chapter\s+\w+(?:\s+\d+)?\s*$', re.IGNORECASE)
LEADING_NUM_RE = re.compile(r'^\s*\d+[\.,]?\s+(.*)$')
REMOVE_LINE_RE = re.compile(r'^\s*\d+\s*$', re.UNICODE)  # lines that are just numbers
VERSIONS_RE = re.compile(r'^\s*verses of senior monks\s*$', re.IGNORECASE)

def process_text(text: str) -> str:
    lines = text.splitlines()
    out_lines = []
    inside_verse = False

    for line in lines:
        stripped = line.rstrip()

        # drop page-heading lines like "chapter sixteen 157"
        if PAGE_HEADING_RE.match(stripped):
            continue

        # drop the "verses of senior monks" heading
        if VERSIONS_RE.match(stripped):
            continue

        # drop lines that are just a page number
        if REMOVE_LINE_RE.match(stripped):
            continue

        # detect verse title like "16.1 Adhimutta"
        m_title = TITLE_RE.match(stripped)
        if m_title:
            # ensure there is a blank line before a new verse title
            if out_lines and out_lines[-1].strip() != '':
                out_lines.append('')

            title_text = f"{m_title.group(1)} {m_title.group(2)}"
            out_lines.append(f"## {title_text}")
            # ensure a blank line after the title (so title and verse are separated)
            out_lines.append('')
            inside_verse = True
            continue

        # remove leading inline line numbers (e.g. "705 This is a line..."), but do not strip titles like "16.1"
        m_lead = LEADING_NUM_RE.match(stripped)
        if m_lead and not TITLE_RE.match(stripped):
            stripped = m_lead.group(1)

        # If we are inside a verse block, ensure non-empty lines end with two spaces (markdown hard break)
        if inside_verse:
            if stripped.strip() == '':
                # blank line ends a paragraph but keep inside_verse until next title
                out_lines.append('')
            else:
                # add two spaces for a hard break, avoid duplicating trailing spaces
                out_lines.append(stripped.rstrip() + '  ')
            continue

        # default: passthrough other lines unchanged
        out_lines.append(stripped)

    # Ensure file ends with a newline
    return "\n".join(out_lines).rstrip() + "\n"

def process_file(path: Path, inplace: bool = False, out_dir: Optional[Path] = None):
    text = path.read_text(encoding='utf-8')
    new_text = process_text(text)

    if inplace:
        path.write_text(new_text, encoding='utf-8')
        print(f"Overwrote {path}")
    else:
        out_dir = out_dir or path.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / path.name
        out_path.write_text(new_text, encoding='utf-8')
        print(f"Wrote {out_path}")

def main():
    ap = argparse.ArgumentParser(description="Process chapter markdown files: strip line numbers, remove page headings and 'verses of senior monks', prefix verse titles, add double spaces at end of verse lines, and ensure blank lines between verses.")
    ap.add_argument("patterns", nargs="+", help="File paths or glob patterns to process (e.g. content/.../chapter-sixteen.md)")
    ap.add_argument("--in-place", action="store_true", help="Overwrite the source files")
    ap.add_argument("--out-dir", help="Directory to write processed files (default: same directory as input)")
    args = ap.parse_args()

    out_dir = Path(args.out_dir) if args.out_dir else None
    files = []
    for pat in args.patterns:
        matched = glob.glob(pat)
        if not matched:
            print(f"No files matched: {pat}")
        else:
            files.extend(matched)

    for f in files:
        p = Path(f)
        process_file(p, inplace=args.in_place, out_dir=out_dir)

if __name__ == "__main__":
    main()
# 

#Run from your repo root, for example:
#bash
#python3  "content/en/theragatha/sujato/chapter-sixteen/chapter-sixteen.md" --in-place