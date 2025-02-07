import os
import csv
from unidecode import unidecode
from graphviz import Digraph
from collections import defaultdict

# CSVデータを辞書に変換
def load_bloodline_from_csv(csv_file):
    bloodlines_dict = {}
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['名前']:  # 名前が空でない場合のみ追加
                bloodlines_dict[row['名前']] = row
    return bloodlines_dict

# 画像のパス取得
def get_image_path(image_name):
    image_path = f"img/{image_name}.png"
    return image_path if os.path.isfile(image_path) else "img/mob.png"

# 再帰的に血統図を生成する関数
def create_combined_bloodline_image(names, bloodlines_dict):
    dot = Digraph(format="svg")
    dot.attr(rankdir="TB")
    dot.attr(fontname="MS Gothic")
    dot.attr(ranksep="2.5", nodesep="0.1")  # ノード間の間隔を広げる
    dot.attr(bgcolor='transparent')  # 背景を透過に設定
    
    added_edges = set()  # 追加済みエッジを管理するセット
    node_counter = defaultdict(int)  # 各馬の出現回数を記録
    unique_nodes = {}  # 各馬のユニークIDを管理
    generations = {}  # 世代ごとのノード管理

    def process_individual(child, name, depth=0):
        if depth > 8:  # 無限ループ防止
            return
        
        row = bloodlines_dict.get(name)
        if not row:
            return
        
        if (child, name, depth) not in unique_nodes:
            node_counter[name] += 1
            unique_nodes[(child, name, depth)] = f"{name}_{depth}_{node_counter[name]}"
        
        unique_child = unique_nodes[(child, name, depth)]
        father = row['父'] or "unknown_father"
        mother = row['母'] or "unknown_mother"
        wikiURL = "unknown_wiki"
        
        # ノード追加（子）
        dot.node(unique_child, shape="box", image=get_image_path(unidecode(name)),
                 width="0.1", height="0.1", label=name, URL=wikiURL)

        if depth not in generations:
            generations[depth] = []
        generations[depth].append(unique_child)

        # ノード追加（親）
        for parent, color in [(father, "lightblue"), (mother, "lightcoral")]:
            if (parent not in ["unknown_father", "unknown_mother"] or (parent == "unknown_father" and not row['父']) or (parent == "unknown_mother" and not row['母'])):
                if (unique_child, parent, depth+1) not in unique_nodes:
                    node_counter[parent] += 1
                    unique_nodes[(unique_child, parent, depth+1)] = f"{parent}_{depth+1}_{node_counter[parent]}"
                unique_parent = unique_nodes[(unique_child, parent, depth+1)]
                
                dot.node(unique_parent, shape="box", style="filled", color=color, fontname="MS Gothic",
                         image=get_image_path(unidecode(parent)), width="0.1", height="0.1", label=parent)
                
                if (unique_parent, unique_child) not in added_edges:
                    edge_color = color
                    dot.edge(unique_parent, unique_child, color=edge_color, penwidth="5")
                    added_edges.add((unique_parent, unique_child))
                
                if parent in bloodlines_dict:
                    process_individual(unique_child, parent, depth + 1)

    for name in names:
        process_individual(None, name)

    for generation in generations.values():
        with dot.subgraph() as s:
            s.attr(rank='same')
            for name in generation:
                s.node(name)
    
    filename = "_".join(names)
    output_path = dot.render(filename, cleanup=False)
    print(f"SVGファイルが生成されました: {output_path}")

# CSV読み込み
name = "マルゼンスキー"
#csv_file = f"{name}.csv"
csv_file = "bloodline_netkeiba5_cfm.csv"
bloodlines_dict = load_bloodline_from_csv(csv_file)

# 血統図を作成
names = [name]
create_combined_bloodline_image(names, bloodlines_dict)
