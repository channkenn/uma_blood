import os

# svgフォルダのパス
svg_folder = os.path.join(os.getcwd(), "svg")

# 置換元と置換先
replace_from = "c:/Users/chann/Documents/VScode/uma_blood/img/"
replace_to = "https://channkenn.github.io/uma_blood/img/"

# svgフォルダ内の全SVGファイルを処理
for filename in os.listdir(svg_folder):
    if filename.endswith(".svg"):
        filepath = os.path.join(svg_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # バックスラッシュをスラッシュに統一
        content = content.replace("\\", "/")

        # パスをURLに置換
        new_content = content.replace(replace_from, replace_to)

        # 上書き保存
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"置換完了: {filename}")
