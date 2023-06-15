import json

import pyautogui
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController
import keyboard
import ghub.ghub_mouse as ghub
import cv2

from calculated import scan_screenshot

mouse = MouseController()
# keyboard = KeyboardController()
with open('./hero.json', 'r', encoding='utf-8')as f:
    heros = json.load(f)  # 加载英雄与ID
with open('./config.json', 'r', encoding='utf-8')as f:
    config = json.load(f)  # 加载策略组，可以在config.json配置
aims = config['梭哈提莫、加里奥、崔丝塔娜、波比']  # 选择策略
aim_heros = []
for aim in aims:
    img = cv2.imread(r'./lol250/' + str(heros[aim]) + '.jpg')
    aim_heros.append(img)
    # cv2.imshow( str(heros[aim]),img)
    # cv2.waitKey()


def find():
    for index, aim_hero in enumerate(aim_heros):
        # result = scan_screenshot(aim_hero,'Google Chrome')
        result = scan_screenshot(aim_hero, '照片')
        if result['max_val'] > 0.96:
            print(aims[index], heros[aims[index]], "相似度：", result['max_val'])
            # cv2.imshow(str(index), aim_hero)
            # cv2.waitKey()
            print("目标", result['max_loc'], mouse.position)
            mouse_pos_x, mouse_pos_y = mouse.position
            x_center, y_center = result['max_loc']
            rel_x = x_center - mouse_pos_x
            rel_y = y_center + 1200 - mouse_pos_y # 识别只识别屏幕下半部分，1200：1600
            ghub.mouse_xy(round(rel_x * 0.4), round(rel_y * 0.4))


if __name__ == '__main__':
    print('查找')
    print(aims)
    while True:
        keyboard.wait('d')
        find()
