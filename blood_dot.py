import os
import csv
from unidecode import unidecode
from graphviz import Digraph

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
# 血統図を描画して保存する関数（父と母から直接子に矢印が向かう形式）
def create_bloodline_image_with_direct_arrows(child, father, mother):
    # グラフ作成
    dot = Digraph(format="svg")
    dot.attr(rankdir="TB")
    # 日本語フォントを指定（Windows環境の場合はMS ゴシックなど）
    dot.attr(fontname="MS Gothic")

  # 画像をノードに挿入
    imgFather = unidecode(father)
    imgMother = unidecode(mother)
    imgChild = unidecode(child)
    dot.node(father, shape="box", style="filled", color="lightblue", fontname="MS Gothic", image=get_image_path(imgFather), width="0.1", height="0.1")  # 父ノード
    dot.node(mother, shape="box", style="filled", color="lightcoral", fontname="MS Gothic", image=get_image_path(imgMother), width="0.1", height="0.1")  # 母ノード
    dot.node(child, shape="box", image=get_image_path(imgChild), width="0.1", height="0.1")  # 子ノード
    # 父→子、母→子 の矢印を追加
    dot.edge(father, child)  # 父→子
    dot.edge(mother, child)  # 母→子

    # ファイル名を子の名前で保存（拡張子を含めない）
    filename = f"{child}"
    dot.render(filename, cleanup=True)

# CSVファイルのパス
csv_file = "bloodline.csv"

# 血統データを読み込み
bloodlines = load_bloodline_from_csv(csv_file)

# 各行に対して血統図を作成
for row in bloodlines:
    child = row['名前']
    father = row['父']
    mother = row['母']
    create_bloodline_image_with_direct_arrows(child, father, mother)

print("すべての血統図が作成されました。")
