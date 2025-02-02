from PIL import Image
name = "uma_blood_f"
# 画像を読み込む
image = Image.open(f"{name}.png")

# αチャネルを削除する
image = image.convert('RGB')

# αなしPNGとして保存する
image.save(f"{name}_no_alpha.png")
