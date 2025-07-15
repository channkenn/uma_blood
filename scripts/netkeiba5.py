# scripts/netkeiba5.py

import csv
import os
from bloodline import load_bloodline_from_csv, create_combined_bloodline_image_google, process_horse
from utils import get_csv_path, get_svg_path, get_generated_csv_path
index_set = [
    (0, 1, 32), (1, 2, 17), (2, 3, 10), (3, 4, 7), (4, 5, 6),
    (7, 8, 9), (10, 11, 14), (11, 12, 13), (14, 15, 16), (17, 18, 25),
    (18, 19, 22), (19, 20, 21), (22, 23, 24), (25, 26, 29), (26, 27, 28),
    (29, 30, 31), (32, 33, 48), (33, 34, 41), (34, 35, 38), (35, 36, 37),
    (38, 39, 40), (41, 42, 45), (42, 43, 44), (45, 46, 47), (48, 49, 56),
    (49, 50, 53), (50, 51, 52), (53, 54, 55), (56, 57, 60), (57, 58, 59),
    (60, 61, 62),
]

def process_csv(input_filename):
    first_loop = True
    input_file = get_csv_path("bloodline_netkeiba5.csv")
    with open(input_file, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        for row in reader:
            if len(row) < 2:
                continue
            name = row[0]
            ancestor_str = ",".join(row[1:])
            ancestor_list = (name + "," + ancestor_str).split(",")
            processed = set()
            data = [["名前", "父", "母"]]

            process_horse(index_set[0], ancestor_list, processed, data)
            for index_tuple in index_set[1:]:
                process_horse(index_tuple, ancestor_list, processed, data)

            # CSVの出力先を utils.py で管理している csv フォルダに出力
            output_filename = get_generated_csv_path(f"{name}.csv")
            with open(output_filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(data)

            mode = "w" if first_loop else "a"
            cfm_filename = get_generated_csv_path("bloodline_netkeiba5_cfm.csv")
            with open(cfm_filename, mode=mode, newline='', encoding="utf-8") as cfm_file:
                writer = csv.writer(cfm_file)
                if first_loop:
                    writer.writerow(["名前", "父", "母"])
                    first_loop = False
                writer.writerows(data[1:])

            bloodlines_dict = load_bloodline_from_csv(output_filename)

            # SVG出力先も utils.py で管理している svg フォルダに
            output_file = get_svg_path(f"{name}.svg")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            if not os.path.exists(output_file):
                create_combined_bloodline_image_google(name, bloodlines_dict)
            else:
                print(f"{output_file} は既に存在するためスキップします。")

if __name__ == "__main__":
    process_csv("bloodline_netkeiba5.csv")
