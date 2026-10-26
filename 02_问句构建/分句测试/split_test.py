# -*- coding: utf-8 -*-

import os
import re
import jionlp as jio

# 读取文本并去掉所有的换行符
with open("合并.txt", "r", encoding="utf-8") as file:
    text = file.read().replace("\n", "")

# 使用joinlp分句
sentences = jio.split_sentence(text, criterion='coarse')

# 构建问答数据集
qa_dataset = []
window_size = 5  # 选择5个句子作为一组问答
overlap = 1  # 每组问答之间的重叠句子数

i = 0
while i < len(sentences):
    qa_group = sentences[i:i + window_size]

    # 如果总字数超过400，减少选取的句子数量
    while len("".join(qa_group)) > 400:
        qa_group.pop(0)

    qa_dataset.append("".join(qa_group))
    i += window_size - overlap

# 将问答数据集写入txt文件
output_dir = "output_data"
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, "qa_dataset_5.txt"), "w", encoding="utf-8") as file:
    for qa_group in qa_dataset:
        file.write(qa_group + "\n\n")

print("问答数据集已生成并保存在 output_data 目录下的 qa_dataset.txt 文件中。")
