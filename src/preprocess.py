import re
import os
import string

def clean_text(file_path: str) -> str:
    """
    อ่านไฟล์ข้อความ แล้วทำความสะอาดให้อยู่ในรูปแบบที่ NLP ใช้ได้ง่าย
    - ลบเลขหน้า / เครื่องหมายพิเศษ
    - ลบช่องว่างซ้ำ
    - รวมบรรทัดให้ต่อกันเป็นข้อความเดียว
    """

    # 🔹 อ่านไฟล์ข้อความ
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 🔹 ลบเลขไทยและเลขอารบิก
    text = re.sub(r"[0-9๐๑๒๓๔๕๖๗๘๙]+", " ", text)

    # 🔹 ลบเครื่องหมายอัญประกาศและสัญลักษณ์พิเศษ
    text = re.sub(r"[“”\"'()\[\]{}<>]", "", text)
    text = re.sub(r"[•\*\-–—_~^]", " ", text)

    # 🔹 ลบวรรคตอนภาษาอังกฤษทั่วไป
    text = text.translate(str.maketrans("", "", string.punctuation))

    # 🔹 ลบช่องว่างเกินและบรรทัดว่าง
    text = re.sub(r"\s+", " ", text).strip()

    # 🔹 แปลง … ให้เป็นจุดเดียว (บางบทมีจุดไข่ปลา)
    text = text.replace("…", ".")

    return text


def preprocess_all(input_dir: str, output_dir: str):
    """
    ทำความสะอาดทุกไฟล์ในโฟลเดอร์ input_dir แล้วบันทึกผลลัพธ์ไว้ใน output_dir
    """
    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]

    if not files:
        print("⚠️ ไม่พบไฟล์ .txt ในโฟลเดอร์ chapters")
        return

    for filename in files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename.replace(".txt", "_cleaned.txt"))

        try:
            cleaned = clean_text(input_path)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned)
            print(f"✅ cleaned: {filename} → {os.path.basename(output_path)}")
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดกับไฟล์ {filename}: {e}")

    print("\n🎉 ทำความสะอาดข้อความทุกบทเรียบร้อยแล้ว!")


# 🧪 ใช้งานโดยตรง
if __name__ == "__main__":
    input_dir = r"..\data\chapters"
    output_dir = r"..\cleaned"
    preprocess_all(input_dir, output_dir)
