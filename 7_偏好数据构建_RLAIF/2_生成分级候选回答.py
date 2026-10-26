# -*- coding: utf-8 -*-
from concurrent.futures.thread import ThreadPoolExecutor

import openai
import time
import re
import os

from tqdm import tqdm

prompt = '''
现在你是一个历史学研究学者，请你基于文本回答该问题：{q}
要求：生成完整性、流畅性、内容长度由高到低的三个答案
文本：
{text}
回答格式：
最好的答案：[]。
一般的答案：[]。
最次的答案：[]。
'''
openai.api_key = os.getenv("OPENAI_API_KEY")
os.environ["http_proxy"] ="http://127.0.0.1:7890"
os.environ["https_proxy"] = "https://127.0.0.1:7890"

def generate_a(dic):
    try:
        question = prompt.format(text=dic['文本'], q=dic['用户'])
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user',
                       'content': question}]
        )
        res = response.choices[0].message["content"]
        a1 = re.findall(r'最好的答案：.*', res)
        a2 = re.findall(r'一般的答案：.*', res)
        a3 = re.findall(r'最次的答案：.*', res)
        result = [a1, a2, a3]
    except openai.error.APIError as e:
        if "Rate limit reached" in str(e):
            print("Rate limit reached. Waiting for 1 minutes...")
            time.sleep(60)  # 等待 1 分钟
            return generate_a(question)  # 重新调用 OpenAI 接口
        else:
            result = "暂无"
            print(f"Error: {e}")
    except Exception as e:
        result = "暂无"
        print(f"Error: {e}")
        print("-----------------------")
    return result

if __name__ == '__main__':
    new_all = []
    all_ = eval(open('1w.txt').read())
    try:
        with ThreadPoolExecutor() as executor, tqdm(total=len(all_)) as progress:
            # 并行调用 OpenAI 接口
            futures = [executor.submit(generate_a, i) for i in all_]
            # 收集结果
            for i, future in zip(all_, futures):
                result = future.result()
                if type(result) == type([1, 2]):
                    i['回答'] = result
                    new_all.append(i)
                progress.update(1)
                flag = progress.n
    finally:
        open('new1w.txt', 'w').write(str(new_all))


