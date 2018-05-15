triplas = []
with open("testess.txt", mode="r", encoding="UTF-8") as f:
    for linha in f:
        if linha[0] == "#":
            tripla = linha[1:].split()
            tripla.append(0)
            triplas.append(tripla)

# frase=Qual é a idade de Alencar?
# frase=O bolsista de Denis é um Estudante?
# keywords = ['bolsistaDe', 'Denis', 'Estudante']
keywords = ["idade", "Alencar"]

distances = {}

for tripla in triplas:
    print(tripla)


def s(tripla):
    return tripla[0]


def p(tripla):
    return tripla[1]


def o(tripla):
    return tripla[2]


def set_s(tripla, value):
    tripla[0] = value


def set_p(tripla, value):
    tripla[1] = value


def set_o(tripla, value):
    tripla[2] = value


def string_tripla(tripla):
    return '-'.join([s(tripla), p(tripla), o(tripla)])

def distances_add_if_not_present(part1, part2, value):
    key = part1 + '-' + part2
    if key in distances:
        return
    distances[key] = value


def distance_match(part1, part2, value):
    key = part1 + '-' + part2
    if key in distances:
        return distances[key] == value
    return False


def merge(list1, list2):
    return list1 + list(set(list2) - set(list1))


var_id = 1
map_vars = {}


def add_var(value):
    if value in map_vars:
        return map_vars[value]

    global var_id
    var_name = "x" + str(var_id)
    map_vars[value] = var_name
    var_id += 1
    return var_name


print("\n\n")

triplas_variaveis = []

for tripla in triplas:
    for word in keywords:
        if (word in tripla):
            print(tripla)
            triplas_variaveis.append(tripla)
            break

for tripla in triplas_variaveis:
    if s(tripla) not in keywords:
        tripla[3] += 1
        set_s(tripla, add_var(s(tripla)))

    if p(tripla) not in keywords:
        tripla[3] += 1
        set_p(tripla, add_var(p(tripla)))

    if o(tripla) not in keywords:
        tripla[3] += 1
        set_o(tripla, add_var(o(tripla)))

print("\n\ntriplas_variaveis")

triplas_sorted = sorted(triplas_variaveis, key=lambda tripla: tripla[3])

for tripla in triplas_sorted:
    print(tripla)

lista_composta = []
for index, tripla1 in enumerate(triplas_sorted):
    for tripla2 in triplas_sorted[index+1:]:
        te = []
        te.append(tripla1)
        te.append(tripla2)
        te.append(tripla1[3] + tripla2[3])

        temp = []
        for re in tripla1:
            if re in keywords and re not in temp:
                temp.append(re)
        for re in tripla2:
            if re in keywords and re not in temp:
                temp.append(re)
        te.append(len(temp))

        lista_composta.append(te)




print("\n\n")
print("triplas -> NUMERO_VARIAVEIS , NUMERO_DISTINTO_KEYWORD_QUE_CONTEMPLA\n")
lista_composta = sorted(lista_composta, key=lambda tripla: tripla[3], reverse=True)
for tripla in lista_composta:
    print(tripla[0][:3], tripla[1][:3], '\t\t->',tripla[2],',',tripla[3])

exit()
print("\n")
# Alencar tipo Pessoa
# Denis amigo Alencar
# Alencar bolsista Denis

for tripla in triplas:
    ok = False
    for word in keywords:
        if (word in tripla):
            ok = True
            break

    if not ok:
        continue

    distances_add_if_not_present(s(tripla), p(tripla), 1)  # Alencar tipo 1
    distances_add_if_not_present(s(tripla), o(tripla), 2)  # Alencar Pessoa 2
    distances_add_if_not_present(p(tripla), o(tripla), 1)  # tipo Pessoa 1

    distances_add_if_not_present(o(tripla), s(tripla), -2)
    distances_add_if_not_present(o(tripla), p(tripla), -1)
    distances_add_if_not_present(p(tripla), s(tripla), -1)

    for sub_tripla in triplas:
        if o(tripla) == s(sub_tripla) and p(tripla) != p(sub_tripla) and o(sub_tripla) != o(tripla) and s(tripla) != s(sub_tripla):
            distances_add_if_not_present(s(tripla), p(sub_tripla), 3)
            distances_add_if_not_present(s(tripla), o(sub_tripla), 4)
            distances_add_if_not_present(p(tripla), p(sub_tripla), 2)
            distances_add_if_not_present(p(tripla), o(sub_tripla), 3)

        if o(tripla) == o(sub_tripla) and p(tripla) != p(sub_tripla) and s(tripla) != s(sub_tripla):
            distances_add_if_not_present(s(tripla), p(sub_tripla), -3)
            distances_add_if_not_present(s(tripla), s(sub_tripla), -4)
            distances_add_if_not_present(p(tripla), p(sub_tripla), -2)
            distances_add_if_not_present(p(tripla), o(sub_tripla), -3)

print(len(distances))
for key, distance in distances.items():
    print("{:>20} <-> {}".format(key, distance))

__s1 = [s(tripla) for tripla in triplas]
__s2 = [p(tripla) for tripla in triplas]
__s3 = [o(tripla) for tripla in triplas]

Vso = []
Vp = []
K = 1
k = 0
L = list()


def generate(L, k):
    for s1 in merge(__s1, Vso):
        for s2 in merge(__s2, Vp):
            for s3 in merge(__s3, Vso):
                if k == 0 and distance_match(s2, s3, -1) and distance_match(s1, s2, 1) and distance_match(s1, s3, 2):
                    L.append((s1, s2, s3))

                b1 = True
                b2 = True
                b3 = True
                b4 = True
                for t1, t2, t3 in L:
                    if not (
                            s1 == t1 and
                            distance_match(t1, s2, 2) and
                            distance_match(t1, s3, 3) and
                            distance_match(t2, s2, -2) and
                            distance_match(t2, s3, -3) and
                            distance_match(t3, s2, -3) and
                            distance_match(t3, s3, -4)
                    ):
                        b1 = False

                    if not (
                            s1 == t3 and
                            distance_match(t1, s2, 3) and
                            distance_match(t1, s3, 4) and
                            distance_match(t2, s2, 2) and
                            distance_match(t2, s3, 3) and
                            distance_match(t3, s2, 1) and
                            distance_match(t3, s3, 2)
                    ):
                        b2 = False

                    if not (
                            s3 == t1 and
                            distance_match(t1, s2, -1) and
                            distance_match(t1, s3, -4) and
                            distance_match(t2, s2, -2) and
                            distance_match(t2, s3, -3) and
                            distance_match(t3, s2, -1) and
                            distance_match(t3, s3, -2)
                    ):
                        b3 = False

                    if not (
                            s3 == t3 and
                            distance_match(t1, s2, -3) and
                            distance_match(t1, s3, 2) and
                            distance_match(t2, s2, -2) and
                            distance_match(t2, s3, -1) and
                            distance_match(t3, s2, -1)
                    ):
                        b4 = False

                if b1 or b2 or b3 or b4:
                    L.append((s1, s2, s3))
                    Vso.append(s1)
                    Vso.append(s3)
                    Vp.append(s2)

                if k != K:
                    generate(L, k + 1)


generate(L, k)
print("\n")
print(L)
print("\n")
for l in L:
    print(l)
