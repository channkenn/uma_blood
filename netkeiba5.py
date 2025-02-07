# -*- coding: utf-8 -*-
import os
import csv
import urllib.parse
from unidecode import unidecode
from graphviz import Digraph
from collections import defaultdict

site_name = "(netkeiba OR wikipedia)"
def generate_google_search_url(horse_name, site_name):
    query = f"{horse_name} {site_name}"
    encoded_query = urllib.parse.quote(query)
    return f"https://www.google.com/search?q={encoded_query}"


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

def process_horse(index_tuple, ancestor_list, processed, data):
    """馬の父母を取得し、データをリストに追加する"""
    name_index, father_index, mother_index = index_tuple

    # インデックスが範囲内であることを確認
    if name_index >= len(ancestor_list) or father_index >= len(ancestor_list) or mother_index >= len(ancestor_list):
        return

    name = ancestor_list[name_index]
    father = ancestor_list[father_index]
    mother = ancestor_list[mother_index]

    # すでに処理した馬ならスキップ
    if name in processed:
        return

    # データ追加
    data.append([name, father, mother])
    processed.add(name)
    
# 再帰的に血統図を生成する関数
def create_combined_bloodline_image(name, bloodlines_dict):
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
        if depth > 4:  # 無限ループ防止
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
        wikiURL = generate_google_search_url(name, site_name)
        
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
                         image=get_image_path(unidecode(parent)), width="0.1", height="0.1", label=parent, URL=generate_google_search_url(parent, site_name))
                
                if (unique_parent, unique_child) not in added_edges:
                    edge_color = color
                    dot.edge(unique_parent, unique_child, color=edge_color, penwidth="5")
                    added_edges.add((unique_parent, unique_child))
                
                if parent in bloodlines_dict:
                    process_individual(unique_child, parent, depth + 1)
    
    process_individual(None, name)

    for generation in generations.values():
        with dot.subgraph() as s:
            s.attr(rank='same')
            for name in generation:
                s.node(name)
    
    filename = os.path.splitext(csv_file)[0]  # CSVファイル名（拡張子なし）
    output_path = dot.render(filename, cleanup=True)
    print(f"SVGファイルが生成されました: {output_path}")

# インデックスセット
index_set = [
    (0, 1, 32), (1, 2, 17), (2, 3, 10), (3, 4, 7), (4, 5, 6),
    (7, 8, 9), (10, 11, 14), (11, 12, 13), (14, 15, 16), (17, 18, 25),
    (18, 19, 22), (19, 20, 21), (22, 23, 24), (25, 26, 29), (26, 27, 28),
    (29, 30, 31), (32, 33, 48), (33, 34, 41), (34, 35, 38), (35, 36, 37),
    (38, 39, 40), (41, 42, 45), (42, 43, 44), (45, 46, 47), (48, 49, 56),
    (49, 50, 53), (50, 51, 52), (53, 54, 55), (56, 57, 60), (57, 58, 59),
    (60, 61, 62),
]

# CSVからデータを読み込む
input_filename = "bloodline_netkeiba5.csv"
first_loop = True  # 最初のループかどうかを判定するフラグ
with open(input_filename, newline='', encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーをスキップ

    for row in reader:
        if len(row) < 2:
            continue  # 不正な行をスキップ
        
        name = row[0]
        ancestor_str = ",".join(row[1:])  # 2列目以降すべてをカンマ区切りで結合
        ancestor_list = (name + "," + ancestor_str).split(",")
        # すでに処理した馬のセット
        processed = set()

        # 結果データ（最初の行にヘッダー）
        data = [["名前", "父", "母"]]
        # 最初のセットを手動で追加
        process_horse(index_set[0], ancestor_list, processed, data)
     
        # 追加の処理
        for index_tuple in index_set[1:]:
            process_horse(index_tuple, ancestor_list, processed, data)
        # 各nameごとにCSVファイルを書き出し
        output_filename = f"{name}.csv"
        with open(output_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)

        # `bloodline_netkeiba5_cfm.csv` の書き出し（最初の回だけ新規作成、それ以降は追記）
        mode = "w" if first_loop else "a"
        cfm_filename = "bloodline_netkeiba5_cfm.csv"
        with open(cfm_filename, mode=mode, newline="", encoding="utf-8") as cfm_file:
            writer = csv.writer(cfm_file)
            if first_loop:
                writer.writerow(["名前", "父", "母"])  # 1回目のみヘッダーを書き出す
                first_loop = False  # 2回目以降は `a` モードにする
            writer.writerows(data[1:])  # 1行目（ヘッダー）を除いて書き出し

        # CSV読み込み
        csv_file = output_filename
        bloodlines_dict = load_bloodline_from_csv(csv_file)

        # 血統図ファイルが既に存在する場合はスキップ
        if not os.path.exists(f"{name}.svg"):
            # **血統図を生成**
            create_combined_bloodline_image(name, bloodlines_dict)
        else:
            print(f"{name}.svg は既に存在するためスキップします。")

