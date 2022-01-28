import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import random


data = []
answ = []
for i in range(200):
    tmp = random.randint(0, 400)
    while tmp in data:
        tmp = random.randint(0, 400)
    data.append(tmp)
tmp = random.randint(1, 150)
if tmp < 30:
    tmp = random.randint(1, 150)
for i in range(tmp):
    answ.append(0)
for i in range(200-tmp):
    answ.append(1)

data = sorted(data)

tst_data = []
tst_answ = []
tmp_counter = random.randint(1, 25)
for i in range(tmp_counter):
    q = random.randint(0, tmp-i)
    tst_data.append(data[q])
    tst_answ.append(answ[q])

    data.pop(q)
    answ.pop(q)

for i in range(30-tmp_counter):
    q = random.randint(tmp, len(data)-1)
    tst_data.append(data[q])
    tst_answ.append(answ[q])

    data.pop(q)
    answ.pop(q)

data = np.array(data).reshape(-1, 1)
answ = np.array(answ)

tst_data = np.array(tst_data).reshape(-1, 1)
tst_answ = np.array(tst_answ)

model = LogisticRegression(solver='liblinear', random_state=0).fit(data, answ)
print(f'Значення наклону b_1 = {model.intercept_[0]}')
print(f'Точка перетину b_0 = {model.coef_[0][0]}')


conf = confusion_matrix(tst_answ, model.predict(tst_data))
tp = conf[0][0]
print(f'Істинно-позитивні випадки = {tp}')
fp = conf[0][-1]
print(f'Хибно позитивні випадки = {fp}')
fn = conf[-1][0]
print(f'Хибнопозитивні зразки = {fn}')
tn = conf[-1][-1]
print(f'Істинно негативні випадки = {tn}')
print(f'Точність моделі = {model.score(tst_data, tst_answ)}')
x = model.predict_proba(tst_data)
d_x = []
for i in x:
    d_x.append(i[-1])

x_axes = np.linspace(1, len(d_x), len(d_x))
plt.plot(x_axes, d_x, '*-')
plt.plot(x_axes, [0.5]*len(d_x))
plt.show()