import os
import json
import networkx as nx
from pyvis.network import Network

INPUT_DIR = r"C:\Homework\3-kingdoms-for-NLP\output\chapter_relations_rulebased"
OUTPUT_PATH = r"C:\Homework\3-kingdoms-for-NLP\output\graphs\3kingdoms_rulebased_final.html"

def build_graph(input_dir):
    G = nx.Graph()
    total_relations = 0

    print("🔗 รวมข้อมูลความสัมพันธ์จากบทที่มีเนื้อหา...")

    for file in sorted(os.listdir(input_dir)):
        path = os.path.join(input_dir, file)
        if not file.endswith(".json"):
            continue

        # ✅ ข้ามไฟล์ที่ขนาดเล็กเกินไป (ไม่มีข้อมูล)
        if os.path.getsize(path) < 50:
            print(f"⚠️ ข้าม {file} (ไฟล์ว่าง)")
            continue

        print(f"📖 โหลด: {file}")
        with open(path, "r", encoding="utf-8") as f:
            relations = json.load(f)

        for rel in relations:
            a = rel.get("character_1")
            b = rel.get("character_2")
            label = rel.get("relationship", "")
            if not a or not b:
                continue

            if G.has_edge(a, b):
                G[a][b]["count"] += 1
            else:
                G.add_edge(a, b, label=label, count=1)
            total_relations += 1

    print(f"✅ โหลดเสร็จ: Node {len(G.nodes())}, Edge {len(G.edges())}, ความสัมพันธ์ {total_relations}")
    return G


def visualize_graph(G, output_path):
    if len(G.nodes()) == 0:
        print("❌ ไม่มีข้อมูลในกราฟเลย ตรวจ JSON อีกครั้ง")
        return

    net = Network(height="900px", width="100%", bgcolor="#ffffff", font_color="#000000", notebook=False)
    net.force_atlas_2based(gravity=-30, central_gravity=0.01, spring_length=150, spring_strength=0.05)

    color_map = {
        "พี่น้อง": "#27ae60",
        "ศัตรู": "#e74c3c",
        "เจ้านาย-ลูกน้อง": "#2980b9",
        "พันธมิตร": "#f39c12"
    }

    for node in G.nodes():
        net.add_node(node, label=node, color="#A7C7E7", size=40, title=f"ตัวละคร: {node}")

    for a, b, data in G.edges(data=True):
        rel = data.get("label", "")
        count = data.get("count", 1)
        color = color_map.get(rel, "#7f8c8d")
        width = 2 + count * 1.2
        net.add_edge(a, b, label=f"{rel} ({count}x)", color=color, width=width)

    net.set_options("""
    var options = {
      "physics": {
        "enabled": true,
        "solver": "forceAtlas2Based",
        "forceAtlas2Based": {
          "gravitationalConstant": -30,
          "centralGravity": 0.01,
          "springLength": 150,
          "springConstant": 0.05
        },
        "minVelocity": 0.75
      },
      "interaction": {
        "hover": true,
        "dragNodes": true,
        "zoomView": true
      },
      "nodes": {
        "font": {"size": 22, "face": "Tahoma"},
        "borderWidth": 2
      },
      "edges": {
        "font": {"size": 18, "align": "middle"},
        "smooth": {"type": "dynamic"}
      }
    }
    """)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    net.save_graph(output_path)
    print(f"🎨 สร้างกราฟเรียบร้อย → {output_path}")


if __name__ == "__main__":
    G = build_graph(INPUT_DIR)
    visualize_graph(G, OUTPUT_PATH)
