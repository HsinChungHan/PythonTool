import cv2
import pysrt
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
from multiprocessing import Process
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor


def capture_frame_with_subtitle(video_path, srt_path, output_folder):
    # 加载字幕文件
    subs = pysrt.open(srt_path)

    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file {video_path}")
        return

    # 字体配置
    font_path = "/System/Library/Fonts/PingFang.ttc"  # 字体路径
    font_size = 40  # 字体大小
    font = ImageFont.truetype(font_path, font_size)

    for i, sub in enumerate(subs):
        # 字幕结束时间转换为毫秒
        end_time_ms = (sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds

        # 跳转到字幕结束时间
        cap.set(cv2.CAP_PROP_POS_MSEC, end_time_ms)

        # 读取帧
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to capture frame at {end_time_ms}ms")
            continue

        # 将BGR帧转换为RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)

        # 绘制字幕
        draw = ImageDraw.Draw(pil_img)
        font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 40)
        
        text = sub.text
        # 繪製白色的字體
        text_width, text_height = draw.textsize(text, font=font)
        # text_width, text_height = font.getsize(text)
        x_center = (frame.shape[1] - text_width) / 2
        y_center = frame.shape[0] - 100 + (100 - text_height) / 2 - 20

        # 繪製黑色的邊框
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            draw.text((x_center + dx, y_center + dy), text, font=font, fill="black")
        
        # 繪製白色的字體
        draw.text((x_center, y_center), text, font=font, fill="white")

        # 将修改后的图像转换回OpenCV格式
        cv2_frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        # 格式化文件名为 时间（分：秒）
        end_time_formatted = f"{sub.end.minutes:02d}-{sub.end.seconds:02d}"
        output_path = os.path.join(output_folder, f"{end_time_formatted}.jpg")

        # 保存截图
        cv2.imwrite(output_path, cv2_frame)
        print(f"Saved frame with subtitle to {output_path}")

    # 完成后释放视频捕获
    cap.release()


def _get_subdirectories(base_dir_path):
    subdirs = []
    for subdir, dirs, files in os.walk(base_dir_path):
        for dir in dirs:
            subdirs.append(os.path.join(subdir, dir))
    return subdirs

def _find_files_with_extension(folder, extension):
    """找到指定資料夾中的所有指定副檔名的檔案。"""
    for dirpath, _, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith(extension):
                yield os.path.join(dirpath, filename)

def _create_srt_dictionary(srts_path):
    srt_dict = {}
    for file_path in srts_path:
        # 获取文件名
        file_basename = os.path.basename(file_path)
        file_name_without_ext = os.path.splitext(file_basename)[0].lower()
        # 将文件名作为字典的键，文件路径作为值
        srt_dict[file_name_without_ext] = file_path
    return srt_dict

def _merge_screenshot_and_srt(folder_path):
    """複製 A 和 B 資料夾中檔名相同的 .mkv 和 .srt 檔案到目標資料夾。"""
    
    # 找到 A, B 資料夾中的所有 .mkv 和 .srt 檔案
    mkv_files = list(_find_files_with_extension(folder_path, '.mp4'))
    srt_files = list(_find_files_with_extension(folder_path, '.srt'))
    srt_files_dict = _create_srt_dictionary(srt_files)
    # print(srt_files_dict)

    # 比對檔名
    for mkv_file in mkv_files:
        mkv_basename = os.path.basename(mkv_file)
        mkv_name_without_ext = os.path.splitext(mkv_basename)[0].lower()
        print(mkv_basename)
        if mkv_name_without_ext in srt_files_dict:
            mkv_basename = os.path.basename(mkv_file)
            mkv_name_without_ext = os.path.splitext(mkv_basename)[0].lower()
            folder_path = os.path.dirname(mkv_file)
            output_folder = os.path.join(folder_path, 'screenshots', mkv_name_without_ext)

            # 检查 output_folder 是否存在
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)  # 仅当文件夹不存在时创建
            else:
                print(f"Folder '{output_folder}' already exists.")

            srt_file_path = srt_files_dict[mkv_name_without_ext]
            mkv_file_path = mkv_file
            capture_frame_with_subtitle(mkv_file_path, srt_file_path, output_folder)
            print(f"🚀 Start to make screenshot {mkv_name_without_ext}")

def do_video_scrrenshot_process(src_folder_path):
    sub_folders_paths = _get_subdirectories(src_folder_path)
    for folder_path in sub_folders_paths:
        _merge_screenshot_and_srt(folder_path)


def _merge_screenshot_and_srt_multi_thread(folder_path):
    # 找到所有 .mkv 和 .srt 文件
    mkv_files = list(_find_files_with_extension(folder_path, '.mp4'))
    srt_files = list(_find_files_with_extension(folder_path, '.srt'))
    srt_files_dict = _create_srt_dictionary(srt_files)
    print("I am here")
    with ThreadPoolExecutor(max_workers=24) as executor:  # 调整max_workers以适应您的系统
        futures = []

        for mkv_file in mkv_files:
            mkv_basename = os.path.basename(mkv_file)
            mkv_name_without_ext = os.path.splitext(mkv_basename)[0].lower()
            
            if mkv_name_without_ext in srt_files_dict:
                folder_path = os.path.dirname(mkv_file)
                output_folder = os.path.join(folder_path, 'screenshots', mkv_name_without_ext)

                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                else:
                    print(f"Folder '{output_folder}' already exists.")

                srt_file_path = srt_files_dict[mkv_name_without_ext]
                mkv_file_path = mkv_file
                
                future = executor.submit(capture_frame_with_subtitle, mkv_file_path, srt_file_path, output_folder)
                futures.append(future)

        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error processing task: {e}")

def do_video_scrrenshot_process_multi_thread(src_folder_path):
    sub_folders_paths = _get_subdirectories(src_folder_path)
    sub_folders_paths.append(src_folder_path)
    with ThreadPoolExecutor(max_workers=24) as executor:
        futures = [executor.submit(_merge_screenshot_and_srt_multi_thread, folder_path) for folder_path in sub_folders_paths]
        for future in futures:
            try:
                result = future.result()
            except Exception as e:
                print(f"Error processing task: {e}")        
    


SRC_FOLDER_PATH = '/Users/chunghanhsin/Documents/Pinkoi-蔡宗嶧/MainCourse/Ch6_bonus_live_adding_a_new_feature'
# do_video_scrrenshot_process(SRC_FOLDER_PATH)
do_video_scrrenshot_process_multi_thread(SRC_FOLDER_PATH)