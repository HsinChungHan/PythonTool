import opencc
import os

def convert_under_folder(folder_path):
    # 创建转换器，s2t 表示简体中文转繁体中文
    converter = opencc.OpenCC('s2t')
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            # 检查是否为 .srt 文件
            # 检查文件是否以 '._' 开头，如果是，则跳过
            if filename.startswith('._'):
                continue
            source_file = os.path.join(foldername, filename)
            # 读取 .srt 文件
            with open(source_file, 'r', encoding='utf-8') as file:
                srt_text = file.read()

            # 转换文本
            srt_text = converter.convert(srt_text)

            # 写入新的 .srt 文件
            with open(source_file, 'w', encoding='utf-8') as file:
                file.write(srt_text)