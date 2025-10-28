import os
import json
import networkx as nx
from pyvis.network import Network

INPUT_DIR = r"..\output\chapter_relations_rulebased"
OUTPUT_PATH = r"..\output\graphs\3kingdoms_rulebased_filter.html"

def build_graph(input_dir):
    G = nx.Graph()
    for file in os.listdir(input_dir):
        if file.endswith(".json") and os.path.getsize(os.path.join(input_dir, file)) > 50:
            path = os.path.join(input_dir, file)
            with open(path, "r", encoding="utf-8") as f:
                relations = json.load(f)
            for rel in relations:
                a, b = rel.get("character_1"), rel.get("character_2")
                label = rel.get("relationship", "")
                if not a or not b:
                    continue
                if G.has_edge(a, b):
                    G[a][b]["count"] += 1
                else:
                    G.add_edge(a, b, label=label, count=1)
    return G

def create_filtered_graph(G, output_path):
    net = Network(height="900px", width="100%", bgcolor="#ffffff", font_color="#000000", directed=False)
    net.force_atlas_2based(gravity=-35, central_gravity=0.01, spring_length=150, spring_strength=0.05)

    color_map = {
        "พี่น้อง": "#27ae60",
        "ศัตรู": "#e74c3c",
        "เจ้านาย-ลูกน้อง": "#2980b9",
        "พันธมิตร": "#f39c12"
    }

    for node in G.nodes():
        net.add_node(node, label=node, color="#A7C7E7", size=40)

    for a, b, data in G.edges(data=True):
        rel = data.get("label", "")
        count = data.get("count", 1)
        color = color_map.get(rel, "#7f8c8d")
        width = 2 + count
        # ✅ เก็บประเภทความสัมพันธ์ใน edge เพื่อใช้ JS filter
        net.add_edge(a, b, label=f"{rel} ({count}x)", color=color, width=width, title=rel, rel_type=rel)

    # ✅ JS filter menu (ทำงานจริง)
    filter_script = """
    <script type="text/javascript">
      function filterEdges() {
        const selected = Array.from(document.querySelectorAll('input[name="rel_filter"]:checked')).map(cb => cb.value);
        network.body.data.edges.update(
          network.body.data.edges.map(edge => {
            const show = selected.includes(edge.rel_type);
            return { id: edge.id, hidden: !show };
          })
        );
      }
    </script>
    <div style="padding:10px;font-family:tahoma;">
      <b>🔍 กรองประเภทความสัมพันธ์:</b><br>
      <label><input type="checkbox" name="rel_filter" value="พันธมิตร" checked onchange="filterEdges()"> พันธมิตร</label>
      <label><input type="checkbox" name="rel_filter" value="พี่น้อง" checked onchange="filterEdges()"> พี่น้อง</label>
      <label><input type="checkbox" name="rel_filter" value="ศัตรู" checked onchange="filterEdges()"> ศัตรู</label>
      <label><input type="checkbox" name="rel_filter" value="เจ้านาย-ลูกน้อง" checked onchange="filterEdges()"> เจ้านาย-ลูกน้อง</label>
    </div>
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    net.save_graph(output_path)

    # ✅ แทรก filter menu เข้าไฟล์ HTML
    with open(output_path, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("<body>", f"<body>{filter_script}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"🎨 กราฟพร้อม Filter ถูกบันทึกที่: {output_path}")

if __name__ == "__main__":
    print("🔗 สร้างกราฟ + เพิ่มระบบกรองประเภทความสัมพันธ์...")
    G = build_graph(INPUT_DIR)
    create_filtered_graph(G, OUTPUT_PATH)
