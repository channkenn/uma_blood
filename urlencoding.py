import csv
import urllib.parse

# CSVファイルを開く
with open("bloodline.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    
    # 各行の "名前" をURLエンコードして出力
    for row in reader:
        name = row["名前"]
        encoded_name = urllib.parse.quote(name, safe="")
        url = f"https://ja.wikipedia.org/wiki/{encoded_name}"
        print(url)
