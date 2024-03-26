import os
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor
import glob

text = 'Pinkoi - 蔡宗嶧\n0937722898'

def add_text_to_image(image_path):
    # 加载图片
    image = Image.open(image_path).convert("RGBA")
    
    # 创建一个透明的图层来绘制文字
    txt_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))

    # 字体配置
    font_path = "/System/Library/Fonts/PingFang.ttc"  # 字体路径
    font_size = 40  # 字体大小
    font = ImageFont.truetype(font_path, font_size)
    
    # 创建一个可以在上面绘制的对象
    d = ImageDraw.Draw(txt_layer)
    
    # 设置文字颜色和透明度
    text_color = (255, 255, 255, 76)  # 白色文字，透明度约为 30%
    
    # 获取文字尺寸
    text_width, text_height = d.textsize(text, font=font)
    
    # 计算文字位置
    x = (image.width - text_width) - 100
    y = (image.height - text_height) - 100
    
    # 在透明图层上绘制文字
    d.text((x, y), text, font=font, fill=text_color)
    
    # 合并原始图片和透明图层
    combined = Image.alpha_composite(image, txt_layer).convert("RGB")
    
    # 直接替换原图
    combined.save(image_path, "JPEG")

    image_basename = os.path.basename(image_path)
    image_basename_without_ext = os.path.splitext(image_basename)[0].lower()
    print(f"finish draw {image_basename}")

def find_images_in_subdirectories(source_folder):
    # 支持的图片文件扩展名列表
    supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    found_images = []

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if any(file.lower().endswith(ext) for ext in supported_extensions):
                found_images.append(os.path.join(root, file))

    return found_images

def process_images_multithreaded(source_folder):
    # 获取所有图片路径
    image_paths = find_images_in_subdirectories(source_folder)
    for image_path in image_paths:
        add_text_to_image(image_path)
    # 使用ThreadPoolExecutor处理图片
    # with ThreadPoolExecutor() as executor:
    #     executor.map(add_text_to_image, image_paths)

# 使用示例
source_folder = '/Users/chunghanhsin/Documents/Pinkoi-蔡宗嶧/MainCourse/PPT'  # 更新为您的源文件夹路径
process_images_multithreaded(source_folder)
