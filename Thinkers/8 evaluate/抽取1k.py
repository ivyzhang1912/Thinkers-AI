import json
import random
# 打开 JSON 文件进行读取
with open('/Users/zhangduola/Desktop/《中国思想家评传》/6微调数据集构建/fine_tuning_data_zh.json', 'r') as json_file:
    data = json.load(json_file)

# 现在 data 包含了 JSON 文件的内容
data_1k = random.sample(data, 100)

with open('100_evalution.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_1k, json_file, ensure_ascii=False)
