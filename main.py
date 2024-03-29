"""
Copyright(c) 2020 Tatsuro Watanabe
License: MIT
https://github.com/ktpcschool/imageToAscii
"""

import os
import glob
import re

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from youtube import get_youtube_frame
import png_to_mp4

# 文字の濃度を取得
def get_concentration_of_character(character, input_font, width, height):
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), character, font=input_font, fill=(255, 255, 255))
    pixel = [image.getpixel((x, y)) for y in range(height) for x in range(width)]
    n = sum(x == (0, 0, 0) for x in pixel)
    return n / len(pixel)


# 画像をアスキーアートに変換
def image_to_ascii(input_image, sorted_character_list, input_font):
    input_image = input_image.convert('RGB')
    gray_img = input_image.convert('L')
    width, height = input_image.size
    output_image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(output_image)
    list_length = len(sorted_character_list)
    n = 256 / list_length
    font_size = input_font.size
    for y in range(0, height, font_size):
        for x in range(0, width, font_size):
            gray = gray_img.getpixel((x, y))
            index = int(gray / n)
            character = sorted_character_list[index][0]
            r, g, b = input_image.getpixel((x, y))
            draw.text((x, y), character, font=input_font, fill=(r, g, b))
    return output_image


def convert(frame_num):
    characters = '@*+-=[]~^%&qopigbdsca '  # アスキーアートに使用する文字列
    sample_file = Image.open(f'frame/frame32.jpg')
    width, height = sample_file.size
    division = 100  # 分割数
    size = 2000
    height = int(height * size / width)
    width = size
    font = 'font/ipaexg.ttf'  # アスキーアートに使用するフォント
    font_size_to_get_concentration = 256
    encoding = 'utf-8'
    font_width, font_height = 256, 256
    font_to_get_concentration = ImageFont.truetype(font, font_size_to_get_concentration, encoding=encoding)
    character_dict = \
        {character: get_concentration_of_character(character, font_to_get_concentration, font_width, font_height)
         for character in characters}
    sorted_character_list = sorted(character_dict.items(), key=lambda x: x[1])
    print(sorted_character_list)
    font_size = width // division
    input_font = ImageFont.truetype(font, font_size, encoding=encoding)

    ascii_art = "ascii_art"
    if not(os.path.isdir(ascii_art)):
       os.mkdir(ascii_art)
    #動画のフレーム分アスキーアート変換
    for i in range(frame_num):
        input_file = f'frame/frame{i}.jpg'  # 変換する画像ファイル
        input_file_without_ext = os.path.splitext(os.path.basename(input_file))[0]
        output_file = 'ascii_art/ascii_' + input_file_without_ext + '.png'  # 変換後の画像ファイル
        input_image = Image.open(input_file)
        input_image = input_image.resize((width, height))
        output_image = image_to_ascii(input_image, sorted_character_list, input_font)
        output_image.show()
        output_image.save(output_file)
    
    print("asciiに変換完了しました")


if __name__ == '__main__':
    video_url = "https://youtu.be/sLQEunI7p5s?si=DgfbdylA0XbSfv7V"
    frame_num,fps = get_youtube_frame(video_url)
    convert(frame_num)
    #png_to_mp4.out_video(fps)