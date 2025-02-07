import os
import csv
from unidecode import unidecode
from graphviz import Digraph

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

    def process_individual(name, depth=0):
        if depth > 3:  # 無限ループ防止
            return
        
        row = bloodlines_dict.get(name)
        if not row:
            return

        # ノードIDをユニークにする
        child_id = f"{name}_{depth}"
        father_id = f"{row['父']}_{depth+1}" if row['父'] else "unknown_father"
        mother_id = f"{row['母']}_{depth+1}" if row['母'] else "unknown_mother"
        father_father_id = f"{row['父父']}_{depth+2}" if row['父父'] else "unknown_father_father"
        father_mother_id = f"{row['父母']}_{depth+2}" if row['父母'] else "unknown_father_mother"
        mother_father_id = f"{row['母父']}_{depth+2}" if row['母父'] else "unknown_mother_father"
        mother_mother_id = f"{row['母母']}_{depth+2}" if row['母母'] else "unknown_mother_mother"
        
        wikiURL = row.get('wikiURL', "")

        # ノード追加（子）
        dot.node(child_id, shape="box", image=get_image_path(unidecode(name)), width="0.1", height="0.1", 
                 label=name, URL=wikiURL)

        # ノード追加（親）
        for parent, parent_id, color in [(row['父'], father_id, "lightblue"), (row['母'], mother_id, "lightcoral")]:
            if parent:
                dot.node(parent_id, shape="box", style="filled", color=color, fontname="MS Gothic",
                         image=get_image_path(unidecode(parent)), width="0.1", height="0.1", label=parent)
                if (parent_id, child_id) not in added_edges:
                    dot.edge(parent_id, child_id, color=color, penwidth="5")
                    added_edges.add((parent_id, child_id))

        # ノード追加（祖父母）
        for grandparent, grandparent_id, parent_id, color in [
            (row['父父'], father_father_id, father_id, "lightblue"),
            (row['父母'], father_mother_id, father_id, "lightcoral"),
            (row['母父'], mother_father_id, mother_id, "lightblue"),
            (row['母母'], mother_mother_id, mother_id, "lightcoral")
        ]:
            if grandparent:
                dot.node(grandparent_id, shape="box", style="filled", color=color, fontname="MS Gothic",
                         image=get_image_path(unidecode(grandparent)), width="0.1", height="0.1", label=grandparent)
                if (grandparent_id, parent_id) not in added_edges:
                    dot.edge(grandparent_id, parent_id, color=color, penwidth="5")
                    added_edges.add((grandparent_id, parent_id))

        # 祖父母が血統辞書に存在するか確認 -> 再帰処理
        for grandparent, grandparent_id in [
            (row['父父'], father_father_id),
            (row['父母'], father_mother_id),
            (row['母父'], mother_father_id),
            (row['母母'], mother_mother_id)
        ]:
            if grandparent in bloodlines_dict:
                process_individual(grandparent, depth + 2)

    # 各個体を処理
    for name in names:
        process_individual(name)

    # SVGファイルを保存
    filename = "uma_blood_all"
    output_path = dot.render(filename, cleanup=True)
    print(f"SVGファイルが生成されました: {output_path}")

# CSV読み込み
csv_file = "bloodline.csv"
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
    "バイアリーターク"
    ]
create_combined_bloodline_image(names, bloodlines_dict)
