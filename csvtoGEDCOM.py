import pandas as pd

# CSV を読み込む
df = pd.read_csv("bloodline_.csv", encoding="utf-8")

# GEDCOM ヘッダー
gedcom_data = ["0 HEAD"]

# ID 管理用の辞書（名前 → GEDCOM ID）
person_ids = {}
family_count = 1
default_surname = "不明"  # デフォルトの姓

# 個人情報を追加
def add_person(name, role="本人"):
    """名前と役割（世代）ごとに一意の ID を割り当て、GEDCOM データに追加"""
    if pd.isna(name) or name == "---":
        return None
    
    # 名前が空でなくても、同じ人物に一意のIDを割り当て
    unique_key = name  # 姓名で一意にIDを管理するため、役割を除外

    # すでに ID が割り振られている場合は処理しない
    if unique_key in person_ids:
        return person_ids[unique_key]

    # 新規人物にはIDを割り当て
    person_id = f"@I{len(person_ids)+1}@"
    person_ids[unique_key] = person_id

    # 姓と名の分割（空白がない場合はデフォルトの姓を設定）
    if " " in name:
        given_name, surname = name.split(" ", 1)
    else:
        given_name = name
        surname = default_surname

    gedcom_data.append(f"0 {person_id} INDI")
    gedcom_data.append(f"1 NAME {given_name} /{surname}/")  # 姓を追加
    gedcom_data.append("1 SEX U")  # 性別不明（後で追加可能）
    gedcom_data.append("1 BIRT")
    gedcom_data.append("2 DATE XXXX")  # 生年月日（不明なら仮の値）

    return person_ids[unique_key]

# すべての個人を登録（名前に世代情報を付ける）
for _, row in df.iterrows():
    add_person(row["名前"], "本人")
    add_person(row["父"], "父")
    add_person(row["母"], "母")
    add_person(row["父父"], "父方祖父")
    add_person(row["父母"], "父方祖母")
    add_person(row["母父"], "母方祖父")
    add_person(row["母母"], "母方祖母")

# 家族情報を追加
# 家族情報の重複を防ぐためのセット（父母の組み合わせ）
added_family_combinations = set()

# 家族情報を追加
# 家族情報を追加
for _, row in df.iterrows():
    child_id = add_person(row["名前"], "本人")
    father_id = add_person(row["父"], "父")
    mother_id = add_person(row["母"], "母")
    
    if father_id or mother_id:
        family_id = f"@F{family_count}@"
        family_count += 1
        gedcom_data.append(f"0 {family_id} FAM")
        
        # 父母の組み合わせをキーとしてセットで確認
        family_combination = tuple(sorted([father_id, mother_id]))  # 並べ替えて重複を避ける
        if family_combination not in added_family_combinations:
            added_family_combinations.add(family_combination)
            
            # 父親と母親、子供を家族IDに紐付け
            if father_id:
                gedcom_data.append(f"1 HUSB {father_id}")
            if mother_id:
                gedcom_data.append(f"1 WIFE {mother_id}")
            if child_id:
                gedcom_data.append(f"1 CHIL {child_id}")
            
            # 家族IDの参照が必要なので、再度そのIDを家族メンバーとして追加する
            gedcom_data.append(f"1 FAM {family_id}")  # 家族IDの参照を追加

        else:
            # すでに追加されている家族情報なら、FAMを追加しない
            continue


    # 祖父母の家族データを追加（父側）
    grandfather_id = add_person(row["父父"], "父方祖父")
    grandmother_id = add_person(row["父母"], "父方祖母")
    if grandfather_id or grandmother_id:
        family_id = f"@F{family_count}@"
        family_count += 1
        gedcom_data.append(f"0 {family_id} FAM")
        
        # 父側の祖父母の組み合わせ
        family_combination = tuple(sorted([grandfather_id, grandmother_id]))  # 並べ替えて重複を避ける
        if family_combination not in added_family_combinations:
            added_family_combinations.add(family_combination)
            
            # 祖父母を家族IDに紐付け
            if grandfather_id:
                gedcom_data.append(f"1 HUSB {grandfather_id}")
            if grandmother_id:
                gedcom_data.append(f"1 WIFE {grandmother_id}")
        
            if father_id:
                gedcom_data.append(f"1 CHIL {father_id}")

    # 祖父母の家族データを追加（母側）
    grandfather_id = add_person(row["母父"], "母方祖父")
    grandmother_id = add_person(row["母母"], "母方祖母")
    if grandfather_id or grandmother_id:
        family_id = f"@F{family_count}@"
        family_count += 1
        gedcom_data.append(f"0 {family_id} FAM")
        
        # 母側の祖父母の組み合わせ
        family_combination = tuple(sorted([grandfather_id, grandmother_id]))  # 並べ替えて重複を避ける
        if family_combination not in added_family_combinations:
            added_family_combinations.add(family_combination)
            
            # 祖父母を家族IDに紐付け
            if grandfather_id:
                gedcom_data.append(f"1 HUSB {grandfather_id}")
            if grandmother_id:
                gedcom_data.append(f"1 WIFE {grandmother_id}")
        
            if mother_id:
                gedcom_data.append(f"1 CHIL {mother_id}")



# GEDCOM フッター
gedcom_data.append("0 TRLR")

# UTF-8（BOM付き）で保存（Gramps で読み込みやすい）
with open("bloodline.ged", "w", encoding="utf-8-sig", newline="\n") as f:
    f.write("\n".join(gedcom_data))

print("GEDCOMファイルが作成されました: bloodline.ged")
