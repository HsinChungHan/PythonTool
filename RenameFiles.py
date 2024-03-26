import os

def rename_files_in_folder(folder_path):
    # 獲取資料夾中所有檔案和子資料夾的名稱
    files = os.listdir(folder_path)
    # 過濾出檔案，忽略子資料夾
    files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]
    # 排序檔案名稱，如果需要的話
    files.sort()
    # 遍歷檔案並重新命名
    for i, filename in enumerate(files, start=1):
        # 獲取檔案的完整路徑
        old_file = os.path.join(folder_path, filename)
        # 獲取檔案的副檔名
        _, extension = os.path.splitext(filename)
        # 新檔案名稱（不含路徑）
        new_filename = f"{i}{extension}"
        # 新檔案的完整路徑
        new_file = os.path.join(folder_path, new_filename)
        # 重新命名檔案
        os.rename(old_file, new_file)
        print(f"Renamed {old_file} to {new_file}")

# 使用範例，將以下路徑替換成你的目標資料夾路徑
folder_path = '/Users/chunghanhsin/Downloads/images'
rename_files_in_folder(folder_path)
