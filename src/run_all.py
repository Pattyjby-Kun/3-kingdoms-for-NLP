import subprocess

# ✅ ลำดับการรัน pipeline
steps = [
    ("ดึงข้อมูลจาก Vajirayana.org", "python vajirayana_scraper.py"),
    ("ทำความสะอาดข้อความ", "python preprocess.py"),
    ("ตรวจหาตัวละคร (NER)", "python ner.py"),
    ("วิเคราะห์ความสัมพันธ์ Rule-based", "python relationship_extraction.py"),
    ("สร้างกราฟความสัมพันธ์", "python graph_rulebased_filter.py"),
]

for name, cmd in steps:
    print(f"\n🚀 ขั้นตอน: {name}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ เกิดข้อผิดพลาดในขั้นตอน: {name}")
        break
else:
    print("\n🎉 ดำเนินการครบทุกขั้นตอนเรียบร้อยแล้ว!")
