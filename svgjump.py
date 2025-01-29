from xml.etree import ElementTree as ET

def update_svg_links(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # SVG内のリンクを更新する
    for a_tag in root.findall('.//a'):
        a_tag.set('target', '_blank')  # 新しいタブで開くように設定

    # 変更を保存
    tree.write('updated_umadice.svg')

# SVGファイルを更新
update_svg_links('umadice.svg')
