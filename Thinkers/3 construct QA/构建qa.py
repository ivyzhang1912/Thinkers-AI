import openai

import pandas as pd

from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm

import signal

import sys

import time

import os



os.environ["http_proxy"] ="http://127.0.0.1:7890"
os.environ["https_proxy"] = "https://127.0.0.1:7890"



# 在此处填入你的 OpenAI API 密钥

openai.api_key = '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'



prompt = '''

根据以下文本，深入理解文本内容后，请你为我构造多个多轮问答数据，包含用户的问题和你认为的标准答案。

格式为：

用户：[]。

回答：[]。

文本为：{content}

'''



# 获取path文件夹内的所有文件地址，返回列表

def read_dir(path):

    fileArray = []

    for root, dirs, files in os.walk(path):

        for fn in files:

            eachpath = str(root+'/'+fn)

            fileArray.append(eachpath)

    return fileArray



# 从文本文件读取问题

def read_questions(file_path):

    with open(file_path, 'r', encoding="utf-8") as file:

        lines = file.read().split('\n\n')

    questions = [prompt.format(content=line) for line in lines]

    return questions



# 并行调用 OpenAI 接口

def call_openai(question):

    try:

        response = openai.ChatCompletion.create(

            model='gpt-3.5-turbo',

            messages=[{'role': 'user',

                       'content': question}]

            # max_tokens=1000,

            # n=1,

            # stop=None,

            # temperature=0.3

        )

        

        # result = response.choices[0].text.strip()

        result = response.choices[0].message["content"]

        # print("答案生成中...")

    except openai.error.APIError as e:

        if "Rate limit reached" in str(e):

            print("Rate limit reached. Waiting for 1 minutes...")

            time.sleep(60)  # 等待 1 分钟

            return call_openai(question)  # 重新调用 OpenAI 接口

        else:

            result = "暂无"

            print(f"Error: {e}")

    except Exception as e:

        result = "暂无"

        print(f"Error: {e}")

        print("-----------------------")

    return result



# 保存结果到文件

def save_results(output_file, questions, results):

    # 检查问题和答案的数量是否相同

    if len(questions) != len(results):

        # 将数量较少的那个列表补充到和数量较多的列表一样的长度

        if len(questions) > len(results):

            results += [''] * (len(questions) - len(results))

        else:

            questions += [''] * (len(results) - len(questions))

    with open(output_file, 'a', encoding="utf-8") as f:

        for i, j in zip(questions, results):

            f.write(i + 'result:\n' + j + '\n--------')

        print('写入20对qa')





def deal(file_path):

    questions = read_questions(file_path)

    results = []



    out_1 = file_path.split('/')[-2]

    out_2 = file_path.split('/')[-1]



    output_dir = "output_" + out_1

    os.makedirs(output_dir, exist_ok=True)

    output_file = output_dir + '/' + out_2



    try:

        with ThreadPoolExecutor() as executor, tqdm(total=len(questions)) as progress:

            # 并行调用 OpenAI 接口

            futures = [executor.submit(call_openai, question) for question in questions]


            # 收集结果

            for future in futures:

                result = future.result()

                results.append(result)

                progress.update(1)



                flag = progress.n

                if flag % 20 == 0:

                    save_results(output_file, questions[flag-20:flag], results[flag-20:flag])

    finally:

        # 保存结果到文件

        print(out_1 + 'is over\n')



def main():

    files = read_dir('书籍1-10')

    files = [i for i in files if '.DS_Store' not in i]

    for i in files:

       deal(i)



main()

