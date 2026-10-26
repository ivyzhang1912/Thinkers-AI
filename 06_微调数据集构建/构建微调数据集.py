import pandas as pd
import random
import json
import os

# 获取path文件夹内的所有文件地址，返回列表
def read_dir(path):
    fileArray = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            eachpath = str(root+'/'+fn)
            fileArray.append(eachpath)
    return fileArray

def read_csv(path):
    
    df = pd.read_csv(path, encoding='utf-8')
    data = df.values.tolist()
    new_data = []
    for i in data:
        dic = eval(i[0])
        new_dic ={}
        if dic['用户'][:4] == '的用户：':
            new_dic['instruction'] = dic['用户'][4:]
        else:
            new_dic['instruction'] = dic['用户']
        new_dic['input'] = ""
        if dic['回答'][:4] == '的回答：':
            new_dic['output'] = dic['回答'][4:]
        else:
             new_dic['output'] = dic['回答']
        new_data.append(new_dic)
    return new_data

def main():
    path = '/Users/zhangduola/Desktop/《中国思想家评传》/5对话集整合/整合后文件'
    all_ = []
    for i in read_dir(path):
        if 'DS' not in i:
            x = read_csv(i)
            all_.extend(x)
            print(i + ' is ok')
    random.shuffle(all_)
    # 将列表写入 JSON 文件，确保不转义中文字符
    with open('fine_tuning_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(all_, json_file, ensure_ascii=False)

main()
