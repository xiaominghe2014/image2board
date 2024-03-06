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

def detect_chessboard_edges(image_path,save_dir):
    """
    使用霍夫变换检测围棋棋盘图片的直线，定位棋盘的边界和网格。
    
    参数:
    image_path (str): 围棋棋盘图片的路径。
    """
    # 读取图片
    image = cv2.imread(image_path)
    # 转换为灰度图
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 使用Canny算法检测边缘
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # 使用霍夫变换检测直线
    lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
    # 在原图上绘制检测到的直线
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    # 保存绘制了直线的图片
    save_path = file_to_save_path(image_path,save_dir)
    cv2.imwrite(save_path, image)
    return save_path

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
    detect_chessboard_edges(jpeg_image,sys.argv[2])