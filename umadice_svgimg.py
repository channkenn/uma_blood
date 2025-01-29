import os
import csv
import base64
from unidecode import unidecode
from graphviz import Digraph

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

# 画像をBase64エンコードして取得する関数
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        # 画像をバイナリモードで開いてBase64エンコードする
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
    return encoded_string

# 画像ファイルのパスを取得し、Base64エンコードされたデータを生成
def get_image_base64(image_name):
    image_path = f"img/{image_name}.png"
    print("image_path:", image_path)
    if not os.path.isfile(image_path):
        return None  # 画像が見つからない場合
    return encode_image_to_base64(image_path)

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
        image_base64 = get_image_base64(unidecode(child))  # Base64エンコードされた画像データを取得

        if image_base64:
            # Base64データを埋め込んだ形でノードを作成
            dot.node(
                child,
                shape="box",
                width="0.1",
                height="0.1",
                label="",  # テキストラベルを非表示
                image=f"data:image/png;base64,{image_base64}",  # Base64データを埋め込む
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
