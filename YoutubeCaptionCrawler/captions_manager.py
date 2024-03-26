import srt
from datetime import timedelta

import re
import os
import tiktoken
import pysrt

SRT_FOLDER_PATH = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/original_en_srts'
TXT_FOLDER_PATH = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/original_en_txts'
TRANSLATION_SPLITING_EN_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/translation/splited_en'
ORIGINAL_EN_SRTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/original_en_srts'

# gpt-3.5-turbo
# gpt-4-0125-preview	
def _num_tokens_from_string(string: str, encoding_name: str='gpt-4-0125-preview	') -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def _get_all_files_in_directory(dir_path):
    all_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file == '.DS_Store':
                continue
            all_files.append(os.path.join(root, file))
    return all_files

def _get_filename_without_extension(file_path):
    base_name = os.path.basename(file_path)
    file_name_without_extension, _ = os.path.splitext(base_name)
    return file_name_without_extension

def _make_folder_if_needed(under_path, folder_name):
        new_folder_path = os.path.join(under_path, folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        return new_folder_path

def _convert_to_srt(file_path):
    file_name = _get_filename_without_extension(file_path)
    print(file_name)
    with open(file_path, 'r') as f:
        lines = f.readlines()

    srt_format = ""

    for i in range(0, len(lines), 2):
        index = i // 2 + 1
        start_time = lines[i].strip()
        end_time = lines[i+2].strip() if i+2 < len(lines) else "0:00"
        content = lines[i+1].strip()

        start_time = "00:" + start_time + ",000" 
        end_time = "00:" + end_time + ",000" 


        srt_format += f"{index}\n{start_time} --> {end_time}\n{content}\n\n"

    saved_path = os.path.join(SRT_FOLDER_PATH, f'{file_name}.srt')
    print(saved_path)
    with open(saved_path, 'w') as f:
        f.write(srt_format)

# split by tokens
def _split_srt_into_files_by_tokens(file_path, max_tokens_per_file=500):
    file_name = _get_filename_without_extension(file_path)
    print(f"🚀 Start to split {file_name} srt files!")
    saved_folder_path = _make_folder_if_needed(TRANSLATION_SPLITING_EN_FOLDER, file_name)

    # 读取SRT文件
    subs = pysrt.open(file_path)

    # 初始化
    current_file = pysrt.SubRipFile()
    current_tokens = 0
    file_index = 0

    for sub in subs:
        tokens_in_chunk = _num_tokens_from_string(sub.text)  # 使用你的函数计算chunk中的token数量

        # 如果当前文件中的token数量加上新chunk中的token数量超过了限制
        if current_tokens + tokens_in_chunk > max_tokens_per_file:
            # Write the current file
            file_path = os.path.join(saved_folder_path, f'split_file{file_index}.srt')
            current_file.save(file_path, encoding='utf-8')

            # 开始新的文件
            current_file = pysrt.SubRipFile()
            current_file.append(sub)  # Add the current chunk to the new file
            current_tokens = tokens_in_chunk
            file_index += 1
        else:
            # 否则，将新chunk添加到当前文件
            current_file.append(sub)
            current_tokens += tokens_in_chunk

    # 添加最后一个文件
    if current_file:
        file_path = os.path.join(saved_folder_path, f'split_file{file_index}.srt')
        current_file.save(file_path, encoding='utf-8')

    print(f"🤩 Finish to split {file_name} srt files!")
    return saved_folder_path


def _split_chunks_into_files(chunks, max_tokens_per_file):
    files = []
    current_file = []
    current_tokens = 0

    for chunk in chunks:
        tokens_in_chunk = _num_tokens_from_string(chunk)  # 使用你的函数计算chunk中的token数量

        # 如果当前文件中的token数量加上新chunk中的token数量超过了限制
        if current_tokens + tokens_in_chunk > max_tokens_per_file:
            # 确保当前文件中至少有一个chunk
            if current_file:
                # 将当前文件添加到文件列表中
                files.append("\n\n".join(current_file))
                # 开始新的文件
                current_file = [chunk]
                current_tokens = tokens_in_chunk
            else:
                # 如果一个chunk的token数量就超过了限制，那么我们仍然需要将它放入一个文件中
                files.append(chunk)
                current_file = []
                current_tokens = 0
        else:
            # 否则，将新chunk添加到当前文件
            current_file.append(chunk)
            current_tokens += tokens_in_chunk

    # 添加最后一个文件
    if current_file:
        files.append("\n\n".join(current_file))

    return files

# split by nums
def _split_srt_file(file_path, split_length):
    file_name = _get_filename_without_extension(file_path)
    print(f"🚀 Start to splt {file_name} srt files!")
    with open(file_path, 'r') as file:
        lines = file.readlines()
    my_str = ''
    for line in lines:
        my_str += line 
    print(my_str[:50])
    print(f'🤯 一共是 {_num_tokens_from_string(my_str)} !') 
    saved_folder_path = _make_folder_if_needed(TRANSLATION_SPLITING_EN_FOLDER, file_name)
    i = 0
    file_count = 1
    while i < len(lines):
        chunk = lines[i:i+split_length*4]  # 因為每個 index 包括 4 行（序號、時間戳、內容、空行），所以要乘以 4
        file_path = os.path.join(saved_folder_path, f'split_file{file_count}.srt')
        with open(file_path, 'w') as output_file:
            output_file.writelines(chunk)
        i += split_length*4
        file_count += 1
    print(f"🤩 Finish to splt {file_name} srt files!")
    return saved_folder_path

def convert_all_srts():
    all_file_paths = _get_all_files_in_directory(TXT_FOLDER_PATH)
    for file_path in all_file_paths:
        _convert_to_srt(file_path)
    file_paths = _get_all_files_in_directory(ORIGINAL_EN_SRTS_FOLDER)
    for file_path in file_paths:
        _split_srt_into_files_by_tokens(file_path, max_tokens_per_file=150)
        # _split_srt_file(file_path, 1000)
    
# convert_all_srts()