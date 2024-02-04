import glob

import cv2

import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

def out_video(fps):
    img_array = []
    for filename in sorted(glob.glob("ascii_image/*.png"), key=natural_keys):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    name = 'project.mp4'
    out = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()