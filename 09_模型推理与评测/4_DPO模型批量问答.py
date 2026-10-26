import pyautogui
import pyperclip
from time import sleep
import platform
import random
import pandas as pd

users = list(pd.read_csv('3000.csv')['用户'])
sen = '魏源的华夷关系观念脱胎于何休的哪个理论？'
sen2 = '刘向对于神明的看法是什么？'
x = users.index(sen)
y = users.index(sen2)
print(x, y)
cnt_lis = users[x:y+1]

def get_current_text_before_cursor():
    # 获取鼠标光标的位置
    x, y = pyautogui.position()
    print(x, y)
    # 移动鼠标到光标位置
    pyautogui.moveTo(x, y)
    sleep(0.5)
    # 模拟鼠标左键点击两次
    pyautogui.click(clicks=2)
    pyautogui.keyDown('command')
    sleep(0.2)
    pyautogui.press('c')
    pyautogui.keyUp('command')
    copied_text = pyperclip.paste()
    return copied_text

def auto_qa(cnt_lis):
    sleep(3)
    flag = 0
    for i in cnt_lis:
        flag += 1
        print(flag)
        # ipt = input('输入：')
        # print(ipt, type(ipt))
        # if ipt:
        #     print('等待')
        #     sleep(60)
        # current_text = get_current_text_before_cursor()
        # print(current_text)
        #
        # if "\n" not in current_text:

        #     # 如果光标前不包含 "users:"，则 sleep(40)
        #     print('等待')
        #     sleep(80)

        if flag % 50 == 0:
            pyautogui.keyDown('ctrl')
            sleep(0.2)
            pyautogui.press('d')
            pyautogui.keyUp('ctrl')
            sleep(5)
            print('进程终止')
            new = 'CUDA_VISIBLE_DEVICES=0 python src/cli_demo.py --model_name_or_path /home/pgrad/jef/Baichuan2-7B-Chat --template baichuan2 --finetuning_type lora --checkpoint_dir /home/pgrad/jef/Dpo'
            pyperclip.copy(new)
            if platform.system() == 'Windows':
                pyautogui.keyDown('ctrl')
                pyautogui.press('v')
                pyautogui.keyUp('ctrl')
            elif platform.system() == 'Darwin':
                pyautogui.keyDown('command')
                sleep(0.2)
                pyautogui.press('v')
                pyautogui.keyUp('command')
            pyautogui.press('enter')
            sleep(120)
            print('重启成功')

        pyperclip.copy(i)

        if platform.system() == 'Windows':
            pyautogui.keyDown('ctrl')
            pyautogui.press('v')
            pyautogui.keyUp('ctrl')
        elif platform.system() == 'Darwin':
            pyautogui.keyDown('command')
            sleep(0.2)
            pyautogui.press('v')
            pyautogui.keyUp('command')
        pyautogui.press('enter')
        sleep(40)

auto_qa(cnt_lis)
