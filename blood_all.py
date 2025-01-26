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

# すべての血統図を1つのSVGファイルにまとめる関数
def create_combined_bloodline_image(bloodlines):
    dot = Digraph(format="svg")
    dot.attr(rankdir="TB")  # 上から下に変更
    dot.attr(fontname="MS Gothic")

    for row in bloodlines:
        child = row['名前'] if row['名前'] else "unknown_child"
        father = row['父'] if row['父'] else "unknown_father"
        mother = row['母'] if row['母'] else "unknown_mother"
        
        # ノード追加
        imgFather = unidecode(father)
        imgMother = unidecode(mother)
        imgChild = unidecode(child)
        
        dot.node(father, shape="box", style="filled", color="lightblue", fontname="MS Gothic", image=get_image_path(imgFather), width="0.1", height="0.1")
        dot.node(mother, shape="box", style="filled", color="lightcoral", fontname="MS Gothic", image=get_image_path(imgMother), width="0.1", height="0.1")
        dot.node(child, shape="box", image=get_image_path(imgChild), width="0.1", height="0.1")
        
        # エッジ追加
        dot.edge(father, child)
        dot.edge(mother, child)
    
    output_path = dot.render("combined_bloodline", cleanup=False)
    print(f"SVGファイルが生成されました: {output_path}")




# CSVファイルのパス
csv_file = "bloodline.csv"

# 血統データを読み込み
bloodlines = load_bloodline_from_csv(csv_file)

# 1つの血統図にまとめて作成
create_combined_bloodline_image(bloodlines)

print("すべての血統図が1つのSVGファイルにまとめられました。")
