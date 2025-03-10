import os
import csv
from unidecode import unidecode
from graphviz import Digraph
import urllib.parse
site_name = "(netkeiba OR wikipedia)"
def generate_google_search_url(horse_name, site_name):
    query = f"{horse_name} {site_name}"
    encoded_query = urllib.parse.quote(query)
    #return f"https://www.google.com/search?q={encoded_query}"
    return f"{horse_name}.svg"

# CSVデータを辞書に変換
def load_bloodline_from_csv(csv_file):
    bloodlines_dict = {}
    with open(csv_file, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['名前']:  # 名前が空でない場合のみ追加
                bloodlines_dict[row['名前']] = row
    return bloodlines_dict

# 画像のパス取得
def get_image_path(image_name):
    image_path = f"img/{image_name}.png"
    return image_path if os.path.isfile(image_path) else "img/mob.png"

# 再帰的に血統図を生成する関数（複数の名前を処理できるように変更）
def create_combined_bloodline_image(names, bloodlines_dict):
    dot = Digraph(format="svg")
    dot.attr(rankdir="TB")
    dot.attr(fontname="MS Gothic")
    dot.attr(ranksep="1.5", nodesep="0.1")  # ノード間の間隔を広げる
    dot.attr(bgcolor='transparent')  # 背景を透過に設定
    added_edges = set()  # 追加済みエッジを管理するセット
    # 左上固定のテキストを追加
    dot.node("fixed_label", label="左上固定のテキスト", shape="none", pos="-1,0!")
    def process_individual(name, depth=0):
        if depth > 24:  # 無限ループ防止
            return
        
        row = bloodlines_dict.get(name)
        if not row:
            return

        child = row['名前'] or "unknown_child"
        father = row['父'] or "unknown_father"
        mother = row['母'] or "unknown_mother"
        #wikiURL = row['wikiURL'] or "unknown_wiki"
        wikiURL = generate_google_search_url(name, site_name)
        # ノード追加（子）
        if child not in ["unknown_child", "unknown"]:
            dot.node(child, shape="box", image=get_image_path(unidecode(child)), width="0.1", height="0.1", label=child, URL=wikiURL)

        # ノード追加（親）
        for parent, color in [(father, "lightblue")]:
            if parent not in ["unknown_father", "unknown_mother", "unknown"]:
                dot.node(parent, shape="box", style="filled", color=color, fontname="MS Gothic",
                        image=get_image_path(unidecode(parent)), width="0.1", height="0.1", label=parent, URL=generate_google_search_url(parent, site_name))
                if (parent, child) not in added_edges:  # すでに同じエッジがないか確認
                    edge_color = color
                    dot.edge(parent, child, color=edge_color, penwidth="5")  # エッジの色と太さを変更
                    added_edges.add((parent, child))

        # 祖父母が血統辞書に存在するか確認->母のみにする
        for parent in [father]:
            if parent in bloodlines_dict:
                process_individual(parent, depth + 1)

    # 各個体を処理
    for name in names:
        process_individual(name)

    # SVGファイルを保存
    filename = "uma_blood_netkeiba5_cfm_f"  
    output_path = dot.render(filename, cleanup=True)
    print(f"SVGファイルが生成されました: {output_path}")

# CSV読み込み
csv_file = "bloodline_netkeiba5_cfm.csv"
bloodlines_dict = load_bloodline_from_csv(csv_file)

# 複数の名前で血統図を作成
names = [
    "スペシャルウィーク",
    "サイレンススズカ",
    "トウカイテイオー",
    "マルゼンスキー",
    "フジキセキ",
    "オグリキャップ",
    "ゴールドシップ",
    "ウオッカ",
    "ダイワスカーレット",
    "タイキシャトル",
    "グラスワンダー",
    "ヒシアマゾン",
    "メジロマックイーン",
    "エルコンドルパサー",
    "テイエムオペラオー",
    "ナリタブライアン",
    "シンボリルドルフ",
    "エアグルーヴ",
    "アグネスデジタル",
    "タマモクロス",
    "セイウンスカイ",
    "ファインモーション",
    "ビワハヤヒデ",
    "マヤノトップガン",
    "マンハッタンカフェ",
    "ミホノブルボン",
    "メジロライアン",
    "ヒシアケボノ",
    "ユキノビジン",
    "ライスシャワー",
    "アイネスフウジン",
    "アグネスタキオン",
    "アドマイヤベガ",
    "イナリワン",
    "ウイニングチケット",
    "エアシャカール",
    "エイシンフラッシュ",
    "カレンチャン",
    "カワカミプリンセス",
    "ゴールドシチー",
    "サクラバクシンオー",
    "シーキングザパール",
    "シンコウウインディ",
    "スイープトウショウ",
    "スーパークリーク",
    "スマートファルコン",
    "ゼンノロブロイ",
    "ナカヤマフェスタ",
    "トーセンジョーダン",
    "ナリタタイシン",
    "ニシノフラワー",
    "ハルウララ",
    "バンブーメモリー",
    "ビコーペガサス",
    "マーベラスサンデー",
    "マチカネフクキタル",
    "ミスターシービー",
    "メイショウドトウ",
    "メジロドーベル",
    "ナイスネイチャ",
    "キングヘイロー",
    "マチカネタンホイザ",
    "イクノディクタス",
    "メジロパーマー",
    "ダイタクヘリオス",
    "ツインターボ",
    "サトノダイヤモンド",
    "キタサンブラック",
    "メジロアルダン",
    "サクラチヨノオー",
    "シリウスシンボリ",
    "ヤエノムテキ",
    "メジロブライト",
    "ナリタトップロード",
    "ヤマニンゼファー",
    "アストンマーチャン",
    "サトノクラウン",
    "シュヴァルグラン",
    "サクラローレル",
    "ツルマルツヨシ",
    "コパノリッキー",
    "シンボリクリスエス",
    "タニノギムレット",
    "デアリングタクト",
    "ホッコータルマエ",
    "ワンダーアキュート",
    "ダイイチルビー",
    "ケイエスミラクル",
    "メジロラモーヌ",
    "ジャングルポケット",
    "カツラギエース",
    "ネオユニヴァース",
    "ヒシミラクル",
    "タップダンスシチー",
    "サウンズオブアース",
    "ノースフライト",
    "ドゥラメンテ",
    "ヴィルシーナ",
    "ヴィブロス",
    "サムソンビッグ",
    "ロイスアンドロイス",
    "シーザリオ",
    "ラインクラフト",
    "エアメサイア",
    "デアリングハート",
    "フリオーソ",
    "トランセンド",
    "エスポワールシチー",
    "ダンツフレーム",
    "ノーリーズン",
    "スティルインラブ",
    "オルフェーヴル",
    "ジェンティルドンナ",
    "ウインバリアシオン",
    "ドリームジャーニー",
    "ブエナビスタ",
    "ビリーヴ",
    "カルストンライトオ",
    "デュランダル",
    "バブルガムフェロー",
    "フサイチパンドラ",
    "ブラストワンピース",
    "サクラチトセオー",
    "トキノミノル",
    "ゴドルフィンバルブ",
    "ダーレーアラビアン",
    "バイアリーターク",
    "ハイセイコー",
    "スピードシンボリ",
    "セントライト",
    "カレンブーケドール",
    "クロノジェネシス",
    "ラヴズオンリーユー",
    "グランアレグリア",
    "ラッキーライラック",
    "アーモンドアイ",
    "フェノーメノ",
    ]
create_combined_bloodline_image(names, bloodlines_dict)
