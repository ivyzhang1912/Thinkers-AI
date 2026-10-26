import pandas as pd
texts, users, answers1, answers2, answers3 = [], [], [], [], []
lis = open('new1w5_3.txt', encoding='utf-8').readlines()
for i in lis:
    i = eval(i)
    try:
        x = i['回答'][0][0][6:]
        y = i['回答'][1][0][6:]
        z = i['回答'][2][0][6:]
        if x or y or z:
            answers1.append(x)
            answers2.append(y)
            answers3.append(z)
            texts.append(i['文本'])
            users.append(i['用户'])
    except:
        pass
# print(len(texts), len(users), len(answers1), len(answers2), len(answers3))
df = pd.DataFrame(data={'文本': texts, '用户': users, '回答1': answers1, '回答2': answers2, '回答3': answers3})
df.to_csv('2.csv', mode='a', index=False, header=True)


