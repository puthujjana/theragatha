import os
import re

INPUT_FILE = "chapter_four.md"  # adjust path if needed

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Split out any front matter from the body.
    parts = content.split("---", 2)
    if len(parts) >= 3:
        front_matter = parts[1].strip()  # may use if needed
        body = parts[2]
    else:
        body = content

    # RegEx pattern to find verse headings like "## 1.4 Puṇṇa"
    verse_pattern = re.compile(r"^##\s+(\d+\.\d+)\s+(.*)$", re.MULTILINE)
    matches = list(verse_pattern.finditer(body))
    if not matches:
        print("No verses found; check heading formatting")
        return
    
    # x = 0

    for i, match in enumerate(matches):
        #if x > 0:
            #return
        #x = x+1
        verse_number = match.group(1)  # e.g., "1.4"
        verse_title = match.group(2).strip()  # e.g., "Puṇṇa"

        # Determine the region of text for this verse.
        start_index = match.start()
        end_index = matches[i+1].start() if i+1 < len(matches) else len(body)
        verse_body = body[start_index:end_index].strip()

        # Insert an extra line break after the verse heading line.
        lines = verse_body.splitlines()
        if len(lines) > 1:
            verse_body = lines[0] + "\n\n" + "\n".join(lines[1:])
        else:
            verse_body = lines[0]

        # Construct a new front matter.
        # Here we use the part after the dot as the verse number in the front matter.
        verse_suffix = verse_number.split(".")[1]
        verse_chapter = verse_number.split(".")[0]
        new_front_matter = f"""---
title: "{lines[0][3:].strip()}"
id: "thag{verse_number}"
chapter: {verse_chapter}
verse: {verse_suffix}
slug: "thag{verse_number}"
edition: "SuttaCentral"
collection: "Theragāthā"
pali_source: "suttacentral"
translator: "Bhikkhu Sujato"
weight: {verse_suffix}
bookHidden: true
---
"""

        new_content = new_front_matter + "\n" + verse_body + "\n\n## Notes"

        # Write the new file (e.g., thag1.4.md)
        output_filename = f"thag{verse_number}.md"
        with open(output_filename, "w", encoding="utf-8") as out:
            out.write(new_content)
        print(f"Wrote {output_filename}")

if __name__ == "__main__":
    main()