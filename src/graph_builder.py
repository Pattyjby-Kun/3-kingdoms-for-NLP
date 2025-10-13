# src/graph_builder.py
import networkx as nx
from pyvis.network import Network
from relationship_extraction import find_relations
import os

def build_graph(relations):
    """
    รับ list ของความสัมพันธ์ แล้วสร้างกราฟเชื่อมโยงด้วย NetworkX
    """
    G = nx.Graph()
    for a, rel, b in relations:
        G.add_node(a)
        G.add_node(b)
        G.add_edge(a, b, label=rel)
    return G


def show_interactive_graph(G, output_path="../output/graphs/relationship_graph.html"):
    """
    แสดงกราฟแบบ interactive ด้วย PyVis
    """
    # สร้าง Network ของ PyVis
    net = Network(height="700px", width="100%", bgcolor="#ffffff", font_color="#000000", directed=False)

    # สีตามประเภทความสัมพันธ์
    color_map = {
        "พี่น้อง": "green",
        "ศัตรู": "red",
        "เจ้านาย-ลูกน้อง": "blue"
    }

    # วนเพิ่ม node และ edge จาก NetworkX
    for node in G.nodes():
        net.add_node(node, label=node, color="#A7C7E7", title=f"ตัวละคร: {node}")

    for a, b, data in G.edges(data=True):
        relation = data.get("label", "")
        color = color_map.get(relation, "gray")
        net.add_edge(a, b, label=relation, color=color, width=3)

    # layout แบบแรงดึงดูด (ดูเป็นธรรมชาติ)
    net.repulsion(node_distance=200, central_gravity=0.2, spring_length=150, spring_strength=0.05)

    # สร้างโฟลเดอร์ output ถ้ายังไม่มี
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # บันทึกกราฟเป็น HTML
    net.save_graph(output_path)
    print(f"✅ สร้างกราฟแบบ Interactive แล้วที่: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    # โหลดความสัมพันธ์จากบท
    path = "../data/cleaned/chapter1_cleaned.txt"
    relations = find_relations(path)

    # สร้างกราฟ NetworkX
    G = build_graph(relations)

    # แสดงผลแบบ interactive
    show_interactive_graph(G)
