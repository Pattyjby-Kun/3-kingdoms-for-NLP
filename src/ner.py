# src/ner.py
import os
import json
from pythainlp.tag import NER
from pythainlp.tokenize import word_tokenize

# โหลดโมเดล NER ภาษาไทย
ner = NER("thainer")  # ใช้โมเดล thainer ของ PyThaiNLP

def extract_entities(file_path, character_list_path="D:\Trump\data\character_list.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"ไม่พบไฟล์: {file_path}")

    # โหลดรายชื่อตัวละคร
    with open(character_list_path, "r", encoding="utf-8") as f:
        characters = json.load(f)["characters"]

    # อ่านข้อความ
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    words = word_tokenize(text, keep_whitespace=False)
    found = [c for c in characters if c in words or c in text]

    # ลบชื่อซ้ำ
    found = list(set(found))

    return found

if __name__ == "__main__":
    path = "../data/cleaned/chapter1_cleaned.txt"
    entities = extract_entities(path)
    print("รายชื่อตัวละครที่ตรวจพบ:")
    for e in entities:
        print("-", e)