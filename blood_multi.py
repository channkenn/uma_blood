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
# 再帰的に血統図を生成する関数（複数の名前を処理できるように変更）
def create_combined_bloodline_image(names, bloodlines_dict):
    dot = Digraph(format="svg")
    dot.attr(rankdir="TB")
    dot.attr(fontname="MS Gothic")
    dot.attr(ranksep="1.5", nodesep="0.1")  # ノード間の間隔を広げる
    dot.attr(bgcolor='transparent')  # 背景を透過に設定
    added_edges = set()  # 追加済みエッジを管理するセット

    # 世代ごとに処理するための辞書
    generations = {}

    def process_individual(name, depth=0):
        if depth > 1:  # 無限ループ防止
            return
        
        row = bloodlines_dict.get(name)
        if not row:
            return

        child = row['名前'] or "unknown_child"
        father = row['父'] or "unknown_father"
        mother = row['母'] or "unknown_mother"
        father_father = row['父父'] or "unknown_father_father"
        father_mother = row['父母'] or "unknown_father_mother"
        mother_father = row['母父'] or "unknown_mother_father"
        mother_mother = row['母母'] or "unknown_mother_mother"
        wikiURL = row['wikiURL'] or "unknown_wiki"

        # ノード追加（子）
        if child != "unknown_child":
            dot.node(child, shape="box", image=get_image_path(unidecode(child)), width="0.1", height="0.1", label=child, URL=wikiURL)

        # 世代ごとに名前をグループ化
        if depth not in generations:
            generations[depth] = []
        generations[depth].append(child)

        # ノード追加（親）
        for parent, color in [(father, "lightblue"), (mother, "lightcoral")]:
            if parent not in ["unknown_father", "unknown_mother"]:
                dot.node(parent, shape="box", style="filled", color=color, fontname="MS Gothic",
                        image=get_image_path(unidecode(parent)), width="0.1", height="0.1", label=parent)
                if (parent, child) not in added_edges:  # すでに同じエッジがないか確認
                    edge_color = color
                    dot.edge(parent, child, color=edge_color, penwidth="5")  # エッジの色と太さを変更
                    added_edges.add((parent, child))

        # ノード追加（父父、父母、母父）
        for grandparent, color in [(father_father, "lightblue"), (father_mother, "lightcoral"),
                                   (mother_father, "lightblue"), (mother_mother, "lightcoral")]:
            if grandparent not in ["unknown_father_father", "unknown_father_mother", "unknown_mother_father", "unknown_mother_mother"]:
                dot.node(grandparent, shape="box", style="filled", color=color, fontname="MS Gothic",
                        image=get_image_path(unidecode(grandparent)), width="0.1", height="0.1", label=grandparent)
                parent_node = father if grandparent in [father_father, father_mother] else mother
                if (grandparent, parent_node) not in added_edges:  # すでに同じエッジがないか確認
                    edge_color = color
                    dot.edge(grandparent, parent_node, color=edge_color, penwidth="5")  # エッジの色と太さを変更
                    added_edges.add((grandparent, parent_node))

        # 祖父母が血統辞書に存在するか確認 -> 父父のみにする
        for grandparent in [father_father, father_mother, mother_father, mother_mother]:
            if grandparent in bloodlines_dict:
                process_individual(grandparent, depth + 1)

    # 各個体を処理
    for name in names:
        process_individual(name)

    # 世代ごとにrank=sameを設定
    for generation in generations.values():
        with dot.subgraph() as s:
            s.attr(rank='same')
            for name in generation:
                s.node(name)

    # SVGファイルを保存
    filename = "_".join(names)
    output_path = dot.render(filename, cleanup=False)
    print(f"SVGファイルが生成されました: {output_path}")


# CSV読み込み
csv_file = "bloodline.csv"
bloodlines_dict = load_bloodline_from_csv(csv_file)

# 複数の名前で血統図を作成
names = [
    "サクラチヨノオー",
    "スーパークリーク",
    "ヤエノムテキ"
    ]
create_combined_bloodline_image(names, bloodlines_dict)
