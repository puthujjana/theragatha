import os
import shutil
import re

directory_path = '/Users/trashboy/Documents/theragatha/content/en/theragatha/sujato'  # Replace with the actual path to your directory

for filename in os.listdir(directory_path):
    if filename.endswith('.md'):
        filepath = os.path.join(directory_path, filename)
        #print(f"Found Markdown file: {filepath}")
        chapter_number = filepath.split("/")[-1].split("-")[1][:-3]
        #print(split)

        destination_path = os.path.join(directory_path, "chapter-" + chapter_number + "/chapter-" + chapter_number + ".md")
        print(destination_path)
        os.mkdir("chapter-" + chapter_number)
        #os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.move(filepath, destination_path)

        # You can now open and process the file, e.g.:
        # with open(filepath, 'r', encoding='utf-8') as f:
        #     content = f.read()
        #     print(content)