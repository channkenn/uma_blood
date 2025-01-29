import os
import csv
from unidecode import unidecode
from graphviz import Digraph

print("Current directory:", os.getcwd())

# 関数: CSVファイルから血統データを読み込む
def load_bloodline_from_csv(csv_file):
    bloodlines = []
    with open(csv_file, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        print("列名:", reader.fieldnames)  # 列名を確認
        if "名前" not in reader.fieldnames or "ウマ娘順" not in reader.fieldnames:
            raise KeyError("CSVファイルに必要な列名が見つかりません。ヘッダーを確認してください。")
        for row in reader:
            if row["名前"].strip() and row["ウマ娘順"].strip().isdigit():
                bloodlines.append(row)
    return bloodlines

# 画像ファイルのパスを確認
def get_image_path(image_name):
    image_path = f"img/{image_name}.png"
    print("image_path:", image_path)
    if not os.path.isfile(image_path):
        return "img/mob.png"
    return image_path

def create_combined_bloodline_image(bloodlines):
    # ウマ娘順でソート（数字でソートするように）
    bloodlines.sort(key=lambda x: int(x["ウマ娘順"]) if x["ウマ娘順"].isdigit() else float("inf"))

    dot = Digraph(format="svg")
    dot.attr(rankdir="TB")  # 縦並びにする
    dot.attr(fontname="MS Gothic")

    # ノードの作成（エッジなし）
    for index, row in enumerate(bloodlines):
        uma_number = row["ウマ娘順"]  # ウマ娘順を取得
        child = row["名前"] if row["名前"] else f"unknown_{index}"
        url = row["サイゲURL"]  # サイゲURLを取得
        dot.node(
            child,
            shape="box",
            image=get_image_path(unidecode(child)),
            width="0.1",
            height="0.1",
            label="",  # テキストラベルを非表示
            URL=url,
        )


# 3 -> 13 -> 23 -> 33 といったエッジから10ずつループを作成
    for start in range(0, 10):
        for i in range(start, len(bloodlines) - 10, 10):
            from_node = bloodlines[i]["名前"]
            to_node = bloodlines[i + 10]["名前"]
            dot.edge(from_node, to_node, style="invis")



    # グラフを保存
    output_path = dot.render("umadice", cleanup=False)
    print(f"SVGファイルが生成されました: {output_path}")


# CSVファイルのパス
csv_file = "bloodline.csv"

# 血統データを読み込み
bloodlines = load_bloodline_from_csv(csv_file)

# 1つの血統図にまとめて作成
create_combined_bloodline_image(bloodlines)

print("すべての血統図が1つのSVGファイルにまとめられました。")
