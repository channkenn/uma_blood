import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# CSVファイルの読み込み
csv_file = "horses.csv"  # 馬名が書かれたCSVファイル
df = pd.read_csv(csv_file)
horse_names = df.iloc[:, 0].tolist()  # 1列目の馬名リスト

# Seleniumの設定
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # ウィンドウを最大化

driver = webdriver.Chrome(options=options)
driver.get("https://db.netkeiba.com/")  # netkeibaの検索ページを開く

# 5回ずつ検索を実行
for i, horse in enumerate(horse_names):
    try:
        # 検索ボックスを取得して馬名を入力
        search_box = driver.find_element(By.NAME, "word")  # 検索フォームのname属性
        search_box.clear()
        search_box.send_keys(horse)
        search_box.send_keys(Keys.RETURN)  # Enterキーを押す

        time.sleep(3)  # サーバー負荷軽減のため待機

        # 検索結果ページのURLを取得し、新しいタブで開く
        search_result_url = driver.current_url
        driver.execute_script(f"window.open('{search_result_url}');")  

        # 検索タブに戻る
        driver.switch_to.window(driver.window_handles[0])
        driver.get("https://db.netkeiba.com/")  # 再度検索ページに戻る
        time.sleep(2)

        # 5回検索ごとに休憩を入れる
        if (i + 1) % 5 == 0:
            print(f"{i + 1}回検索完了。開いたタブを確認してください...")
            time.sleep(15)  # 15秒待機（手動で確認できるように）

    except Exception as e:
        print(f"エラー発生: {e}")
        break

print("すべての検索が完了しました。ブラウザは開いたままです。Ctrl + C でスクリプトを強制終了")

# ★ 無限ループでブラウザを開いたままにする（手動で閉じるまで待機）
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("スクリプトを終了します。")
