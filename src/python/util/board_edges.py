#!/usr/bin/env python3

# Copyright (c) 2024, xiaominghe2014@gmail.com
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import cv2
import numpy as np

def file_to_save_path(image_path,save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    return os.path.join(save_dir, os.path.basename(image_path))

def board_tetect(image_path, save_dir):
    # 读取图片
    image = cv2.imread(image_path)
    # 将图片缩放到宽为800
    # scale_percent = 800 / image.shape[1]
    # width = int(image.shape[1] * scale_percent)
    # height = int(image.shape[0] * scale_percent)
    # dim = (width, height)
    # image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    # 霍夫变换找到棋盘上的线条
    lines = cv2.HoughLinesP(cv2.Canny(gray, 50, 150, apertureSize=3), 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

    horizontal_lines = []
    vertical_lines = []

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x1 == x2:
                vertical_lines.append(line)
            elif y1 == y2:
                horizontal_lines.append(line)
    for line in horizontal_lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)


    for line in vertical_lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
    
    # 高斯模糊
    # blur = cv2.GaussianBlur(gray,(5,5),0)

     # 定义腐蚀的核大小
    kernel = np.ones((6, 6), np.uint8)

    # 腐蚀操作
    erosion = cv2.erode(gray, kernel, iterations=1)

    # 形态学闭运算
    # closing = cv2.morphologyEx(erosion, cv2.MORPH_CLOSE, kernel)


    # 边缘检测
    # edges = cv2.Canny(erosion, 50, 150, apertureSize=3)
    
    # 轮廓提取
    contours, _ = cv2.findContours(erosion, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

   

    # 根据黑白颜色分别设置阈值，得到两个二值图像
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    min_black = np.array([0,0,10])
    max_black = np.array([180,255,90])
    mask_black = cv2.inRange(hsv,min_black,max_black)
    min_white = np.array([0,0,100])
    max_white = np.array([180,30,255])
    mask_white = cv2.inRange(hsv,min_white,max_white)

    # 与运算，将二值图像与原图相与，得到黑子与白子的图像
    r_black = cv2.bitwise_and(image,image,mask = mask_black)
    r_white = cv2.bitwise_and(image,image,mask = mask_white)
    r_black = cv2.cvtColor(r_black,cv2.COLOR_BGR2GRAY)
    r_white = cv2.cvtColor(r_white,cv2.COLOR_BGR2GRAY)


    # 圆检测，找到棋盘上的棋子
    circles1 = cv2.HoughCircles(erosion,method=cv2.HOUGH_GRADIENT,dp=1,minDist=20,param1=50,param2=30,minRadius=10,maxRadius=30)
    circles2 = cv2.HoughCircles(gray,method=cv2.HOUGH_GRADIENT,dp=1,minDist=20,param1=50,param2=30,minRadius=10,maxRadius=30)
    print('circles1:',len(circles1[0]))
    print('circles2:',len(circles2[0]))
    # 合并circles1和circles2为circles
    circles = np.concatenate((circles1[0], circles2[0]), axis=0)

    # 去除圆心相差5像素之内的重复圆
    circles = np.array([c for i, c in enumerate(circles) if all(np.linalg.norm(np.array(c[:2]) - np.array(cc[:2])) > 5 for cc in circles[:i])])
    
    print('circles:',len(circles))
    for i in circles:
        # 圆心
        cx = int(i[0])
        cy = int(i[1])
        # 半径
        r = int(i[2])

        # 判断是否为黑子
        blacks = r_black[cy-r:cy+r,cx-r:cx+r]
        black_cnt = cv2.countNonZero(blacks)
        if black_cnt>30:
            cv2.circle(image,(cx,cy),r,(0,0,255),2)
        else :
            # 判断是否为白子
            whites = r_white[cy-r:cy+r,cx-r:cx+r]
            white_cnt = cv2.countNonZero(whites)
            if white_cnt>30:
                cv2.circle(image,(cx,cy),r,(255,0,0),2)


    save_path = file_to_save_path(image_path,save_dir)
    cv2.imwrite(save_path, image)


def increase_contrast(image_path, save_dir):
    # 读取图片
    image = cv2.imread(image_path)
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 应用高斯模糊
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # 定义腐蚀和膨胀的核大小
    kernel = np.ones((5, 5), np.uint8)

    # 腐蚀操作
    erosion = cv2.erode(gray, kernel, iterations=1)
    # 形态学闭运算
    closing = cv2.morphologyEx(erosion, cv2.MORPH_CLOSE, kernel)

    save_path = file_to_save_path(image_path,save_dir)
    cv2.imwrite(save_path, closing)

# 查找指定目录下的所有jpeg格式图片
def find_jpeg_images(directory):
    """
    查找指定目录下的所有jpeg格式图片。

    参数:
    directory (str): 要搜索的目录路径。

    返回:
    list: 找到的jpeg图片文件的路径列表。
    """
    images = []
    # 遍历指定目录及其子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.jpeg'):
                images.append(os.path.join(root, file))
    return images

print(f'指定目录{sys.argv[1]} 棋盘检测到 {sys.argv[2]}')
jpeg_images = find_jpeg_images(sys.argv[1])
for jpeg_image in jpeg_images:
    print(f'处理 {jpeg_image}')
    board_tetect(jpeg_image,sys.argv[2])
    # increase_contrast(jpeg_image,sys.argv[2])