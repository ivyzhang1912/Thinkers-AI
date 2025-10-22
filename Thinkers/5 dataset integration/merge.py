# -*- coding: utf-8 -*-
import pandas as pd
from collections import Counter
import os
import openai
import time
import re
from math import log, floor
import random

os.environ["http_proxy"] ="http://127.0.0.1:7890"
os.environ["https_proxy"] = "https://127.0.0.1:7890"
openai.api_key = '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'

# 获取path文件夹内的所有文件地址，返回列表
def read_dir(path):
    fileArray = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            eachpath = str(root+'/'+fn)
            fileArray.append(eachpath)
    return fileArray

def read_txt(path):
    qas = []
    qa = open(path, encoding='utf-8').read().split('--------')
    a = [i[i.index('result:\n') + len('result:\n'):] for i in qa[:-1]]
    for i in a:
        user = re.findall(r'用户：.*', i)
        cnt = re.findall(r'回答：.*', i)
        if len(user) != 0 and len(cnt) != 0:
            for x, y in zip(user, cnt):
                dic = {}
                dic['用户'] = x[3:]
                dic['回答'] = y[3:]
                qas.append(dic)
    return qas

def read_csv(path):
    problem = []
    df = pd.read_csv(path)
    data = df.values.tolist()
    for i in data:
        if i[2] > 0.95:
            problem.append(i)
    return problem

def write_csv(path, sen):
    df = pd.DataFrame(data={'sen': sen})
    df.to_csv(path, mode='a', index=False, header=False)
    return 1

def choose_(same):
    return same[:2]

def fix_problem(problem):
    # 需从原文本中删除的文本
    del_ = []
    for i in problem:
        for j in range(2):
            del_.append(i[j])
    del_ = list(set(del_))

    all_ = [j for i in problem for j in i]
    # print(all_)
    element_counts = Counter(all_)
    dic = dict(element_counts)
    # 对dic按出现次序大小来排序
    dic = dict(sorted(dic.items(), key= lambda x:x[1], reverse=True))

    to_merged = []
    for x, y in dic.items():
        if type(x) != type(1.1):
            same = []
            to_del = []
            indices = [index for index, value in enumerate(all_) if value == x]
            if indices:
                same.append(x)
            for idx in indices:
                to_del.append(idx)
                a, b = all_[idx - 1], all_[idx + 1]
                if type(a) != type(1.1):
                    same.append(a)
                    to_del.append(idx-1)
                if type(b) != type(1.1):
                    same.append(b)
                    to_del.append(idx+1)
            # 删除
            for i in sorted(to_del, reverse=True):
                all_.pop(i)
            if indices:
                # 对same列表进行处理，处理数量过多的same列表
                if len(same) > 3:
                    same = choose_(same)
                to_merged.append(same)
    return del_, to_merged

def merge(one_merged):
    prompt ='''
    以下两段文本的问句有较强的相似性，请你帮我把这两个问句和他们的回答从语义的角度分别融合成一个问句和一个回答，注意是一个，去除重复含义，但也尽可能保留原有的语义信息。
    回答格式为：
    整合后的用户：[]。
    整合后的回答：[]。
'''
    text = ''
    flag = 0
    for i in one_merged:
        flag += 1
        text += '文本' + str(flag) + '\n'
        text += "用户：{}\n".format(eval(i)['用户'])
        text += "回答：{}\n\n".format(eval(i)['回答'])
    question = prompt + text
    # 并行调用 OpenAI 接口
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user',
                       'content': question}]
        )
        res = response.choices[0].message["content"]
        '''此处需要对result进行格式转换，得到res是一个字典{'用户'： '回答'：}'''
        user = re.findall(r'整合后的用户：.*', res)
        cnt = re.findall(r'整合后的回答：.*', res)
        result = {}
        result['用户'] = user[0][3:]
        result['回答'] = cnt[0][3:]
    except openai.error.APIError as e:
        if "Rate limit reached" in str(e):
            print("Rate limit reached. Waitin for 1 minutes...")
            time.sleep(60)  # 等待 1 分钟
            return merge(question)  # 重新调用 OpenAI 接口
        else:
            result = "暂无"
            print(f"Error: {e}")
    except Exception as e:
        result = "暂无"
        print(f"Error: {e}")
        print("-----------------------")
    return result

def main():
    txt_path, csv_path = 'output_书籍191-201', '相似度_书籍191-201'
    txt_files = read_dir(txt_path)
    csv_files = read_dir(csv_path)
    txt_files = [i for i in txt_files if 'DS' not in i]
    csv_files = [i for i in csv_files if 'DS' not in i]
    txt_files, csv_files = sorted(txt_files), sorted(csv_files)
   
    output_dir = '整合后qa集_' + csv_path[4:]
    os.makedirs(output_dir, exist_ok=True)
    
    for t, c in zip(txt_files, csv_files):
        out_1 = c.split('/')[-2].split('\\')[1]
        out_2 = c.split('/')[-1]
        output_dir_2 = output_dir + '/' + out_1
        os.makedirs(output_dir_2, exist_ok=True)
        txt = read_txt(t)
        problem = read_csv(c)
        del_, to_merged = fix_problem(problem)
        # 没有问题的
        w = []
        for i in txt:
            if str(i) not in del_:
                w.append(str(i))
                if len(w) == 20:
                    write_csv(output_dir_2 + '/' + out_2, w)
                    print('写入20条')
                    w = []
        # 有问题的
        for x in to_merged:
            res = merge(x)
            if res != '暂无':
                write_csv(output_dir_2 + '/' + out_2, [str(res)])
                print('整合后写入1条')
        print(c + ' is ok')

main()

