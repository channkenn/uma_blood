import os
import shutil
from utils import get_img_path, to_romaji  # ✅ 共通関数をインポート

def rename_images_in_folder(input_subfolder="seq", output_subfolder=""):
    """
    input_folder の画像をローマ字名にリネームして output_folder にコピー
    """
    # 入力・出力フォルダの絶対パスを取得
    base_img_dir = os.path.dirname(get_img_path(""))  # imgフォルダ
    input_folder = os.path.join(base_img_dir, input_subfolder)
    output_folder = os.path.join(base_img_dir, output_subfolder)

    print("📂 入力フォルダ:", input_folder)
    print("📁 出力フォルダ:", output_folder)

    # 出力フォルダがなければ作成
    os.makedirs(output_folder, exist_ok=True)

    # 入力フォルダ内のファイル一覧
    files = os.listdir(input_folder)
    print("🔍 処理対象ファイル:", files)

    # PNGファイルをローマ字にリネームしてコピー
    for filename in files:
        if filename.lower().endswith('.png'):
            katakana_name = os.path.splitext(filename)[0]  # 拡張子を除く
            romaji_name = to_romaji(katakana_name)         # ✅ 共通関数で変換

            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, romaji_name + '.png')

            # 既に同名ファイルが存在する場合はスキップ
            if os.path.exists(output_path):
                print(f"⚠ {output_path} は既に存在します。スキップします。")
                continue

            try:
                shutil.copy2(input_path, output_path)
                print(f"✅ {filename} → {romaji_name}.png にコピーしました。")
            except Exception as e:
                print(f"❌ {filename} のコピー中にエラー: {e}")

if __name__ == "__main__":
    rename_images_in_folder()
