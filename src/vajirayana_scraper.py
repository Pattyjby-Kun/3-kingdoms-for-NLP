# src/vajirayana_scraper.py
import requests
from bs4 import BeautifulSoup
import os
import time

OUTPUT_DIR = r"..\data\chapters"
BASE_URL = "https://vajirayana.org/สามก๊ก/ตอนที่-{}"

def to_thai_num(num: int) -> str:
    """แปลงเลขอารบิก (1,2,3) → เลขไทย (๑,๒,๓)"""
    arabic = "0123456789"
    thai = "๐๑๒๓๔๕๖๗๘๙"
    return "".join(thai[arabic.index(ch)] for ch in str(num))


def scrape_chapter(chapter_num: int):
    """ดึงเนื้อหาจาก Vajirayana.org ตามหมายเลขตอน แล้วบันทึกเป็นไฟล์ข้อความ .txt"""
    thai_num = to_thai_num(chapter_num)
    url = BASE_URL.format(thai_num)
    print(f"📖 กำลังดึง: {url}")

    try:
        response = requests.get(url)
        response.encoding = "utf-8"

        if response.status_code != 200:
            print(f"❌ ไม่สามารถเข้าถึงตอนที่ {chapter_num} (รหัส {response.status_code})")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        # ชื่อบท
        title_tag = soup.find("h1", class_="title")
        title = title_tag.get_text(strip=True) if title_tag else f"ตอนที่ {chapter_num}"

        # เนื้อหา
        content_div = soup.find("div", class_="field-item")
        if not content_div:
            content_div = soup.find("div", class_="node-content")

        if not content_div:
            print(f"⚠️ ไม่พบเนื้อหาของตอนที่ {chapter_num}")
            return

        paragraphs = content_div.find_all("p")
        if paragraphs:
            text = "\n".join([p.get_text(strip=True) for p in paragraphs])
        else:
            text = content_div.get_text(separator="\n", strip=True)

        # บันทึกไฟล์
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        file_path = os.path.join(OUTPUT_DIR, f"chapter{chapter_num}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(title + "\n\n" + text)

        print(f"✅ บันทึกตอนที่ {chapter_num} สำเร็จ → {file_path}")

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดตอนที่ {chapter_num}: {e}")

    time.sleep(1)


if __name__ == "__main__":
    start_chapter = 1
    end_chapter = 5  # 🔸 ทดสอบก่อน 5 ตอน
    print(f"🚀 เริ่มดึงข้อมูลสามก๊ก ตอนที่ {start_chapter} ถึง {end_chapter} จาก Vajirayana.org\n")
    for i in range(start_chapter, end_chapter + 1):
        scrape_chapter(i)
    print("\n🎉 เสร็จสิ้นการดึงข้อมูลทั้งหมด!")
