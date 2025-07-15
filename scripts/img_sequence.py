import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from utils import get_csv_path, get_img_path

def add_order_to_images(csv_name="bloodline.csv", input_folder="100px", output_folder="seq"):
    # フォルダパスを取得
    input_dir = get_img_path(input_folder)  # 入力フォルダ（img/100px）
    output_dir = get_img_path(output_folder)  # 出力フォルダ（img）
    os.makedirs(output_dir, exist_ok=True)

    # CSVデータを読み込み
    csv_path = get_csv_path(csv_name)
    df = pd.read_csv(csv_path, dtype=str).fillna('')  # NaNを空文字に変換

    # "ウマ娘順" 列があるかチェック
    if "ウマ娘順" in df.columns:
        df["ウマ娘順"] = df["ウマ娘順"].astype(str)  # 確実に文字列化
        name_to_order = dict(zip(df["名前"], df["ウマ娘順"]))
    else:
        name_to_order = {}  # 無ければ空辞書

    # フォント設定
    try:
        font = ImageFont.truetype("arial.ttf", 30)  # Windows
    except IOError:
        font = ImageFont.load_default()  # フォントが無ければデフォルト

    # 画像処理
    for name in df["名前"]:
        img_filename = f"{name}.png"
        img_path = os.path.join(input_dir, img_filename)

        if os.path.exists(img_path):  # 画像が存在する場合のみ処理
            img = Image.open(img_path).convert("RGBA")  # RGBAモードで開く

            if name in name_to_order:
                order = name_to_order[name]
                draw = ImageDraw.Draw(img)

                # 矩形のサイズを画像に応じて調整
                box_width = int(img.width * 0.4)
                box_height = int(img.height * 0.3)
                x1, y1 = 0, img.height - box_height  # 左下に配置
                x2, y2 = box_width, img.height

                # 黒背景の矩形を描画
                draw.rectangle([x1, y1, x2, y2], fill="black")

                # 中央揃えのテキスト配置
                bbox = font.getbbox(order)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                text_x = x1 + (box_width - text_width) / 2
                text_y = y1 + (box_height - text_height) / 2 - bbox[1]

                draw.text((text_x, text_y), order, fill="white", font=font)

            # 保存
            output_path = os.path.join(output_dir, img_filename)
            img.save(output_path)
            print(f"✅ {img_filename} 保存済み")

    print("🎉 全ての画像処理が完了しました！")

if __name__ == "__main__":
    add_order_to_images()
