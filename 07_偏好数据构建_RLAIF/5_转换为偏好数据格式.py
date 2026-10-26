# -*- coding: utf-8 -*-
import pandas as pd
import json
import random
all_ = []
cnt = pd.read_csv('1-1.csv')
flag = 0
for idx, row in cnt.iterrows():
    dic = {}
    if type(row.回答4) == type('s'):
        dic['instruction'] = row.用户
        dic['input'] = ""
        dic['output'] = [row.回答1, row.回答2, row.回答3, row.回答4]
        all_.append(dic)

random.shuffle(all_)

print(len(all_))