import os
from PIL import Image
from utils import get_img_path

def resize_images(input_subfolder="org", output_subfolder="100px", output_size=(100, 100)):
    """
    指定フォルダ内のPNG画像を指定サイズにリサイズして保存。
    """
    # 入力・出力フォルダのパスを取得
    base_img_dir = get_img_path("")  # imgフォルダの絶対パス
    input_folder = os.path.join(base_img_dir, input_subfolder)
    output_folder = os.path.join(base_img_dir, output_subfolder)

    # 出力フォルダがない場合は作成
    os.makedirs(output_folder, exist_ok=True)

    # フォルダ内のすべてのPNG画像を処理
    count = 0
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 画像を開いてリサイズ
            with Image.open(input_path) as img:
                img_resized = img.resize(output_size, Image.LANCZOS)
                img_resized.save(output_path, "PNG")
                count += 1
                print(f"リサイズ: {filename} -> {output_subfolder}")

    print(f"リサイズ完了！（{count} 件処理）")

if __name__ == "__main__":
    resize_images(output_size=(100, 100))
