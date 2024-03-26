import os
import re
import openai
import time
 
import tiktoken



CLEANED_EN_TEXTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/summary_manager/cleaned_en_txts'
CH_SUMMARY_TEXTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/summary_manager/ch_summary_texts'
EN_SUMMARY_TEXTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/summary_manager/en_summary_texts'
ORIGINAL_EN_SRTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/original_en_srts'
ARCHIVED_EN_SRTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/archived_en_srts'
TXT_FOLDER_PATH = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/original_en_txts'

# 16385
MAX_TOKEN_SIZE = 15000
# 只需要有 english 的 SRT 就可以生成 summary

def _num_tokens_from_string(string: str, encoding_name: str='gpt-3.5-turbo') -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def _get_filename_without_extension(file_path):
    base_name = os.path.basename(file_path)
    file_name_without_extension, _ = os.path.splitext(base_name)
    return file_name_without_extension

def _remove_timestamp(srt_text):
    cleaned_text = re.sub(r'\d{2}:\d{2}:\d{2}.\d{3} --> \d{2}:\d{2}:\d{2}.\d{3}', '', srt_text)
    # 使用正則表達式移除序號
    cleaned_text = re.sub(r'^\d+\n', '', cleaned_text, flags=re.MULTILINE)
    return cleaned_text

def _split_txt_file(file_path, text):
    # 找到換行符的總數
    total_newlines = text.count('\n')

    # 找到中間的換行符的位置
    midpoint = total_newlines // 2

    # 找到第 midpoint 個換行符的位置
    start_index = 0
    for _ in range(midpoint):
        start_index = text.index('\n', start_index) + 1

    # 找到第 midpoint+1 個換行符的位置
    end_index = text.index('\n', start_index)
    # 分成兩份文件內容
    part1 = text[:end_index]
    part2 = text[end_index+1:]  # 不包含換行符
    part1_output_file_path = os.path.join(CLEANED_EN_TEXTS_FOLDER, _get_filename_without_extension(file_path) + "_part1.txt")

    part2_output_file_path = os.path.join(CLEANED_EN_TEXTS_FOLDER, _get_filename_without_extension(file_path) + "_part2.txt")

    print('將兩份文件內容寫入新的txt文件中')
    # 將兩份文件內容寫入新的txt文件中
    with open(part1_output_file_path, 'w', encoding='utf-8') as file1:
        file1.write(part1)

    with open(part2_output_file_path, 'w', encoding='utf-8') as file2:
        file2.write(part2)

    print("已成功將文件分成兩份，並存儲為part1.txt和part2.txt。")

def clean_index_from_srts():
    for file_name in os.listdir(ARCHIVED_EN_SRTS_FOLDER):
        if file_name.endswith(".srt"):
            srt_file_path = os.path.join(ARCHIVED_EN_SRTS_FOLDER, file_name)
            with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
                srt_text = srt_file.read()

            cleaned_text = _remove_timestamp(srt_text)

            if _num_tokens_from_string(cleaned_text) > MAX_TOKEN_SIZE:
                _split_txt_file(srt_file_path, cleaned_text)
                continue

            output_file_path = os.path.join(CLEANED_EN_TEXTS_FOLDER, _get_filename_without_extension(file_name) + ".txt")
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(cleaned_text)
            
            
openai.api_key = "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"
def _summary(text, completion_block=None):
    max_retries = 10
    retries = 0

    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                # 'gpt-3.5-turbo-16k-0613'
                model="gpt-4-0613",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant, an expert in computer science, particularly well-versed in iOS and architectural design. Your next task is to help summarize English subtitles of a lecture on architectural design."},
                    {"role": "user", 
                        "content": f"Using a numbered list to summarize the the following English conversation between the two individuals in a concise manner and it must not exceed 2000 words: {text}",
                    }
                ]
            )
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

def _calculate_files(under_dir):
    file_count = 0
    for root, dirs, files in os.walk(under_dir):
        file_count += len(files)
    return file_count

def make_completion_function(text_file_path):
    def completion_function(response):
        if response is None:
            return
        file_name = _get_filename_without_extension(text_file_path)
        print(f"👋 Request completed successfully! Now deleting file: {file_name}")
        os.remove(text_file_path)
        remained_files = _calculate_files(CLEANED_EN_TEXTS_FOLDER)
        print(f"🥰 Remained {remained_files} files!")
        # Add code here to delete the file
    return completion_function


def _get_all_files_in_directory(dir_path):
    all_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file == '.DS_Store':
                continue
            all_files.append(os.path.join(root, file))
    return all_files

def do_summary_srts_process():
    print("🚀 Start to clean all en srts!")
    # clean_index_from_srts()
    print("🤩 Finish to clean all en srts!")
    print("🚀 Start to summarize all srts!")
    file_paths = _get_all_files_in_directory(CLEANED_EN_TEXTS_FOLDER)
    for file_path in file_paths:
        completion_block = make_completion_function(file_path)
        file_name = _get_filename_without_extension(file_path)
        print(f"🚀 Start to summarize {file_name}!")
        with open(file_path, 'r') as file:
            content = file.read()
        summary = _summary(content, completion_block=completion_block)
        if summary is None:
            continue
        saved_file_path = os.path.join(EN_SUMMARY_TEXTS_FOLDER, f'{file_name}.txt')
        with open(saved_file_path, 'w') as file:
            file.write(summary)
            print(f"🤩 Finish to summarize {file_name}!")
    print("🤩 Finish to summarize all srts!")

# do_summary_srts_process()