from PIL import Image
name = "uma_blood_f"
input_png = f"{name}.png"  # 元のPNG
output_png = f"{name}_resized.png"  # 圧縮後のPNG
target_size_mb = 4  # 目標ファイルサイズ（MB）
# 制限解除
Image.MAX_IMAGE_PIXELS = None  
# 画像を開く
img = Image.open(input_png)

# 現在のサイズを取得
width, height = img.size
print(f"元のサイズ: {width}x{height}")

# まず解像度を少し下げる（75%）
new_width = int(width * 0.75)
new_height = int(height * 0.75)
img = img.resize((new_width, new_height), Image.LANCZOS)

# 圧縮して保存（品質を調整）
quality = 90  # PNGはJPEGと違い、品質を圧縮するのではなく、圧縮率を調整
img.save(output_png, format="PNG", optimize=True)

# ファイルサイズを確認しながら調整
import os

file_size_mb = os.path.getsize(output_png) / (1024 * 1024)  # MB単位
print(f"圧縮後サイズ: {file_size_mb:.2f} MB")

# 目標サイズになるまで品質を調整
while file_size_mb > target_size_mb and new_width > 200 and new_height > 200:
    new_width = int(new_width * 0.9)
    new_height = int(new_height * 0.9)
    img = img.resize((new_width, new_height), Image.LANCZOS)
    img.save(output_png, format="PNG", optimize=True)

    file_size_mb = os.path.getsize(output_png) / (1024 * 1024)
    print(f"調整後サイズ: {file_size_mb:.2f} MB")

print(f"最終的なサイズ: {new_width}x{new_height}, {file_size_mb:.2f} MB")
print(f"リサイズ完了: {output_png}")
