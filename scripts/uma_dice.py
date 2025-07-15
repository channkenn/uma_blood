import os
import csv
from unidecode import unidecode
from graphviz import Digraph
from utils import get_csv_path, get_img_path

def load_bloodline_from_csv(csv_file):
    bloodlines = []
    with open(csv_file, mode="r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        print("列名:", reader.fieldnames)  # 列名確認
        if "名前" not in reader.fieldnames or "ウマ娘順" not in reader.fieldnames:
            raise KeyError("CSVファイルに必要な列名がありません。ヘッダーを確認してください。")
        for row in reader:
            if row["名前"].strip() and row["ウマ娘順"].strip().isdigit():
                bloodlines.append(row)
    return bloodlines

def get_image_path(image_name):
    # utilsの関数に合わせて絶対パス取得
    image_path = get_img_path(f"{image_name}.png")
    if not os.path.isfile(image_path):
        return get_img_path("mob.png")
    return image_path

def create_combined_bloodline_image(bloodlines):
    # ウマ娘順で数字ソート
    bloodlines.sort(key=lambda x: int(x["ウマ娘順"]) if x["ウマ娘順"].isdigit() else float("inf"))

    dot = Digraph(format="svg")
    dot.attr(rankdir="TB")  # 縦並び
    dot.attr(fontname="MS Gothic")

    # ノードを作成（ラベルは非表示、画像のみ表示）
    for index, row in enumerate(bloodlines):
        uma_number = row["ウマ娘順"]
        child = row["名前"] if row["名前"] else f"unknown_{index}"
        url = row.get("サイゲURL", "")  # URLがなければ空文字
        dot.node(
            child,
            shape="box",
            image=get_image_path(unidecode(child)),
            width="0.1",
            height="0.1",
            label="",  # テキストラベルを非表示
            URL=url,
        )

    # 10ずつスキップしながらinvisエッジを追加（レイアウト調整用）
    for start in range(0, 10):
        for i in range(start, len(bloodlines) - 10, 10):
            from_node = bloodlines[i]["名前"]
            to_node = bloodlines[i + 10]["名前"]
            dot.edge(from_node, to_node, style="invis")

    # svgフォルダに出力
    output_dir = os.path.join(os.getcwd(), "svg")
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, "umadice")
    output_path = dot.render(filename, cleanup=False)
    print(f"SVGファイルが生成されました: {output_path}")

if __name__ == "__main__":
    csv_file = get_csv_path("bloodline.csv")
    bloodlines = load_bloodline_from_csv(csv_file)
    create_combined_bloodline_image(bloodlines)
    print("すべての血統図が1つのSVGファイルにまとめられました。")
