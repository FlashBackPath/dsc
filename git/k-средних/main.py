import pandas as pd
from sklearn import preprocessing
import collections
import random
import matplotlib.pyplot as plt

document = pd.read_excel('InjuryDeath.xlsx')
#print(document.columns)

age = document['age']
income = document['income']
childyrs = document['childyrs']

raw_data = []
for i in range(len(age)):
    raw_data.append([age[i], income[i], childyrs[i]])

dict_data = {}
for i in raw_data:
    dict_data.update({sum(i): list(i)})


ordered_data = collections.OrderedDict(sorted(dict_data.items()))
death_note = list(ordered_data.keys())
for i in range(int(len(ordered_data)*0.3)):
    ordered_data.pop(death_note[i])

death_note = list(ordered_data.keys())
for i in range(int(len(ordered_data)*0.3)):
    ordered_data.pop(death_note[-i])

#ordered_data = dict(ordered_data)
#print(ordered_data)
data = preprocessing.normalize(list(ordered_data.values()))

def vector_length(a, b):
    eucl_sq = 0
    for i in range(len(a)):
        eucl_sq += (b[i] - a[i]) ** 2
    return eucl_sq

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def claster_creation(n_data, clasters):
    for i in n_data:
        tmp = []
        for j in clasters:
            tmp.append(vector_length(i, j[0]))
        z = min(tmp)
        clasters[tmp.index(z)].append(i)
    return clasters

def new_root(clasters):
    o_c = []
    old_clasters = list(clasters)
    for i in range(len(clasters)):
        d = {}
        for j in clasters[i]:
            tmp = []
            for k in clasters[i]:
                tmp.append(vector_length(j, k))
            d.update({clasters[i].index(j): sum(set(tmp))})
        #print(d)
        x = d.values()

        nc = get_key(d, min(x))
        o_c.append(int(nc))
        clasters[i] = [clasters[i][nc]]
    if o_c[0] == o_c[-1] == 0:
        return old_clasters, False
    else:
        return clasters, True

def draw(clasters):
    #print(clasters)
    colors = ['red', 'blue', 'green', 'purple', 'black']
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for i in range(len(clasters)):
        d0 = []
        d1 = []
        d2 = []
        for j in clasters[i]:
            d0.append(j[0])
            d1.append(j[1])
            d2.append(j[2])
        ax.scatter(d0, d1, d2, c=colors[i])
    plt.show()

def clasterAnalize(n_data, k):
    clasters = []
    for i in range(k):
        clasters.append([])

    for i in clasters:
        q = []
        qq = random.randint(0, len(n_data)-1)
        while qq in q:
            qq = random.randint(0, len(n_data) - 1)
        i.append(list(n_data[qq]))
        q.append(qq)

    check = True
    while check:
        clasters = claster_creation(n_data, clasters)
        clasters, check = new_root(clasters)

    counter = 1
    for claster in clasters:
        max = 0
        min = 200
        d1 = []
        d2 = []

        s1 = 0
        s2 = 0
        s3 = 0
        for dot in claster:
            s1 += dot[0]
            s2 += dot[1]
            s3 += dot[2]

            s = sum(dot)
            if s > max:
                max = s
                d1 = dot
            if s < min:
                min = s
                d2 = dot
        print(f'------Кластер №{counter}------')
        print(f'В кластере {len(claster)} объектов')
        print(f'Самая удалённая от центра точка кластра - {d1}')
        print(f'Самая близлежащая к центру точка кластра - {d2}')
        print(f'Среднее значение координаты Х - {s1 / len(claster)}')
        print(f'Среднее значение координаты Y - {s2 / len(claster)}')
        print(f'Среднее значение координаты Z - {s3 / len(claster)}')
        counter += 1
    draw(clasters)

n_data = []
for i in data:
    n_data.append(list(i))
clasterAnalize(n_data, 5)
