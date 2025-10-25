import re
from pathlib import Path
import sys

FILE = Path(__file__).with_name("chapter_one.md")

def linkify_headings(path: Path):
    text = path.read_text(encoding="utf-8")
    # Match headings like: ## 1.3 Kaṅkhārevata
    pattern = re.compile(r'^(##\s+)(\d+\.\d+)\s+(.*\S)\s*$', re.MULTILINE)
    def repl(m):
        prefix, num, title = m.group(1), m.group(2), m.group(3)
        return f'{prefix}[{num} {title}](../thag{num}/)'
    new_text = pattern.sub(repl, text)
    # backup and write
    backup = path.with_suffix(path.suffix + ".bak")
    path.rename(backup)
    path.write_text(new_text, encoding="utf-8")
    print(f"Updated {path} (backup at {backup})")

if __name__ == "__main__":
    p = FILE if FILE.exists() else Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not p or not p.exists():
        print("Provide path to chapter_one.md or run from the chapter-one directory.")
        sys.exit(1)
    linkify_headings(p)