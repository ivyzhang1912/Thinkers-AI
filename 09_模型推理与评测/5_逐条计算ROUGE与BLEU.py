import pandas as pd
import jieba
from rouge_chinese import Rouge
from transformers import AutoModelForCausalLM, AutoTokenizer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
df = pd.read_csv('eval_3000.csv')
import numpy as np
# 示例数据
labels = list(df['回答'])
preds = list(df['模型'])
qs = list(df['用户'])
tokenizer = AutoTokenizer.from_pretrained('/home/pgrad/jef/export_m', use_fast=False, trust_remote_code=True)

score_dict = {"rouge-1": [], "rouge-2": [], "rouge-l": [], "bleu-4": []}
flag = 0
l1, l2, l3, s, b = [], [], [], [], []
for pred, label in zip(preds, labels):
    q = qs[flag]
    l1.append(q)
    l2.append(label)
    l3.append(pred)
    flag += 1
    hypothesis = list(tokenizer.tokenize(pred))
    reference = list(tokenizer.tokenize(label))

    if len(" ".join(hypothesis).split()) == 0 or len(" ".join(reference).split()) == 0:
        result = {"rouge-1": {"f": 0.0}, "rouge-2": {"f": 0.0}, "rouge-l": {"f": 0.0}}
        s.append({})
    else:
        rouge = Rouge()
        scores = rouge.get_scores(" ".join(hypothesis), " ".join(reference))
        result = scores[0]
        s.append(result)
        
    for k, v in result.items():
        score_dict[k].append(round(v["f"] * 100, 4))

    bleu_score = sentence_bleu([list(label)], list(pred), smoothing_function=SmoothingFunction().method2)
    b.append(bleu_score * 100)
    score_dict["bleu-4"].append(round(bleu_score * 100, 4))

print({k: float(np.mean(v)) for k, v in score_dict.items()})

df = pd.DataFrame(data={'用户': l1, '回答': l2, '模型': l3, 'rouge': s, 'bleu': b})
df.to_csv('单个结果.csv')
