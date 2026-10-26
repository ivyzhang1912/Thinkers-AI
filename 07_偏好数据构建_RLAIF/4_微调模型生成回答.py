from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation.utils import GenerationConfig
import torch
import pandas as pd

# 加载本地分词器
tokenizer = AutoTokenizer.from_pretrained('/home/gpuall/jeffrey/毕业论文/train/model/Export_m', use_fast=False, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained('/home/gpuall/jeffrey/毕业论文/train/model/Export_m', device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
model.generation_config = GenerationConfig.from_pretrained('/home/gpuall/jeffrey/毕业论文/train/model/Export_m')

messages = []
users = pd.read_csv('1.csv')['用户']
for txt in users[:2]:
    messages.append({"role": "user", "content": txt})
    response = model.chat(tokenizer, messages)
    print(response)
    print(type(response))
