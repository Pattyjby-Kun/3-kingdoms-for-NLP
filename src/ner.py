import os
import json
from pythainlp.tokenize import word_tokenize

# โหลดรายชื่อตัวละครจาก JSON
CHARACTER_LIST_PATH = r"C:\Homework\3-kingdoms-for-NLP\data\character_list.json"
INPUT_DIR = r"C:\Homework\3-kingdoms-for-NLP\data\cleaned"
OUTPUT_PATH = r"C:\Homework\3-kingdoms-for-NLP\output\character_summary.json"

def extract_entities(file_path, characters):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    words = word_tokenize(text, keep_whitespace=False)
    found = [c for c in characters if c in words or c in text]
    return list(set(found))

if __name__ == "__main__":
    # โหลดตัวละครจาก JSON
    with open(CHARACTER_LIST_PATH, "r", encoding="utf-8") as f:
        characters = json.load(f)["characters"]

    summary = {}

    for file in os.listdir(INPUT_DIR):
        if file.endswith("_cleaned.txt"):
            path = os.path.join(INPUT_DIR, file)
            found = extract_entities(path, characters)
            summary[file] = found
            print(f"📘 {file}: {', '.join(found) if found else '(ไม่พบตัวละคร)'}")

    # บันทึกผลรวม
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=4)

    print(f"\n✅ บันทึกผลรวมที่: {OUTPUT_PATH}")
