import os
import glob

src_folder = '/Volumes/Transcend/Essential Developer/test2'

def get_subdirectory_paths(base_path):
        return [os.path.join(base_path, name) for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name))]


def clean_screenshots(src_dir, suffix='-0'):
    chapter_folder_paths = get_subdirectory_paths(src_dir)

    all_sub_chapter_folder_paths = []
    for chapter_folder_path in chapter_folder_paths:
        all_sub_chapter_folder_paths += get_subdirectory_paths(chapter_folder_path)
    all_screenshots_folder_paths = []
    for sub_chapter_folder_path in all_sub_chapter_folder_paths:
        all_screenshots_folder_paths += get_subdirectory_paths(sub_chapter_folder_path) 
    
    for sceenshot_folder_path in all_screenshots_folder_paths:
         files = glob.glob(os.path.join(sceenshot_folder_path, '*'))
         # 遍歷每個文件
         for file_path in files:
             base_name = os.path.splitext(os.path.basename(file_path))[0]
             # 檢查檔名是否以指定的後綴結尾
             if base_name.endswith(suffix):
                # 刪除該文件
                os.remove(file_path)
                print(f'Deleted file: {file_path}')


        

clean_screenshots(src_folder)
