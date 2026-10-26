lis = eval(open('2000.txt').read())
a, q = [], []
for i in lis:
    a.append(i['回答'])
    q.append(i['用户'])
import pandas as pd

df = pd.DataFrame(data={'用户':q, '回答':a})
df.to_csv('3000.csv')
