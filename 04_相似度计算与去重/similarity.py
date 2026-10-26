import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1,2,3,4,5,6,7,8"

import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import openai
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import signal
import sys
import time

# os.environ["http_proxy"] ="http://127.0.0.1:7890"
# os.environ["https_proxy"] = "https://127.0.0.1:7890"

openai.api_key = os.getenv("OPENAI_API_KEY")

prompt = '''
以下两段文本的问句有较强的相似性，请你帮我把这两个问句和他们的回答分别合并，去除重复含义，保留二者原语义。
文本1：
问句：{q1}
回答：{a1}
文本2：
问句：{q2}
回答：{a2}
回答格式：
合并问句：[]。
合并答案：[]。
'''

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
        sub_qas = []
        user = re.findall(r'用户：.*', i)
        cnt = re.findall(r'回答：.*', i)
        if len(user) != 0 and len(cnt) != 0:
            for x, y in zip(user, cnt):
                dic = {}
                dic['用户'] = x[3:]
                dic['回答'] = y[3:]
                sub_qas.append(dic)
        qas.append(sub_qas)
    return qas

model = SentenceTransformer('/home/gpuall/jeffrey/评传/chatdataset/torch/sentence_transformers/sentence-transformers_all-MiniLM-L6-v2')

# 相似度是否大于x
def comparing(a, b, x):
    sen1, sen2 = a['用户'], b['用户']
    embedding1 = model.encode([sen1])  # 将句子转换为形状为(1, embedding_size)的二维数组
    embedding2 = model.encode([sen2])  # 将句子转换为形状为(1, embedding_size)的二维数组
    similarity = cosine_similarity(embedding1, embedding2)
    if x < similarity[0][0] < 1:
        return similarity[0][0]
    else:
        return 0

# 合并问题和答案
def merge(a, b):
    try:
        question = prompt.format(q1=a['用户'], a1=a['回答'], q2=b['用户'], a2=b['回答'])
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user',
                       'content': question}]
        )
        res = response.choices[0].message["content"]
        user = re.find(r'用户：.*', res)
        cnt = re.find(r'回答：.*', res)
    except openai.error.APIError as e:
        if "Rate limit reached" in str(e):
            print("Rate limit reached. Waiting for 1 minutes...")
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

def process_lis(qas, output_file):
    le = len(qas)
    flag = 0
    for i in range(le):
        # start = time.time()
        sen1, sen2, score = [], [], []
        flag += 1
        for j in range(len(qas[i])):
            for k in range(i + 1, min(i + 4, len(qas))):
                for l in range(len(qas[k])):
                    s = comparing(qas[i][j], qas[k][l], x=0)
                    if s:
                        sen1.append(qas[i][j])
                        sen2.append(qas[k][l])
                        score.append(s)
        # end = time.time()
        # print('time: ', end - start)
        df = pd.DataFrame(data={'sen1':sen1, 'sen2':sen2, 'score': score})
        df.to_csv(output_file, mode='a',index=False, header=False)
        print(str(flag) + '/' + str(le))

def main():
    path = 'output_书籍1-10'
    files = read_dir(path)
    files = [i for i in files if '.DS_Store' not in i]
    output_dir = '相似度_' + path.split('_')[1]
    os.makedirs(output_dir, exist_ok=True)
    for i in files:
        print(i)
        qas = read_txt(i)
        out_1 = i.split('/')[-2]
        out_2 = i.split('/')[-1]
        os.makedirs(output_dir + '/' + out_1, exist_ok=True)
        output_file = output_dir + '/' + out_1 + '/' + out_2[:-3] + 'csv'
        print('开始')
        process_lis(qas, output_file)
        print(i + 'is ok\n\n\n')

main()
