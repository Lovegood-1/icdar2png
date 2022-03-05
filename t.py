"""
transform the 'txt' annotation in ic15 to 'png' format.

'png' can be used in Paddle
"""
import os
import re
import numpy as np
import cv2
from PIL import Image
from src.utils import label_colormap
flag = 'test'
gt_floder = 'datasets/icdar2015/{}_gts'.format(flag)
img_floder = 'datasets/icdar2015/{}_images'.format(flag)

png_floder_path = os.path.join('datasets/icdar2015', '{}_pngs'.format(flag))
print('write into >>>', png_floder_path)
if os.path.exists(png_floder_path) is False:
    os.mkdir(png_floder_path)

img = cv2.imread('datasets/icdar2015/test_images/img_1.jpg')
a  = 1
# 读取所有文件，开始循环
    # 读取 txt 文件
    # 创建 720, 1280 的图片
    # 读取 某行 开始循环
        # 对
def read_single_txt(gt):
    lines = []

    reader = open(gt, 'r').readlines()
    for line in reader:
        item = {}
        parts = line.strip().split(',')
        label = parts[-1]
        line = [i.strip('\ufeff').strip('\xef\xbb\xbf') for i in parts]
        poly = np.array(list(map(float, line[:8]))).reshape((-1, 2)).tolist()
        item['poly'] = poly
        item['text'] = label
        lines.append(item)
    return lines

def read_all_txt(img_floder,gt_floder, save_floder):
    # colormap = label_colormap(256)
    # all_gt_path = []
    filename_list = os.listdir(gt_floder)  # 获取文件夹路径下的所有目录及文件名
    for i in range(len(filename_list)):   #打印文件路径下的目录及文件名称
        new_path = os.path.join(gt_floder,filename_list[i])    #把目录和文件名合成一个路径
        cost=re.findall(r'[1-9]+\.?[0-9]*',filename_list[i])[0].replace('.','')
        png_path = os.path.join(save_floder,'img_{}.png'.format(cost))  
        if os.path.isfile(new_path):          #判断是否为文件
            annotation = read_single_txt(new_path)
            # 建立
            img_path =os.path.join(img_floder,'img_{}.jpg'.format(cost))  
            size_ = cv2.imread(img_path,-1).shape[:-1]
            png = np.zeros(size_)
            for single_Word in annotation:
                polygon = np.array(single_Word['poly'])
                # polygon2 = np.array(list(map(float, line[:8]))).reshape((-1, 2)).tolist()
                ignore = True if '#' in single_Word['text'] else False
                height = max(polygon[:, 1]) - min(polygon[:, 1])
                width = max(polygon[:, 0]) - min(polygon[:, 0])
                if  min(height, width) < 10 or ignore is True:
                    cv2.fillPoly(png, polygon.astype(np.int32)[np.newaxis, :, :], 255)
                else:
                    cv2.fillPoly(png, polygon.astype(np.int32)[np.newaxis, :, :], 125)
            # res1_PIL = Image.fromarray(png, mode='P')
            # res1_PIL.putpalette((colormap).astype(np.uint8).flatten())
            # res1_PIL.save(png_path)
            cv2.imwrite(png_path,png)
            print(png_path)
            a = 1
read_all_txt(img_floder,gt_floder,png_floder_path)