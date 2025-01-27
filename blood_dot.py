import os
import csv
from unidecode import unidecode
from graphviz import Digraph

print("Current directory:", os.getcwd())

# 関数: CSVファイルから血統データを読み込む
def load_bloodline_from_csv(csv_file):
    bloodlines = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            bloodlines.append(row)
    return bloodlines

# 画像ファイルのパスを確認
def get_image_path(image_name):
    image_path = f"img/{image_name}.png"
    # 画像ファイルが存在しない場合はデフォルト画像を使用
    if not os.path.isfile(image_path):
        return "img/mob.png"
    return image_path

# 各行ごとに個別の血統図を生成する関数
def create_individual_bloodline_image(row):
    # 子・親・祖父母の情報を取得（デフォルト値: unknown_XXX）
    child = row['名前'] if row['名前'] else "unknown_child"
    father = row['父'] if row['父'] else "unknown_father"
    mother = row['母'] if row['母'] else "unknown_mother"
    father_father = row['父父'] if row['父父'] else "unknown_father_father"
    father_mother = row['父母'] if row['父母'] else "unknown_father_mother"
    mother_father = row['母父'] if row['母父'] else "unknown_mother_father"
    mother_mother = row['母母'] if row['母母'] else "unknown_mother_mother"

    # グラフ作成
    dot = Digraph(format="svg")
    dot.attr(rankdir="TB")  # 矢印を下向きにする
    dot.attr(fontname="MS Gothic")  # 日本語フォントを指定

    # ノードを追加（祖父母も含む）
    dot.node(father, shape="box", style="filled", color="lightblue", fontname="MS Gothic", image=get_image_path(unidecode(father)), width="0.1", height="0.1")
    dot.node(mother, shape="box", style="filled", color="lightcoral", fontname="MS Gothic", image=get_image_path(unidecode(mother)), width="0.1", height="0.1")
    dot.node(child, shape="box", image=get_image_path(unidecode(child)), width="0.1", height="0.1")

    dot.node(father_father, shape="box", style="filled", color="lightblue", fontname="MS Gothic", image=get_image_path(unidecode(father_father)), width="0.1", height="0.1")
    dot.node(father_mother, shape="box", style="filled", color="lightcoral", fontname="MS Gothic", image=get_image_path(unidecode(father_mother)), width="0.1", height="0.1")
    dot.node(mother_father, shape="box", style="filled", color="lightblue", fontname="MS Gothic", image=get_image_path(unidecode(mother_father)), width="0.1", height="0.1")
    dot.node(mother_mother, shape="box", style="filled", color="lightcoral", fontname="MS Gothic", image=get_image_path(unidecode(mother_mother)), width="0.1", height="0.1")

    # エッジを追加（親から子、祖父母から親）
    dot.edge(father, child)
    dot.edge(mother, child)
    dot.edge(father_father, father)
    dot.edge(father_mother, father)
    dot.edge(mother_father, mother)
    dot.edge(mother_mother, mother)

    # SVGファイルに保存（名前をファイル名に使用）
    filename = f"{child}"
    output_path = dot.render(filename, cleanup=False)
    output_path = dot.render(filename, cleanup=False)
    print(f"SVGファイルが生成されました: {output_path}")

# CSVファイルのパス
csv_file = "bloodline.csv"

# 血統データを読み込み
bloodlines = load_bloodline_from_csv(csv_file)

# 各行ごとに血統図を作成
for row in bloodlines:
    create_individual_bloodline_image(row)

print("すべての血統図が個別のSVGファイルとして作成されました。")
