import os
import shutil
import re

COURSE_CURRICULUM_FOLDER = '/Volumes/Transcend/Essential Developer/Course Curriculum/Ch3-1_ Persistence Module'
ORIGINAL_EN_SRTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/original_en_srts'

def _clean_vtt_file(file_path):
    # Open the file and read its contents
    with open(file_path, 'r', encoding='utf-8') as file:
        file_contents = file.read()

    # Use regex to remove the unwanted lines
    cleaned_contents = re.sub(r'WEBVTT\nX-TIMESTAMP-MAP=MPEGTS:130000,LOCAL:00:00:00.000\n', '', file_contents)
    cleaned_contents = cleaned_contents.strip() # remove leading and trailing whitespace

    # Overwrite the original file with the cleaned contents
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_contents)

def clean_vtt_files(under_dir=ORIGINAL_EN_SRTS_FOLDER):
    for root, dirs, files in os.walk(under_dir):
        for file in files:
            if file.endswith('.srt') or file.endswith('.vtt'):
                file_path = os.path.join(root, file)
                _clean_vtt_file(file_path)
                


def copy_srt_files(source_folder, target_folder):
    source_folder = COURSE_CURRICULUM_FOLDER
    target_folder = ORIGINAL_EN_SRTS_FOLDER
    print(os.listdir(source_folder))
    # 確保目標資料夾存在
    os.makedirs(target_folder, exist_ok=True)

    for foldername, subfolders, filenames in os.walk(source_folder):
        for filename in filenames:
            # 检查是否为 .srt 文件
            # 检查文件是否以 '._' 开头，如果是，则跳过
            if filename.startswith('._'):
                continue
            if '_en' not in filename:
                continue

            if filename.endswith('.srt'):
                # 完整的文件路径
                
                source_file = os.path.join(foldername, filename)
                filename = filename.replace('[', '').replace(']', '')
                target_file = os.path.join(target_folder, filename)

                # 复制文件
                shutil.copyfile(source_file, target_file)

# copy_srt_files(COURSE_CURRICULUM_FOLDER, ORIGINAL_EN_SRTS_FOLDER)
# clean_vtt_files(ORIGINAL_EN_SRTS_FOLDER)