import re
from pathlib import Path

def update_verse_headers(file_path):
    # Read the file content
    content = file_path.read_text(encoding='utf-8')
    
    # Only process individual verse files (thag*.md), skip chapter_one.md
    if not file_path.stem.startswith('thag'):
        return
        
    # Replace ## for verse titles with #
    # Pattern matches "## N.N Name" at start of line
    updated = re.sub(r'^##\s+(\d+\.\d+\s+\S.*?)$', 
                     r'# \1', 
                     content,
                     flags=re.MULTILINE)
    
    if content != updated:
        # Backup original file
        backup = file_path.with_suffix(file_path.suffix + '.bak')
        file_path.rename(backup)
        
        # Write updated content
        file_path.write_text(updated, encoding='utf-8')
        print(f"Updated {file_path.name}")

def main():
    # Process all .md files in current directory
    chapter_dir = Path(__file__).parent
    for md_file in chapter_dir.glob('*.md'):
        update_verse_headers(md_file)

if __name__ == '__main__':
    main()