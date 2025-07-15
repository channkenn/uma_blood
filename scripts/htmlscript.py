import pandas as pd

# CSVファイルを読み込む
csv_file = "bloodline.csv"  # CSVファイル名
df = pd.read_csv(csv_file, encoding="utf-8")  # 日本語対応のためにエンコーディングを指定

# HTMLテンプレート
html_template = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <!-- SNS用メタタグ -->
    <meta property="og:title" content="{name}3代血統">
    <meta property="og:description" content="このページにはSVG画像を埋め込んだサムネイルが表示されます。">
    <meta property="og:image" content="https://channkenn.github.io/uma_blood/img/{name}.png">
    <meta property="og:url" content="https://channkenn.github.io/uma_blood/{name}.html">
    <meta name="twitter:card" content="summary_large_image">
    
    <title>{name}3代血統</title>
</head>
<body>
    <h1>{name}3代血統</h1>

    <!-- SVGを外部から埋め込む -->
    <object data="https://channkenn.github.io/uma_blood/{name}.svg" type="image/svg+xml" width="200" height="200">
        お使いのブラウザではSVG画像を表示できません。
    </object>
    
</body>
</html>
"""

# 各名前でHTMLファイルを生成
for name in df['名前']:
    # HTMLを生成
    html_content = html_template.format(name=name)
    
    # 日本語名でHTMLファイルを保存
    file_name = f"{name}.html"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"{file_name} を作成しました！")
