from collections import defaultdict
from graphviz import Digraph
from utils import get_img_path, get_svg_path, to_romaji
import os
import urllib.parse
from unidecode import unidecode


# GitHub Pages のベースURL
GITHUB_BASE_URL = "https://channkenn.github.io/uma_blood/"

# Google検索URL生成
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

# 🟢 GitHubリンク付き血統図生成
def create_combined_bloodline_image(names, bloodlines_dict):
    dot = Digraph(format="svg")
    dot.attr(rankdir="TB", fontname="MS Gothic", ranksep="1.5", nodesep="0.1", bgcolor="transparent")
    added_edges = set()

    # 左上固定ラベル 仮置き
    dot.node("fixed_label", label="左上固定のテキスト", shape="none", pos="-1,0!")
    
    def process_individual(name, depth=0):
        if depth > 25:  # 無限ループ防止
            return

        row = bloodlines_dict.get(name)
        if not row:
            return

        child = row['名前'] or "unknown_child"
        father = row['父'] or "unknown_father"

        # GitHub Pages のURL（日本語名のまま）
        child_url = f"{GITHUB_BASE_URL}svg/{child}.svg"
        father_url = f"{GITHUB_BASE_URL}svg/{father}.svg"

        # 子ノード
        if child not in ["unknown_child", "unknown"]:
            dot.node(
                child,
                shape="box",
                image=get_image_path(to_romaji(child)),
                width="0.1",
                height="0.1",
                label=child,
                URL=child_url
            )

        # 父ノード
        if father not in ["unknown_father", "unknown"]:
            dot.node(
                father,
                shape="box",
                style="filled",
                color="lightblue",
                fontname="MS Gothic",
                image=get_image_path(to_romaji(father)),
                width="0.1",
                height="0.1",
                label=father,
                URL=father_url
            )
            if (father, child) not in added_edges:
                dot.edge(father, child, color="lightblue", penwidth="5")
                added_edges.add((father, child))

        if father in bloodlines_dict:
            process_individual(father, depth + 1)

    for name in names:
        process_individual(name)

    output_file = get_svg_path("uma_blood_netkeiba5_cfm_f")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    dot.render(output_file, cleanup=True, format="svg")
    print(f"✅ GitHubリンク付きSVG生成: {output_file}.svg")
    # fixed_label書き換え
    update_fixed_label_in_svg(output_file + ".svg")

# 🟣 Google検索リンク付き血統図生成
# 🆕 Google検索リンク版
def create_combined_bloodline_image_google(name, bloodlines_dict):
    dot = Digraph(format="svg")
    dot.attr(rankdir="TB")
    dot.attr(fontname="MS Gothic")
    dot.attr(ranksep="2.5", nodesep="0.1")
    dot.attr(bgcolor="transparent")  # 背景透明

    added_edges = set()
    node_counter = defaultdict(int)
    unique_nodes = {}
    generations = defaultdict(list)  # 世代ごとのノード

    def process_individual(child, name, depth=0):
        if depth > 4:  # 5代まで表示
            return

        row = bloodlines_dict.get(name)
        if not row:
            return

        # ユニークID生成
        if (child, name, depth) not in unique_nodes:
            node_counter[name] += 1
            unique_id = f"{name}_{depth}_{node_counter[name]}"
            unique_nodes[(child, name, depth)] = unique_id
        else:
            unique_id = unique_nodes[(child, name, depth)]

        # ノード追加
        dot.node(unique_id,
                 shape="box",
                 image=get_image_path(unidecode(name)),
                 width="0.1", height="0.1",
                 label=name,
                 URL=generate_google_search_url(name))

        generations[depth].append(unique_id)

        father = row['父'] or "unknown_father"
        mother = row['母'] or "unknown_mother"

        for parent, color in [(father, "lightblue"), (mother, "lightcoral")]:
            if parent not in ["unknown_father", "unknown_mother"]:
                # 親ノードのユニークID
                if (unique_id, parent, depth+1) not in unique_nodes:
                    node_counter[parent] += 1
                    parent_id = f"{parent}_{depth+1}_{node_counter[parent]}"
                    unique_nodes[(unique_id, parent, depth+1)] = parent_id
                else:
                    parent_id = unique_nodes[(unique_id, parent, depth+1)]

                # 親ノード追加
                dot.node(parent_id,
                         shape="box",
                         style="filled",
                         color=color,
                         fontname="MS Gothic",
                         image=get_image_path(unidecode(parent)),
                         width="0.1", height="0.1",
                         label=parent,
                         URL=generate_google_search_url(parent))

                # エッジ追加
                if (parent_id, unique_id) not in added_edges:
                    dot.edge(parent_id, unique_id, color=color, penwidth="5")
                    added_edges.add((parent_id, unique_id))

                # 再帰
                if parent in bloodlines_dict:
                    process_individual(unique_id, parent, depth+1)

    # 処理開始
    process_individual(None, name)

    # 世代ごとに rank=same で整列
    for generation in generations.values():
        with dot.subgraph() as s:
            s.attr(rank="same")
            for node in generation:
                s.node(node)

    # 出力ディレクトリ
    output_dir = os.path.join(os.getcwd(), "svg")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, name)
    final_output_path = dot.render(output_file, cleanup=True, format="svg")
    print(f"✅ SVG生成完了: {final_output_path}")

def update_fixed_label_in_svg(svg_path):
    """
    SVGのfixed_label部分を書き換える
    """
    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()

    # fixed_labelノード部分を書き換え
    new_label = '''
    <!-- fixed_label -->
    <g id="node1" class="node">
    <title>fixed_label</title>
    <text text-anchor="middle" x="2000.12" y="-4700.32" font-family="Times New Roman,serif" font-size="144.00">
        <tspan x="2000.12" dy="0">あにまん掲示板 ウマカテ用 サイアーライン図</tspan>
        <tspan x="2000.12" dy="180">非常に大きな画像です(SVGファイル)</tspan>
        <tspan x="2000.12" dy="180">右や下にスクロールしてください</tspan>
        <tspan x="2000.12" dy="180">ノードをクリックすると個別の5代血統図へジャンプします</tspan>
    </text></g>
    '''

    # <title>fixed_label</title> を含む <g>...</g> を置換
    import re
    content, count = re.subn(
        r'<g id="node\d+" class="node">\s*<title>fixed_label</title>.*?</g>',
        new_label.strip(),
        content,
        flags=re.DOTALL
    )

    if count == 0:
        print("⚠ fixed_label が見つかりませんでした")
    else:
        print("✅ fixed_label を書き換えました")

    # 上書き保存
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(content)

def process_horse(index_tuple, ancestor_list, processed, data):
    """馬の父母を取得し、データをリストに追加する"""
    name_index, father_index, mother_index = index_tuple

    if name_index >= len(ancestor_list) or father_index >= len(ancestor_list) or mother_index >= len(ancestor_list):
        return

    name = ancestor_list[name_index]
    father = ancestor_list[father_index]
    mother = ancestor_list[mother_index]

    if name in processed:
        return

    data.append([name, father, mother])
    processed.add(name)