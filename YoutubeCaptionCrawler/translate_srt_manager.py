import openai
import os
import re
import glob
import shutil
import time

BILINGUAL_SRTS_FOLDER = "/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/bilingual_srts"
ORIGINAL_EN_SRTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/original_en_srts'
ARCHIVED_EN_SRTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/archived_en_srts'
ARCHIVED_MERGED_CH_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/translation/archived_merged_ch'
TRANSLATION_SPLITING_EN_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/translation/splited_en'
TRANSLATION_SPLITING_CH_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/translation/splited_ch'
TRANSLATION_MERGED_CH_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/translation/merged_ch'


def _get_filename_without_extension(file_path):
    base_name = os.path.basename(file_path)
    file_name_without_extension, _ = os.path.splitext(base_name)
    return file_name_without_extension

def _get_folder_name(folder_path):
    return os.path.basename(folder_path)

def _get_all_subfolders(folder_path):
    return [os.path.join(folder_path, name) for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]

def _calculate_files(under_dir):
    file_count = 0
    for root, dirs, files in os.walk(under_dir):
        file_count += len(files)
    return file_count

def _get_filename_without_extension(file_path):
    base_name = os.path.basename(file_path)
    file_name_without_extension, _ = os.path.splitext(base_name)
    return file_name_without_extension

def _get_foldername(folder_path):
    return os.path.basename(folder_path)

def _make_folder_if_needed(under_path, folder_name):
        new_folder_path = os.path.join(under_path, folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        return new_folder_path

def merge_srt_files_in_folder(folder_path):
    print(folder_path)
    video_name = _get_folder_name(folder_path)
    print(f"🚀 Start to merge {video_name} srt files!")
    print(video_name)
    # 獲取文件夾下的所有 srt 文件，並按照數字順序排序
    file_list = sorted(glob.glob(os.path.join(folder_path, '*.srt')), key=lambda x: int(x.split('/')[-1].split('.')[0].replace('split_file', '')))

    output_file_path = os.path.join(TRANSLATION_MERGED_CH_FOLDER, f'{video_name}.srt')
    with open(output_file_path, 'w') as output_file:
        for file_name in file_list:
            with open(file_name, 'r') as input_file:
                lines = input_file.readlines()
                output_file.write('\n\n')
                output_file.writelines(lines)
    
    print(f"🤩 finish to merge {video_name} srt files!")


openai.api_key = "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"

def request_with_retry(text, completion_block=None):
    max_retries = 20
    retries = 0

    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                # model="gpt-4-0125-preview",
                model='gpt-4-0613',
                # model="gpt-3.5-turbo-16k-0613",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant, an expert in computer science, particularly well-versed in iOS and architectural design. Your next task is to help translate English subtitles of a lecture on architectural design."},
                    {"role": "user", 
                        "content": f"Translate the following English subtitles to Traditional Chinese, but do not translate the technical terms, and people's name. Please retain the original subtitle format (time stamps, subtitle sequence numbers, etc.), only translate the content of the subtitles: {text}"},
                ]
            )
            
            # If request was successful, break the loop and return the response
            if completion_block:
                translated_subtitle = response.choices[0].message['content']
                completion_block(translated_subtitle)
            return translated_subtitle
        
        except openai.error.APIError as e:
            print(f"APIError occurred: {e}. Retrying...")

        # If request was not successful, wait for 60 seconds and then retry
        retries += 1
        time.sleep(300 * retries)

    # If maximum retries are exhausted, raise an exception
    raise Exception("Maximum retries exceeded without a successful response.")

def make_completion_function(text_file_path):
    def completion_function(response):
        file_name = _get_filename_without_extension(text_file_path)
        print(f"👋 Request completed successfully! Now deleting file: {file_name}")
        os.remove(text_file_path)
        remained_files = _calculate_files(TRANSLATION_SPLITING_EN_FOLDER)
        print(f"🥰 Remained {remained_files} files!")
        # Add code here to delete the file
    return completion_function

def _translate_by_chat_api(text_file_path):
    completion_block = make_completion_function(text_file_path)
    with open(text_file_path, 'r') as file:
        content = file.read()
    translated_subtitle = request_with_retry(content, completion_block=completion_block)
    return translated_subtitle



def _get_all_files_in_directory(dir_path):
    all_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file == '.DS_Store':
                continue
            all_files.append(os.path.join(root, file))
    return all_files

def _get_subfolders(directory):
    subfolder_list = []

    for dirpath, dirnames, files in os.walk(directory):
        for dirname in dirnames:
            subfolder_list.append(os.path.join(dirpath, dirname))
    
    return subfolder_list


def _translate_srts():
    print("🚀 Start _translate_srts process!")
    splited_en_folder_paths = _get_subfolders(TRANSLATION_SPLITING_EN_FOLDER)
    print(splited_en_folder_paths)
    all_splited_en_file_paths = []
    for splited_en_folder_path in splited_en_folder_paths:
        video_name = _get_folder_name(splited_en_folder_path)
        all_splited_en_file_paths.append((video_name ,_get_all_files_in_directory(splited_en_folder_path)))
    for video_name, splited_en_file_paths in all_splited_en_file_paths:
        saved_folder_path = _make_folder_if_needed(TRANSLATION_SPLITING_CH_FOLDER, video_name)
        print(f'🚀 Start to use chat API to translate: {video_name}')
        for splited_en_file_path in splited_en_file_paths:
            file_name = _get_filename_without_extension(splited_en_file_path)
            print(f'🚀 Start to translate: {file_name}')
            translated_subtitle = _translate_by_chat_api(splited_en_file_path)
            print(f'🤩 Finish to translate: {file_name}')
            saved_file_path = os.path.join(saved_folder_path, f'{file_name}.srt')
            with open(saved_file_path, 'w') as file:
                file.write(translated_subtitle)
        print(f'🤩 Finish to use chat API to translate: {video_name}')
    print("🤩 Finish _translate_srts process!")


