import os

def replace_svg_paths(
    svg_subfolder="svg",
    replace_from="c:/Users/chann/Documents/VScode/uma_blood/img/",
    replace_to="https://channkenn.github.io/uma_blood/img/"
):
    """
    svg_subfolder 内のすべての .svg ファイルについて、
    ローカルパスをGitHub PagesのURLに置換する。
    """
    # カレントディレクトリからsvgフォルダのパスを取得
    base_dir = os.getcwd()
    svg_folder = os.path.join(base_dir, svg_subfolder)

    if not os.path.isdir(svg_folder):
        print(f"❌ SVGフォルダが見つかりません: {svg_folder}")
        return

    # svgフォルダ内の全SVGファイルを処理
    for filename in os.listdir(svg_folder):
        if filename.lower().endswith(".svg"):
            filepath = os.path.join(svg_folder, filename)

            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # バックスラッシュをスラッシュに統一
                content = content.replace("\\", "/")

                # パスをURLに置換
                new_content = content.replace(replace_from, replace_to)

                # 上書き保存
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(new_content)

                print(f"✅ 置換完了: {filename}")

            except Exception as e:
                print(f"❌ エラー: {filename} の処理中に失敗しました → {e}")

if __name__ == "__main__":
    replace_svg_paths()
