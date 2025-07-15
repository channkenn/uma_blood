import os

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
