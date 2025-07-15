from collections import defaultdict
from graphviz import Digraph
from unidecode import unidecode
from utils import get_img_path, get_svg_path
import os
import urllib.parse

# 検索URL生成
def generate_google_search_url(horse_name, site_name="(netkeiba OR wikipedia)"):
    query = f"{horse_name} {site_name}"
    encoded_query = urllib.parse.quote(query)
    return f"https://www.google.com/search?q={encoded_query}"

# CSV -> dict変換
def load_bloodline_from_csv(csv_file):
    import csv
    bloodlines_dict = {}
    with open(csv_file, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['名前']:
                bloodlines_dict[row['名前']] = row
    return bloodlines_dict

# 画像パス取得
def get_image_path(image_name):
    if not image_name.endswith(".png"):
        image_name += ".png"
    path = get_img_path(image_name)
    return path if os.path.isfile(path) else get_img_path("mob.png")

# 血統図生成
def create_combined_bloodline_image(names, bloodlines_dict):
    dot = Digraph(format="svg")
    dot.attr(rankdir="TB", fontname="MS Gothic", ranksep="1.5", nodesep="0.1", bgcolor="transparent")
    added_edges = set()

    # 左上固定のラベル
    dot.node("fixed_label", label="左上固定のテキスト", shape="none", pos="-1,0!")

    def process_individual(name, depth=0):
        if depth > 25:  # 無限ループ防止
            return

        row = bloodlines_dict.get(name)
        if not row:
            return

        child = row['名前'] or "unknown_child"
        father = row['父'] or "unknown_father"

        wikiURL = generate_google_search_url(name)

        # 子ノード
        if child not in ["unknown_child", "unknown"]:
            dot.node(child, shape="box", image=get_image_path(unidecode(child)),
                     width="0.1", height="0.1", label=child, URL=wikiURL)

        # 父ノード
        if father not in ["unknown_father", "unknown"]:
            dot.node(father, shape="box", style="filled", color="lightblue", fontname="MS Gothic",
                     image=get_image_path(unidecode(father)),
                     width="0.1", height="0.1", label=father, URL=generate_google_search_url(father))
            if (father, child) not in added_edges:
                dot.edge(father, child, color="lightblue", penwidth="5")
                added_edges.add((father, child))

        # 父親を再帰処理
        if father in bloodlines_dict:
            process_individual(father, depth + 1)

    # 複数個体を処理
    for name in names:
        process_individual(name)

    # 出力先ディレクトリ
    output_file = get_svg_path("uma_blood_netkeiba5_cfm_f")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # SVG生成
    dot.render(output_file, cleanup=True, format="svg")
    print(f"✅ SVG生成完了: {output_file}.svg")