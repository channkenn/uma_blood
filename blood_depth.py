import os
import csv
from unidecode import unidecode
from graphviz import Digraph

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

# 再帰的に血統図を生成する関数（複数の名前を処理できるように変更）
# 再帰的に血統図を生成する関数（修正版）
def create_combined_bloodline_image(names, bloodlines_dict):
    dot = Digraph(format="svg")
    dot.attr(rankdir="TB")
    dot.attr(fontname="MS Gothic")
    dot.attr(ranksep="2.5", nodesep="0.1")  # ノード間の間隔を広げる
    dot.attr(bgcolor='transparent')  # 背景を透過に設定
    added_edges = set()  # 追加済みエッジを管理するセット

    generations = {}  # 世代ごとのノード管理

    def process_individual(name, depth=0):
        if depth > 3:  # 無限ループ防止
            return

        row = bloodlines_dict.get(name)
        if not row:
            return

        # ノードIDをユニークにする（Graphviz用のIDを変更）
        child_id = f"{name}_{depth}"
        father_id = f"{row['父']}_{depth+1}" if row['父'] else "unknown_father"
        mother_id = f"{row['母']}_{depth+1}" if row['母'] else "unknown_mother"

        # ノード追加（子）
        dot.node(child_id, shape="box", image=get_image_path(unidecode(name)), width="0.1", height="0.1", 
                 label=name, URL=row['wikiURL'] if 'wikiURL' in row else "")

        # 世代ごとに名前をグループ化
        if depth not in generations:
            generations[depth] = []
        generations[depth].append(child_id)

        # ノード追加（親）
        for parent, parent_id, color in [(row['父'], father_id, "lightblue"), (row['母'], mother_id, "lightcoral")]:
            if parent:
                dot.node(parent_id, shape="box", style="filled", color=color, fontname="MS Gothic",
                         image=get_image_path(unidecode(parent)), width="0.1", height="0.1", label=parent)
                if (parent_id, child_id) not in added_edges:  # すでに同じエッジがないか確認
                    dot.edge(parent_id, child_id, color=color, penwidth="5")
                    added_edges.add((parent_id, child_id))

        # 再帰的に親を処理（新しいIDを渡す）
        for parent, parent_id in [(row['父'], father_id), (row['母'], mother_id)]:
            if parent in bloodlines_dict:
                process_individual(parent, depth + 1)

    # 各個体を処理
    for name in names:
        process_individual(name)

    # 世代ごとに rank=same を設定
    for generation in generations.values():
        with dot.subgraph() as s:
            s.attr(rank='same')
            for name in generation:
                s.node(name)

    # SVGファイルを保存
    filename = "_".join(names)
    output_path = dot.render(filename, cleanup=True)
    print(f"SVGファイルが生成されました: {output_path}")

# CSV読み込み
csv_file = "bloodline.csv"
bloodlines_dict = load_bloodline_from_csv(csv_file)

# 複数の名前で血統図を作成
names = [
    "デアリングタクト"
    ]
create_combined_bloodline_image(names, bloodlines_dict)
