import random
import pandas as pd
from sklearn import preprocessing
import collections
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
for i in range(int(len(ordered_data)*0.1)):
    ordered_data.pop(death_note[i])

death_note = list(ordered_data.keys())
for i in range(int(len(ordered_data)*0.2)):
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

def find_min(t_len):
    minimal = 1000
    ind_1 = -1
    ind_2 = -1

    for i in range(len(t_len)):
        for j in range(len(t_len[i])):
            if t_len[i][j] < minimal:
                minimal = t_len[i][j]
                ind_1 = i
                ind_2 = j
    return minimal, [ind_1, ind_2]

def get_claster_cord(dot):
    t1 = 0
    t2 = 0
    t3 = 0

    for i in dot:
        t1 += i[0]
        t2 += i[1]
        t3 += i[2]

    t1 /= len(dot)
    t2 /= len(dot)
    t3 /= len(dot)

    return [t1, t2, t3]

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

def clasterAnalize(n_data):
    clasters = []
    for i in range(20):
        clasters.append([n_data[random.randint(0, len(n_data)-i)]])

    history = []
    while len(clasters) != 1:
        #print(clasters)
        counter = len(clasters)
        t_len = []
        for j in clasters:
            tmp = []
            a = get_claster_cord(j)
            for i in range(len(clasters)-counter):
                b = get_claster_cord(clasters[i])
                tmp.append(vector_length(a, b))
            t_len.append(tmp)
            counter -= 1

        minimal, inds = find_min(t_len)
        #print(minimal, inds)

        tmp = clasters.pop(inds[0])
        for i in tmp:
            clasters[inds[1]].append(i)
        history.append(list(clasters))

    while True:
        xd = int(input('Сколько кластеров вам нужно? '))
        cl = history[-xd]
        for i in cl[0]:
            for j in range(1, len(cl)):
                if i in cl[j]:
                    if i in cl[0]:
                        cl[0].remove(i)
        print(cl)
        draw(cl)
        counter = 1
        for claster in cl:
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
        if int(input('Вас утроили данные кластеры?(1 - Да|| 0 - Нет) ')):
            break



n_data = [list(i) for i in data]

clasterAnalize(n_data)
