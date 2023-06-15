import os
import orjson
import cv2
import numpy as np
import pygetwindow as gw
from PIL import ImageGrab, Image
import mss
CONFIG_FILE_NAME = "config.json"


def take_screenshot(winname, points=(0, 0, 0, 0)):
    """
    说明:
        返回RGB图像
    参数:
        :param points: 图像截取范围
    """
    window = gw.getWindowsWithTitle(winname)
    window = window[0]
    # b不如全屏截图
    scaling = 1.5
    left, top, right, bottom = int(window.left * scaling), int(window.top * scaling), int(window.right * scaling), int(
        window.bottom * scaling)
    temp = ImageGrab.grab((left, top, right, bottom))
    # temp = ImageGrab.grab()
    # print(left, top, right, bottom)
    width, length = temp.size
    screenshot = np.array(temp)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)
    return (screenshot, left, top, right, bottom, width, length)


left, top, right, bottom = 0, 0, 2560, 1600
monitor = {'left': left, 'top': top, 'width': right, 'height': bottom}
cap = mss.mss()
def take_fullscreenshot():
    """
    说明:
        返回RGB图像

    """
    screenshot = cv2.cvtColor(np.array(cap.grab(monitor)), cv2.COLOR_BGRA2BGR)  # 获取图片
    # print(left, top, right, bottom)
    width, length = screenshot.shape[:2]
    return (screenshot, width, length)


def scan_screenshot(prepared: np, winnmae) -> dict:
    """
    说明：比对图片
    参数：:param prepared: 比对图片地址
        :param winnmae: 截图窗口
    """
    screenshot, width, length = take_fullscreenshot()
    # cv2.imshow('screenshot', screenshot)
    # cv2.waitKey()
    result = cv2.matchTemplate(screenshot[1200:,:,:], prepared, cv2.TM_CCORR_NORMED)
    # cv2.imshow( 'result',result)
    length, width, _ = prepared.shape
    length = int(length)
    width = int(width)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return {
        # "screenshot": screenshot,
        "min_val": min_val,
        "max_val": max_val,
        "min_loc": (min_loc[0] + left + (width / 2), min_loc[1] + top + (length / 2)),
        "max_loc": (max_loc[0] + left + (width / 2), max_loc[1] + top + (length / 2)),
    }
