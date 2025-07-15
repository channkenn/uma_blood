import os
import re
from unidecode import unidecode

# プロジェクトルートを計算
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG_DIR = os.path.join(ROOT_DIR, "img")
SVG_DIR = os.path.join(ROOT_DIR, "svg")
CSV_DIR = os.path.join(ROOT_DIR, "csv")

def get_csv_path(filename):
    return os.path.join(CSV_DIR, filename)

def get_img_path(filename):
    return os.path.join(IMG_DIR, filename)

def get_svg_path(filename):
    return os.path.join(SVG_DIR, filename)

def to_romaji(name: str) -> str:
    """
    日本語名をローマ字に変換し、半角スペース・禁止文字を除去
    """
    romaji = unidecode(name)              # ローマ字に変換
    romaji = romaji.replace(" ", "")      # 半角スペース削除
    romaji = re.sub(r'[\\/:*?"<>|]', "", romaji)  # Windows禁止文字削除
    return romaji