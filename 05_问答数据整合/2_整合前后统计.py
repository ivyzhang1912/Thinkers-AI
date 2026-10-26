import pandas as pd
import os
import re

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
    if '106' in path:
        print(len(qas))
    return len(qas)

def read_csv(path):
    problem = []
    df = pd.read_csv(path)
    data = df.values.tolist()
    return len(data)

def write_csv():
    txt_dir = '/Users/zhangduola/Desktop/《中国思想家评传》/4qa相似度计算/待计算文本'
    csv_dir = '/Users/zhangduola/Desktop/《中国思想家评传》/5对话集整合/整合后文件'
    txt_path = [i for i in read_dir(txt_dir) if 'DS' not in i]
    csv_path = [i for i in read_dir(csv_dir) if 'DS' not in i]
    name, ltxt, lcsv = [], [], []
    for x, y in zip(sorted(txt_path), sorted(csv_path)):
        lt = read_txt(x)
        lc = read_csv(y)
        n = x.split('/')[-2]
        
        name.append(n)
        ltxt.append(lt)
        lcsv.append(lc)
        # print(x + ' is ok')
    df = pd.DataFrame(data={'书籍': name, '整合前问句数': ltxt, '整合后问句数': lcsv})
    df.to_csv('整合统计.csv', index=False)

write_csv()
