import os
from unidecode import unidecode

# 変換したいフォルダのパス
folder_path = os.getcwd()  # 現在の作業ディレクトリを取得
print("現在の作業ディレクトリ:", os.getcwd())
# フォルダ内のファイルをチェック
print("フォルダ内のファイル:", os.listdir(folder_path))
for filename in os.listdir(folder_path):
    if filename.endswith('.png'):  # .pngファイルを対象に
        katakana_name = os.path.splitext(filename)[0]  # 拡張子を除いたカタカナ部分
        romaji_name = unidecode(katakana_name)  # ローマ字に変換
        old_file = os.path.join(folder_path, filename)
        new_file = os.path.join(folder_path, romaji_name + '.png')  # ローマ字に変換してファイル名変更
                # 既に同じ名前のファイルが存在する場合はスキップ
        if os.path.exists(new_file):
            print(f"{new_file} は既に存在します。スキップします。")
            continue  # 次のファイルに進む
        os.rename(old_file, new_file)  # リネーム
        print(f"{filename} を {romaji_name}.png に変換しました。")
