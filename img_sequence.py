import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

# フォルダ設定
input_folder = "imgorg"  # 入力画像のフォルダ
output_folder = "img"  # 出力画像のフォルダ
csv_file = "bloodline.csv"  # CSVファイル名

# フォルダがなければ作成
os.makedirs(output_folder, exist_ok=True)

# CSVデータを読み込む
df = pd.read_csv(csv_file, dtype=str)  # 文字列として読み込む
name_to_order = dict(zip(df["名前"], df["ウマ娘順"]))  # 名前 → ウマ娘順 の辞書

# フォント設定（適宜パスを指定）
try:
    font = ImageFont.truetype("arial.ttf", 30)  # Windows向け
except IOError:
    font = ImageFont.load_default()  # フォントがない場合の代替

# 画像の処理
for name, order in name_to_order.items():
    img_filename = f"{name}.png"  # ファイル名（例: スペシャルウィーク.png）
    img_path = os.path.join(input_folder, img_filename)

    if os.path.exists(img_path):  # 画像が存在する場合のみ処理
        img = Image.open(img_path).convert("RGBA")  # RGBA モードで開く
        draw = ImageDraw.Draw(img)

        # 四角の座標
        box_width = 80
        box_height = 50
        x1, y1 = 0, img.height - box_height  # 左下に配置
        x2, y2 = box_width, img.height

        # 黒背景の四角を描画
        draw.rectangle([x1, y1, x2, y2], fill="black")

        # 中央揃えのための計算
        bbox = font.getbbox(order)  # (left, top, right, bottom)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        text_x = x1 + (box_width - text_width) / 2  # 横中央
        text_y = y1 + (box_height - text_height) / 2 - bbox[1]  # 縦中央（基準線補正）

        draw.text((text_x, text_y), order, fill="white", font=font)

        # 保存
        output_path = os.path.join(output_folder, img_filename)
        img.save(output_path)

print("処理完了！")
