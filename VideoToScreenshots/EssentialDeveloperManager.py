import os
import shutil
from collections import defaultdict

def get_subdirectory_paths(base_path):
    return [os.path.join(base_path, name) for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]


def move_files_to_new_folders(src_dir):
    file_dict = defaultdict(list)

    # 建立前綴和檔案路徑的映射
    for filename in os.listdir(src_dir):
        # 忽略隱藏檔案（即以點開頭的檔案）
        if filename.startswith('.'):
            continue

        if filename.endswith('.mkv') or filename.endswith('.srt') or filename.endswith('.pdf'):
            prefix = filename.split('_')[0]
            file_dict[prefix].append(filename)

    # 移動具有相同前綴的檔案到新資料夾
    for prefix, files in file_dict.items():
        # 以.mkv檔案命名新資料夾
        mkv_file = [file for file in files if file.endswith('.mkv')]
        if mkv_file:
            new_dir = os.path.join(src_dir, os.path.splitext(mkv_file[0])[0])
            os.makedirs(new_dir, exist_ok=True)
            for file in files:
                shutil.move(os.path.join(src_dir, file), new_dir)

# src_dir = '/Volumes/Transcend/Essential Developer/test'  # 將此行更改為你的源資料夾路徑
# dirs = get_subdirectory_paths(src_dir)
# # print(dirs)
# # print(os.listdir(dirs[0]))
# for dir in dirs:
#     move_files_to_new_folders(dir)




font_dirs = ["/Library/Fonts", "/System/Library/Fonts", os.path.expanduser("~/Library/Fonts")]
for font_dir in font_dirs:
    for font_file in os.listdir(font_dir):
        # print(font_file.lower())
        if font_file.lower() == "monaco.ttf":
            print(f"Arial font found: {os.path.join(font_dir, font_file)}")