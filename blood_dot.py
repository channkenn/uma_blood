import csv
from graphviz import Digraph

# 関数: CSVファイルから血統データを読み込む
def load_bloodline_from_csv(csv_file):
    bloodlines = []
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            bloodlines.append(row)
    return bloodlines

# 血統図を描画して保存する関数
def create_bloodline_image(child, father, mother):
    # グラフ作成
    dot = Digraph(format="svg")
    dot.attr(rankdir="TB")
    # 日本語フォントを指定（Windows環境の場合はMS ゴシックなど）
    dot.attr(fontname="MS Gothic")

    # ノードとエッジを追加
    dot.node(father, fontname="MS Gothic")  # 父ノード
    dot.node(mother, fontname="MS Gothic")  # 母ノード
    dot.node(child, fontname="MS Gothic")  # 子ノード
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
    create_bloodline_image(child, father, mother)

print("すべての血統図が作成されました。")
