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

# 再帰的に血統図を生成する関数
# 再帰的に血統図を生成する関数
def create_individual_bloodline_image(name, bloodlines_dict, dot=None, depth=0, added_edges=None):
    if depth > 20:  # 無限ループ防止（15世代まで）
        return

    row = bloodlines_dict.get(name)
    if not row:
        return

    # データ取得（デフォルト: unknown_XXX）
    child = row['名前'] or "unknown_child"
    father = row['父'] or "unknown_father"
    mother = row['母'] or "unknown_mother"
    father_father = row['父父'] or "unknown_father_father"
    father_mother = row['父母'] or "unknown_father_mother"
    mother_father = row['母父'] or "unknown_mother_father"
    mother_mother = row['母母'] or "unknown_mother_mother"

    # グラフ初期化（最初の呼び出し時のみ）
    if dot is None:
        dot = Digraph(format="svg")
        dot.attr(rankdir="TB")
        dot.attr(fontname="MS Gothic")
        added_edges = set()  # 追加済みエッジを管理するセット

    # ノード追加（子）
    if child != "unknown_child":
        dot.node(child, shape="box", image=get_image_path(unidecode(child)), width="0.1", height="0.1", label=child)

    # ノード追加（親）
    for parent, color in [(father, "lightblue"), (mother, "lightcoral")]:
        if parent not in ["unknown_father", "unknown_mother"]:
            dot.node(parent, shape="box", style="filled", color=color, fontname="MS Gothic",
                     image=get_image_path(unidecode(parent)), width="0.1", height="0.1", label=parent)
            if (parent, child) not in added_edges:  # すでに同じエッジがないか確認
                dot.edge(parent, child)
                added_edges.add((parent, child))

    # ノード追加（祖父母）
    for grandparent, color in [(father_father, "lightblue"), (father_mother, "lightcoral"),
                               (mother_father, "lightblue"), (mother_mother, "lightcoral")]:
        if grandparent not in ["unknown_father_father", "unknown_father_mother", "unknown_mother_father", "unknown_mother_mother"]:
            dot.node(grandparent, shape="box", style="filled", color=color, fontname="MS Gothic",
                     image=get_image_path(unidecode(grandparent)), width="0.1", height="0.1", label=grandparent)
            parent_node = father if grandparent in [father_father, father_mother] else mother
            if (grandparent, parent_node) not in added_edges:  # すでに同じエッジがないか確認
                dot.edge(grandparent, parent_node)
                added_edges.add((grandparent, parent_node))

    # 祖父母が血統辞書に存在するか確認→父父のみを対象にする
    for grandparent in [father_father]:
        if grandparent in bloodlines_dict:
            create_individual_bloodline_image(grandparent, bloodlines_dict, dot, depth + 1, added_edges)

    # 最初の呼び出し時のみSVGを保存
    if depth == 0:
        filename = f"{child}_ff"
        output_path = dot.render(filename, cleanup=True)
        print(f"SVGファイルが生成されました: {output_path}")


# CSV読み込み
csv_file = "bloodline.csv"
bloodlines_dict = load_bloodline_from_csv(csv_file)

# 各行ごとに血統図を作成
for name in bloodlines_dict.keys():
    create_individual_bloodline_image(name, bloodlines_dict)
