import openai
import os
import time
import shutil

CH_SUMMARY_TEXTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/summary_manager/ch_summary_texts'
EN_SUMMARY_TEXTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/summary_manager/en_summary_texts'
TXT_FOLDER_PATH = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/translate_srt_manager/original_en_txts'
ARCHIVED_EN_SUMMARY_TEXTS_FOLDER = '/Users/chunghanhsin/Documents/YoutubeCaptionCrawler/summary_manager/archived_en_summary_texts'

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

def _calculate_files(under_dir):
    file_count = 0
    for root, dirs, files in os.walk(under_dir):
        file_count += len(files)
    return file_count

def _get_filename_without_extension(file_path):
    base_name = os.path.basename(file_path)
    file_name_without_extension, _ = os.path.splitext(base_name)
    return file_name_without_extension

openai.api_key = "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"

def _move_all_files_to_en_summary_texts_folder():
    file_paths = _get_all_files_in_directory(ARCHIVED_EN_SUMMARY_TEXTS_FOLDER)
    for file_path in file_paths:
        _move_file(file_path, EN_SUMMARY_TEXTS_FOLDER)


def _translate_by_chat_api(text, completion_block=None):
    max_retries = 10
    retries = 0

    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-0125-preview",
                # model="gpt-4-0613",
                # model="gpt-3.5-turbo-16k-0613",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant, an expert in computer science, particularly well-versed in iOS and architectural design. Your next task is to help translate English contents of a lecture on architectural design."},
                    {"role": "user", 
                        "content": f"Translate the following English contents to Traditional Chinese not Simpleified Chinese, but do not translate the technical terms of computer science, and people's name. Please retain the original content format: {text}"},
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
        print(f"👋 Request completed successfully! Now moving file: {file_name}")
        _move_file(text_file_path, ARCHIVED_EN_SUMMARY_TEXTS_FOLDER)
        remained_files = _calculate_files(EN_SUMMARY_TEXTS_FOLDER)
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

def do_translate_process():
    print("🚀 Start to translate all english summarizes!")
    # _move_all_files_to_en_summary_texts_folder()
    file_paths = _get_all_files_in_directory(EN_SUMMARY_TEXTS_FOLDER)
    for file_path in file_paths:
        file_name = _get_filename_without_extension(file_path)
        print(f"🚀 Start to translate {file_name}!")
        with open(file_path, 'r') as file:
            content = file.read()
        completion_block = make_completion_function(file_path)
        translation = _translate_by_chat_api(content, completion_block=completion_block)
        saved_file_path = os.path.join(CH_SUMMARY_TEXTS_FOLDER, f'{file_name}.txt')
        with open(saved_file_path, 'w') as file:
            file.write(translation)
            print(f"🤩 Finish to translate {file_name}!")
    print("🤩 Finish to translate all english summarizes!")

# do_translate_process()



