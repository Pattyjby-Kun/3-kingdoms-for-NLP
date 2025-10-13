# src/relationship_ai.py
import json
from pythainlp.tokenize import sent_tokenize
from transformers import pipeline

# โหลดโมเดล WangchanBERTa สำหรับ Zero-shot classification
print("⚙️ กำลังโหลดโมเดล WangchanBERTa...")
pipe = pipeline("zero-shot-classification", model="airesearch/wangchanberta-base-att-spm-uncased")
print("✅ โหลดโมเดลสำเร็จ พร้อมใช้งาน")

def ai_infer_relationship(char1, char2, sentence):
    """
    ใช้ WangchanBERTa วิเคราะห์ความสัมพันธ์ของตัวละคร 2 ตัวในประโยค
    """
    labels = ["พี่น้อง", "ศัตรู", "เจ้านาย-ลูกน้อง", "ไม่มีข้อมูล"]
    hypothesis = f"{char1} และ {char2} มีความสัมพันธ์เป็นแบบ"
    
    result = pipe(sentence, candidate_labels=labels, hypothesis_template=hypothesis)
    relation = result["labels"][0]
    return relation


def find_relations_ai(file_path, character_list_path=r"D:\Trump\data\character_list.json",
                      output_path=r"D:\Trump\output\chapter1_relations_ai.json"):
    """
    อ่านเนื้อหาจากไฟล์ chapter, วิเคราะห์ความสัมพันธ์ แล้วบันทึกเป็น JSON
    """
    # โหลดรายชื่อตัวละคร
    with open(character_list_path, "r", encoding="utf-8") as f:
        characters = json.load(f)["characters"]

    # โหลดเนื้อหา
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    sentences = sent_tokenize(text)
    relations = []

    print("🔍 เริ่มวิเคราะห์ความสัมพันธ์จากเนื้อหา...")

    for sent in sentences:
        found = [c for c in characters if c in sent]
        if len(found) >= 2:
            for i in range(len(found)):
                for j in range(i + 1, len(found)):
                    relation = ai_infer_relationship(found[i], found[j], sent)
                    if relation != "ไม่มีข้อมูล":
                        relations.append({
                            "character_1": found[i],
                            "relationship": relation,
                            "character_2": found[j],
                            "sentence": sent.strip()
                        })
                        print(f"{found[i]} —({relation})→ {found[j]}")

    # บันทึกผลลัพธ์ลงไฟล์ JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(relations, f, ensure_ascii=False, indent=4)

    print(f"\n✅ วิเคราะห์เสร็จแล้ว บันทึกผลที่: {output_path}")
    return relations


if __name__ == "__main__":
    path = r"D:\Trump\data\cleaned\chapter1_cleaned.txt"
    find_relations_ai(path)
