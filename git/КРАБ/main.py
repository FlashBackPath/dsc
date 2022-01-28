import pandas as pd
from sklearn import preprocessing
import collections
import random
from math import log
import matplotlib.pyplot as plt


document = pd.read_excel('InjuryDeath.xlsx')
#print(document.columns)

age = document['age']
income = document['income']
childyrs = document['childyrs']

raw_data = []
for i in range(len(age)):
    raw_data.append([age[i], income[i], childyrs[i]])

#norm_data = preprocessing.normalize(data)
#print(norm_data)

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

def get_bigs(data, k):
    inds = []
    for i in range(k-1):
        t = data.index(max(data))
        inds.append(t)
        data.pop(t)
    return sorted(inds)

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
    tlen = []
    data_len = []
    tmp_data = list(n_data)
    r_dot = tmp_data[random.randint(0, len(n_data) - 1)]
    tmp_lst = [r_dot]
    tmp_data.remove(r_dot)
    while len(tmp_data) != 0:
        i_val = 0
        min_sum = 10
        for i in range(len(tmp_data)):
            x = vector_length(tmp_lst[0], tmp_data[i])
            tlen.append(x)
            if x < min_sum:
                min_sum = x
                i_val = i

        tmp_lst.append(tmp_data[i_val])
        tmp_data.remove(tmp_data[i_val])
        data_len.append(min(tlen))
        tlen.clear()

    print(tmp_lst)
    print(data_len)

    clasters = []
    borders = []
    for i in range(k-1):
        clasters.append([])
        borders.append([])
    borders.append([])

    z = get_bigs(data_len, k)
    print(z)

    counter = 0
    minus = 0
    for i in z:
        i -= minus
        for j in range(i+1):
            clasters[counter].append(tmp_lst[0])
            tmp_lst.pop(0)
        counter += 1
        minus += i+1
    clasters.append(tmp_lst)
    print(clasters)

    for i in range(len(clasters)):
        tmp = clasters[i]
        for j in range(len(tmp)-1):
            borders[i].append(vector_length(tmp[j], tmp[j+1]))
    print(borders)
    p = []
    d = 0
    alpha = []
    h = []
    for i in range(len(clasters)):
        pi = []
        for j in borders:
            pi.append(sum(j))
        p.append(sum(pi) / k)

        t_sum = 0
        flag = False
        for j in data_len:
            for jj in borders:
                if flag:
                    continue
                elif j not in jj:
                    t_sum += j
                    flag = True
            flag = False
        print(t_sum)
        d = t_sum / (k - 1)

        if len(borders[i]) == 0:
            alpha.append(0)
        else:
            for j in range(len(borders)):
                if j == 0:
                    alpha.append(borders[i][j+1]/borders[i][j])
                elif j == len(borders) - 1:
                    alpha.append(borders[i][j-1] / borders[i][j])
                else:
                    alpha.append(min([borders[i][j-1]], [borders[i][j+1]])[0] / borders[i][j])

        h.append(len(clasters[i])/len(tmp_lst))

    h_m = 1.0
    for i in h:
        h_m *= i
    h_m *= k**k

    a = d*h_m
    b = sum(alpha)/(k-1)*sum(p)
    F = log(a/b)

    print(f'p = {sum(p)}')
    print(f'd = {d}')
    print(f'alpha = {sum(alpha)/(k-1)}')
    print(f'h = {h_m}')
    print(f'F = {F}')
    for claster in clasters:
        max = 0
        min_ = 200
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
            if s < min_:
                min_ = s
                d2 = dot
        print(f'------Кластер №{counter-3}------')
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
#n_data = [[1.0, 0.2, 0.3], [0.2, 0.65, 0.33], [0.7, 0.42, 0.11], [0.77, 0.66, 0.55], [0.58, 0.69, 0.53], [0.25, 0.54, 0.16], [0.74, 0.59, 0.95]]
clasterAnalize(n_data, 5)
