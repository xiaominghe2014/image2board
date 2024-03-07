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

from PIL import Image, ImageFilter

def file_to_save_path(image_path,save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    return os.path.join(save_dir, os.path.basename(image_path))

def grayscale_image(image_path,save_dir):
    """
    将图片转换为灰度图像。
    
    参数:
    image_path (str): 图片的路径。
    """
    image = Image.open(image_path)
    grayscale_image = image.convert('L')
    save_path = file_to_save_path(image_path,save_dir)
    grayscale_image.save(save_path)
    return save_path

def binarize_image(image_path, save_dir, threshold=128):
    """
    将图片二值化。
    
    参数:
    image_path (str): 图片的路径。
    threshold (int): 二值化阈值。
    """
    image = Image.open(image_path)
    binarized_image = image.convert('L').point(lambda x: 0 if x<threshold else 255, '1')
    save_path = file_to_save_path(image_path,save_dir)
    binarized_image.save(save_path)
    return save_path

def apply_filter(image_path, save_dir,filter_type=ImageFilter.GaussianBlur(5)):
    """
    应用滤波器处理图像。
    
    参数:
    image_path (str): 图片的路径。
    filter_type (ImageFilter): 应用的滤波器类型。
    """
    image = Image.open(image_path)
    filtered_image = image.filter(filter_type)
    save_path = file_to_save_path(image_path,save_dir)
    filtered_image.save(save_path)
    return save_path

def preprocess_image(image_path, save_dir, preprocess_steps=['grayscale', 'binarize', 'filter']):
    """
    对图像进行预处理，包括灰度化、二值化和滤波等步骤，以减少噪声并突出特征。
    
    参数:
    image_path (str): 图片的路径。
    preprocess_steps (list): 预处理步骤列表。
    """
    for step in preprocess_steps:
        if step == 'grayscale':
            image_path = grayscale_image(image_path,save_dir)
        elif step == 'binarize':
            image_path = binarize_image(image_path,save_dir)
        elif step == 'filter':
            image_path = apply_filter(image_path,save_dir)
    print(f'预处理完成，保存到{image_path}')

# 查找指定目录下的所有jpeg格式图片
def find_jpeg_images(directory):
    """
    查找指定目录下的所有webp格式图片。

    参数:
    directory (str): 要搜索的目录路径。

    返回:
    list: 找到的图片文件的路径列表。
    """
    images = []
    # 遍历指定目录及其子目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.jpeg'):
                images.append(os.path.join(root, file))
    return images

print(f'指定目录{sys.argv[1]} 预处理到 {sys.argv[2]}')
jpeg_images = find_jpeg_images(sys.argv[1])
for jpeg_image in jpeg_images:
    preprocess_image(jpeg_image,sys.argv[2],preprocess_steps=['grayscale', 'binarize'])


