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
import time
import math
import objc
from AppKit import NSWorkspace, NSColor, NSBezierPath
import pyautogui
import Quartz
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
import Cocoa
import AppKit

def find_front_window_by_app_name(app_name):
    # 获取 NSWorkspace 实例
    running_apps = NSWorkspace.sharedWorkspace().activeApplication()

    # 获取所有运行中的应用程序
    # running_apps = workspace.runningApplications()

    # 遍历应用程序列表，查找具有指定名称的应用程序
    for app in running_apps:
        windows = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
        # 获取应用程序的窗口
        for window in windows:
            if window['kCGWindowLayer'] == 0:
                if window['kCGWindowOwnerName'] == app_name:
                    return window
                else:
                    return None
            # if app.localizedName() == app_name:
    # 如果没有找到具有指定名称的应用程序，返回 None
    return None

def draw_circle(circle_center, window_rect):
    bounds = Quartz.CGRectMake(window_rect[0], window_rect[1], window_rect[2], window_rect[3])
    blue_color = (0.0, 0.67, 1.0, 0.5)
    circle_context = Quartz.CGBitmapContextCreate(None, int(bounds.size.width), int(bounds.size.height), 8, 0, Quartz.CGColorSpaceCreateDeviceRGB(), Quartz.kCGImageAlphaPremultipliedLast)    
    Quartz.CGContextSetRGBFillColor(circle_context, blue_color[0], blue_color[1], blue_color[2], blue_color[3])
    Quartz.CGContextBeginPath(circle_context)
    Quartz.CGContextAddArc(circle_context, circle_center[0], circle_center[1], 10, 0, 2 * math.pi, False)
    Quartz.CGContextClosePath(circle_context)
    Quartz.CGContextDrawPath(circle_context, Quartz.CGPathDrawingMode(Quartz.kCGPathFill))
    Quartz.CGContextRelease(circle_context)
    return None

def monitor_window(app_name):
    while True:
        try:
            window = find_front_window_by_app_name(app_name)
            #在 find_front_window_by_app_name 函数中，可以通过判断窗口的 kCGWindowLayer 是否为 0 来确定当前窗口是否处于活动状态（即当前窗口是否在最上层）
            if window is not None:
                for key, value in window.items():
                    print(f'{key} -> {value}')
                # 获取窗口的位置和大小
                window_rect = (window['kCGWindowBounds']['X'], window['kCGWindowBounds']['Y'], window['kCGWindowBounds']['Width'], window['kCGWindowBounds']['Height'])
                # 计算窗口中心点
                center_x = window_rect[0] + window_rect[2] // 2    
                center_y = window_rect[1] + window_rect[3] // 2
                circle_center = (center_x, center_y)
                print(f'{circle_center}')
                # TODO FIX 在中心点画一个蓝色半透明实心小圆
                draw_circle(circle_center, window_rect)
                screenshot = pyautogui.screenshot(region=(window_rect[0], window_rect[1], window_rect[2], window_rect[3]))
                screenshot.save('board_temp.png')
                # TODO 根据棋盘进行AI分析,并在window上显示分析的点的详细信息
            else:
                pass
        except IndexError:
            print("未找到指定窗口")
        time.sleep(1)  # 每隔1秒检查一次

if __name__ == "__main__":
    app_name = sys.argv[1]
    print(f'{app_name}')
    monitor_window(app_name)