import subprocess
name = "uma_blood_f"
input_svg = f"{name}.svg"
output_png = f"{name}.png"
inkscape_path = r"C:\Program Files\Inkscape\bin\inkscape.exe"  # Inkscape のパスを指定

# SVG → PNG 変換
subprocess.run([inkscape_path, input_svg, "--export-filename=" + output_png, "--export-dpi=50"])

print(f"変換完了: {output_png}")
