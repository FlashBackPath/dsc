def vector_length(a, b):
    if len(a) != len(b):
        print('вектори різної довжини')
        return 0

    eucl_sq = 0
    manh_met = 0
    cheb = []
    for i in range(len(a)):
        eucl_sq += (b[i] - a[i])**2

        tmp = abs(b[i] - a[i])
        manh_met += tmp
        cheb.append(tmp)

    eucl = eucl_sq**0.5

    print(f'Евклідова відстань = {eucl}')
    print(f'Квадрат евклідової відстані = {eucl_sq}')
    print(f'Манхеттенська метрика = {manh_met}')
    print(f'Відстань Чебишова = {max(cheb)}')


a_str = str(input("Введіть перший вектор: "))  #Приклад: 1, 2
b_str = str(input("Введіть дургий вектор: "))  #Приклад: 3, 4

a = []
for i in a_str.split(','):
    a.append(int(i))

b = []
for i in b_str.split(','):
    b.append(int(i))
#print(a, b)
vector_length(a, b)
