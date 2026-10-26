# -*- coding: utf-8 -*-
import random
import os
import re

# 获取path文件夹内的所有文件地址，返回列表
def read_dir(dir_path):
    fileArray = []
    for root, dirs, files in os.walk(dir_path):
        for fn in files:
            eachpath = str(root+'/'+fn)
            fileArray.append(eachpath)
    return fileArray

def read_txt(txt_path):
    olis = []
    lis = open(txt_path).read().split('--------')
    lis = random.sample(lis, 11)
    for i in lis:
        text = re.findall(r'文本为：.*', i)
        q = re.findall(r'用户：.*', i)
        a = re.findall(r'回答：.*', i)
        
        # print(a)
        if len(q) > 1:
            dic = {}
            try:
                dic['文本'] = text[0][4:]
                u = random.choice(q[1:])
                dic['用户'] = u[3:]
                index = q.index(u)
                dic['回答'] = a[index][3:]
                olis.append(dic)
            except:
                pass
    return olis

if __name__ == '__main__':
    dir_path = '/Users/zhangduola/Desktop/《中国思想家评传》/4qa相似度计算/待计算文本'
    files = read_dir(dir_path)
    files = [i for i in files if '.DS_Store' not in i]
    all_ = []
    for i in files:
        olis = read_txt(i)
        all_.extend(olis)
    all_ = all_
    print(len(all_))
    open('2000.txt', 'w').write(str(all_))
    print('over')
