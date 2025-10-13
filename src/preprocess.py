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

    # 🔹 ลบเลขหน้า / หมายเลขบรรทัด / เครื่องหมายที่ไม่จำเป็น
    text = re.sub(r"\d+", " ", text)               # ลบตัวเลข
    text = re.sub(r"[“”\"'()\[\]{}]", "", text)    # ลบเครื่องหมายอัญประกาศ
    text = re.sub(r"[•\*\-–—_]", " ", text)        # ลบ bullet หรือ dash

    # 🔹 ลบช่องว่างเกินและบรรทัดว่าง
    text = re.sub(r"\s+", " ", text)               # ให้เหลือช่องว่างเดียว
    text = text.strip()                            # ตัดช่องว่างหัวท้าย

    # 🔹 แปลงเครื่องหมายวรรคตอนให้เป็นรูปแบบเดียวกัน (ถ้าจำเป็น)
    text = text.translate(str.maketrans("", "", string.punctuation))

    return text


def split_sentences(text: str) -> list:
    """
    แยกประโยคแบบง่าย ๆ สำหรับภาษาไทย
    ใช้เมื่อเราต้องการวิเคราะห์ทีละประโยค เช่นตอนหาความสัมพันธ์
    """
    # แยกด้วย "。" หรือ "!" หรือ "?" หรือ " " ที่จบด้วยคำพูด
    sentences = re.split(r"[.!?]|[ ](?=[A-Zก-๙])", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences


# 🧪 ตัวอย่างการใช้งาน (ทดสอบเฉพาะตอนรันไฟล์นี้โดยตรง)

if __name__ == "__main__":
    path = r"D:\Trump\data\chapters\chapter1.txt"
    cleaned = clean_text(path)

    os.makedirs(r"D:\Trump\data\cleaned", exist_ok=True)
    cleaned_path = r"D:\Trump\data\cleaned\chapter1_cleaned.txt"

    with open(cleaned_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"✅ บันทึกไฟล์ cleaned แล้วที่: {cleaned_path}")
