import os
from pathlib import Path

def create_new_entry(verse_number):
    
    # The raw template string with placeholders for metadata
    DEFAULT_METADATA = {
    "title": '"Verse ' + str(verse_number) + '"',
    "id": '"thag1.' + str(verse_number) + '"',
    "chapter": 1,
    "verse": verse_number,
    "edition": "SuttaCentral",
    "collection": "Theragāthā",
    "pali_source": "suttacentral",
    "translator": "",
    "weight": 1,
    "slug": '"thag1.' + str(verse_number) + '"',
    "bookHidden": "true"
    }

    TEMPLATE = "---\n" + "\n".join(f"{key}: {value}" for key, value in DEFAULT_METADATA.items()) + "\n---\n\n"

    filename = "thag1." + str(verse_number) + ".md"

    if os.path.exists(filename):
        print(f"File already exists.")
        return
    
    with open(filename, "w") as f:
        f.write(TEMPLATE + "# " + "1." + str(verse_number) + "\n\n\n\n## Notes")

verse_number = input("Please enter the verse number: ")
create_new_entry(verse_number)