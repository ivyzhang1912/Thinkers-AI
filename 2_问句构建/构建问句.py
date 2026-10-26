# -*- coding: utf-8 -*-

import os
import re
import jionlp as jio
import pandas as pd

# 获取path文件夹内的所有文件地址，返回列表
def read_dir(path):
    fileArray = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            eachpath = str(root+'/'+fn)
            fileArray.append(eachpath)
    return fileArray

def bulid_q(path):
    # 读取文本并去掉所有的换行符
    with open(path, "r", encoding="utf-8") as file:
        text = file.read().replace("\n", "")
    
    # 使用joinlp分句
    sentences = jio.split_sentence(text, criterion='coarse')

    # 构建问答数据集
    qa_dataset = []
    window_size = 5  # 选择5个句子作为一组问答
    overlap = 2  # 每组问答之间的重叠句子数

    i = 0
    while i < len(sentences):
        qa_group = sentences[i:i + window_size]

        # 如果总字数超过400，减少选取的句子数量
        while len("".join(qa_group)) > 400:
            qa_group.pop(0)

        qa_dataset.append("".join(qa_group))
        i += window_size - overlap

    out_1 = path.split('/')[-2]
    out_2 = path.split('/')[-1]

    # 将问答数据集写入txt文件
    output_dir = "/Users/zhangduola/Desktop/《中国思想家评传》/文本提问句构建/output_data/" + out_1
    os.makedirs(output_dir, exist_ok=True)

    with open(output_dir + '/' + out_2, "x") as file:
        for qa_group in qa_dataset:
            file.write(qa_group + "\n\n")

    print(out_1 + 'is ok\n')
    return out_1, out_2, len(qa_dataset)

def main():
    files = read_dir('/Users/zhangduola/Desktop/《中国思想家评传》/xml文本提取/《中国思想家评传》系列丛书_正文及注释')
    txt_files = [i for i in files if '_正文.txt' in i]
    out_1_lis = []
    out_2_lis = []
    leng_lis = []
    for i in txt_files:
        out_1, out_2, leng = bulid_q(i)
        out_1_lis.append(out_1)
        out_2_lis.append(out_2)
        leng_lis.append(leng)
    df = pd.DataFrame({'书籍': out_1_lis, '正文': out_2_lis, '段落数': leng_lis})
    df.to_excel('统计运行情况.xlsx', index=True)

main()