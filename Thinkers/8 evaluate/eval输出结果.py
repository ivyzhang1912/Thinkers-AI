import pandas as pd
import jieba
from rouge_chinese import Rouge
import numpy as np
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from transformers import AutoModelForCausalLM, AutoTokenizer
df = pd.read_csv('/home/pgrad/jef/eval_30002.csv')

# 示例数据
labels = list(df['回答'])
preds = list(df['chatglm'])

tokenizer = AutoTokenizer.from_pretrained("/home/pgrad/jef/export_m", use_fast=False, trust_remote_code=True)

score_dict = {"rouge-1": [], "rouge-2": [], "rouge-l": [], "bleu-4": []}

for pred, label in zip(preds, labels):
    hypothesis = list(tokenizer.tokenize(pred))
    reference = list(tokenizer.tokenize(label))

    if len(" ".join(hypothesis).split()) == 0 or len(" ".join(reference).split()) == 0:
        result = {"rouge-1": {"f": 0.0}, "rouge-2": {"f": 0.0}, "rouge-l": {"f": 0.0}}
    else:
        rouge = Rouge()
        scores = rouge.get_scores(" ".join(hypothesis), " ".join(reference))
        result = scores[0]

    for k, v in result.items():
        score_dict[k].append(round(v["f"] * 100, 4))

    bleu_score = sentence_bleu([list(label)], list(pred), smoothing_function=SmoothingFunction().method2)
    score_dict["bleu-4"].append(round(bleu_score * 100, 4))

print({k: float(np.mean(v)) for k, v in score_dict.items()})
