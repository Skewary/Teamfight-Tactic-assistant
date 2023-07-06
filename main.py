import time
import pyautogui
import cv2
import numpy as np
import os
from pynput import keyboard

# 设置待匹配图片文件夹路径
import win32gui

template_folder = "./template_folder"

# 全局变量，用于标记是否按下了"tab"键
tab_pressed = False

left, top = 0, 0


def capture_window_screenshot(window_title):
    global left,top
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        print("指定窗口未找到")
        return None

    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top

    screenshot = pyautogui.screenshot(region=(left, top, width, height))
    return screenshot


def load_templates(template_folder):
    # 文件一定要英文路径，cv2原因
    templates = {}
    for filename in os.listdir(template_folder):
        template_path = os.path.join(template_folder, filename)
        template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)  # 灰度化处理
        templates[filename] = template
    return templates


def match_templates(screenshot_gray, templates):
    threshold = 0.9  # 设置匹配阈值
    # print(type(templates))
    for filename, template in templates.items():
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= threshold:
            center_x = max_loc[0] + template.shape[1] // 2
            center_y = max_loc[1] + template.shape[0] // 2
            center_location = (center_x, center_y)
            return (filename, center_location)



def perform_actions(match):
    # 根据匹配结果执行相应的鼠标或键盘操作
    global d_pressed
    filename, location = match
    print("匹配到：", filename)
    print("位置：", location)
    # 移动鼠标到匹配位置
    pyautogui.moveTo(location[0]+left, location[1]+top)
    d_pressed = False


def on_press(key):
    global tab_pressed
    if key == keyboard.Key.tab:
        tab_pressed = True


templates = load_templates(template_folder)


def on_release(key):
    global tab_pressed
    if key == keyboard.Key.tab:
        screenshot = capture_window_screenshot(window_title)
        if screenshot is not None:
            screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
            match = match_templates(screenshot_gray, templates)
            if match is not None:
                perform_actions(match)
        tab_pressed = False


def main(window_title):
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    while True:
        time.sleep(0.01)


if __name__ == "__main__":
    window_title = "你要操作的窗口标题"  # 替换为你要操作的窗口标题
    main(window_title)