def parse_srt(srt_content):
    blocks = re.split(r'\n\n', srt_content.strip())
    srt_dict = {}
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 2:
            index = lines[0]
            timestamp = lines[1]
            text_lines = lines[2:]
            srt_dict[index] = {'timestamp': timestamp, 'text_lines': text_lines}
    return srt_dict

def _merge_bilingual_subtitles():
    print("🚀 Start to do _merge_bilingual_subtitles process!")
    # 獲取每個資料夾中所有的srt文件的檔名
    en_srt_files = glob.glob(os.path.join(ORIGINAL_EN_SRTS_FOLDER, "*.srt"))
    ch_srt_files = glob.glob(os.path.join(TRANSLATION_MERGED_CH_FOLDER, "*.srt"))
    for file in en_srt_files:
        print(en_srt_files)
    # 取得 en_srt 和 ch_srt 資料夾中相同的檔名（不含副檔名）
    common_filenames = set(_get_filename_without_extension(en_file) for en_file in en_srt_files).intersection(
        set(_get_filename_without_extension(ch_file) for ch_file in ch_srt_files)
    )
    print(common_filenames)
    for filename in common_filenames:
        en_file_path = os.path.join(ORIGINAL_EN_SRTS_FOLDER, filename + ".srt")
        ch_file_path = os.path.join(TRANSLATION_MERGED_CH_FOLDER, filename + ".srt")
        print(en_file_path)
        print(ch_file_path)
        # 讀取英文和中文srt文件的內容
        with open(en_file_path, "r") as en_file, open(ch_file_path, "r") as ch_file:
            en_srt_dict = parse_srt(en_file.read())
            ch_srt_dict = parse_srt(ch_file.read())

        # 將兩個srt文件的內容合併，同一個時間戳的英文和中文內容放在一起
        combined_srt_content = []
        for index in sorted(en_srt_dict.keys(), key=int):  # 排序以確保正確的順序
            en_block = en_srt_dict[index]
            combined_srt_content.append(index)
            combined_srt_content.append(en_block['timestamp'])
            combined_srt_content.extend(en_block['text_lines'])
            if index in ch_srt_dict:
                combined_srt_content.extend(ch_srt_dict[index]['text_lines'])
            combined_srt_content.append('')  # 空行作為分隔符

        # 寫入到新的srt文件
        bingual_viedeo_name = os.path.basename(en_file_path).replace('_en', '')
        output_file_path = os.path.join(BILINGUAL_SRTS_FOLDER, bingual_viedeo_name)
        with open(output_file_path, "w") as output_file:
            output_file.write("\n".join(combined_srt_content))
        _move_file(en_file_path, target_folder=ARCHIVED_EN_SRTS_FOLDER)
        _move_file(ch_file_path, target_folder=ARCHIVED_MERGED_CH_FOLDER)
    print("🤩 Finish to do _merge_bilingual_subtitles process!")

def _move_files(source_folder, target_folder):
    # 確保目標資料夾存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # 取得來源資料夾中的所有檔案
    files = os.listdir(source_folder)

    for file in files:
        source_file_path = os.path.join(source_folder, file)
        target_file_path = os.path.join(target_folder, file)

        # 使用 shutil.move 將檔案移動到目標資料夾
        shutil.move(source_file_path, target_file_path)

def _move_file(file_path, target_folder):
    # 確保目標資料夾存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    base_name = os.path.basename(file_path)
    target_file_path = os.path.join(target_folder, base_name)
    shutil.move(file_path, target_file_path)

def _move_en_srts():
    _move_files(ORIGINAL_EN_SRTS_FOLDER, ARCHIVED_EN_SRTS_FOLDER)


'''
steps:
1. 將想要翻譯的英文字幕放到 original_en_srts folder
2. 系統會直接將 srt 每 10 個區間分為一個檔案(存放在 translation/splited_en/{video_name} 中)，然後一個一個 file 餵給 chat API
3. chat API 翻譯完的文件會存放在 translation/splited_ch/{video_name} 中
4. 系統會再主動將這些翻譯好的小文件 merge 在一起，並存放在 translation/merged_ch/{video_name} 中
5. 最後會執行 _merge_bilingual_subtitles 將 translation/merged_ch/{video_name} 和 original_en_srts 下的相同檔名的 srt merge 成雙語字幕黨
並存放在 bilingual_srts
'''

def _merge_splited_ch():
    print("🚀 Start to do merge process!")
    srt_folders = _get_all_subfolders(TRANSLATION_SPLITING_CH_FOLDER)
    print(srt_folders)
    for srt_folder in srt_folders:
        video_name = _get_folder_name(srt_folder)
        print(f"🚀 Start to merge {video_name}!")
        merge_srt_files_in_folder(srt_folder)
        print(f"🤩 Finish to merge {video_name}!")
    print("🤩 Finish to do all merge process!")

def do_translation_process():
    _translate_srts()
    _merge_splited_ch()
    _merge_bilingual_subtitles()