import os
import json
from pythainlp.tokenize import sent_tokenize

# 🔹 Path ของไฟล์ข้อมูล
CHARACTER_LIST_PATH = r"C:\Homework\3-kingdoms-for-NLP\data\character_list.json"
INPUT_DIR = r"C:\Homework\3-kingdoms-for-NLP\data\cleaned"
OUTPUT_DIR = r"C:\Homework\3-kingdoms-for-NLP\output\chapter_relations_rulebased"

# 🔹 คำหลักสำหรับตรวจจับความสัมพันธ์
RELATION_KEYWORDS = {
    "พี่น้อง": ["สาบาน", "ร่วมคำสัตย์", "พี่น้อง", "สหาย"],
    "ศัตรู": ["รบกับ", "ต่อสู้กับ", "ทำศึกกับ", "ศัตรู", "ฆ่า", "จับตัว", "ทำร้าย"],
    "พันธมิตร": ["ร่วมรบ", "ช่วย", "เข้าร่วม", "ยกทัพไปด้วยกัน", "สู้ร่วมกัน", "ช่วยเหลือ"],
    "เจ้านาย-ลูกน้อง": ["รับใช้", "ที่ปรึกษา", "คำสั่ง", "ถวาย", "แนะนำ", "ปรึกษา", "ฟังคำสั่ง"]
}


def find_relations_rulebased(file_path, characters):
    """
    วิเคราะห์ความสัมพันธ์ของตัวละครจากข้อความ โดยอิง keyword rule
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    sentences = sent_tokenize(text)
    relations = []

    for sent in sentences:
        # หาใครอยู่ในประโยคนี้บ้าง
        found = [c for c in characters if c in sent]
        if len(found) >= 2:
            # มีตัวละครมากกว่า 1 คนในประโยค
            for rel_type, keywords in RELATION_KEYWORDS.items():
                if any(k in sent for k in keywords):
                    for i in range(len(found)):
                        for j in range(i + 1, len(found)):
                            relation_data = {
                                "character_1": found[i],
                                "relationship": rel_type,
                                "character_2": found[j],
                                "sentence": sent.strip()
                            }
                            relations.append(relation_data)

    return relations


def run_rulebased():
    # โหลดรายชื่อตัวละครจากไฟล์ JSON
    if not os.path.exists(CHARACTER_LIST_PATH):
        raise FileNotFoundError(f"ไม่พบไฟล์ตัวละคร: {CHARACTER_LIST_PATH}")

    with open(CHARACTER_LIST_PATH, "r", encoding="utf-8") as f:
        characters = json.load(f)["characters"]

    # ตรวจโฟลเดอร์ output
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("🔍 เริ่มวิเคราะห์ความสัมพันธ์แบบ Rule-based...\n")

    for file in sorted(os.listdir(INPUT_DIR)):
        if not file.endswith("_cleaned.txt"):
            continue

        file_path = os.path.join(INPUT_DIR, file)
        relations = find_relations_rulebased(file_path, characters)

        # 🔸 กรองความสัมพันธ์ซ้ำ (เล่าปี่–กวนอู vs กวนอู–เล่าปี่)
        unique_relations = []
        seen_pairs = set()
        for rel in relations:
            pair = tuple(sorted([rel["character_1"], rel["character_2"], rel["relationship"]]))
            if pair not in seen_pairs:
                seen_pairs.add(pair)
                unique_relations.append(rel)

        # 🔸 บันทึกผลลัพธ์
        output_path = os.path.join(
            OUTPUT_DIR, file.replace("_cleaned.txt", "_relations_rulebased.json")
        )
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(unique_relations, f, ensure_ascii=False, indent=4)

        print(f"✅ {file}: พบความสัมพันธ์ {len(unique_relations)} รายการ")

    print("\n🎉 วิเคราะห์เสร็จแล้ว! ดูผลในโฟลเดอร์:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    run_rulebased()
