var_id = 0
map_vars = {}


def get_var_name(value):
    if value in map_vars:
        return map_vars[value]

    global var_id
    var_name = "x" + str(var_id)
    map_vars[value] = var_name
    var_id += 1
    return var_name


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


triplas = []
with open("testess.txt", mode="r", encoding="UTF-8") as f:
    for linha in f:
        if linha[0] == "#":
            tripla = linha[1:].split()
            tripla.append(0)
            triplas.append(tripla)

print("Lista de triplas")
for tripla in triplas:
    print(tripla[:3])

# keywords = ['idade', 'Alencar']
keywords = ['bolsistaDe', 'Denis', "Estudante"]

print("\n\nKeywords")
print(keywords)

triplas_var_keywords = []
for tripla in triplas:
    for word in keywords:
        if (word in tripla):
            triplas_var_keywords.append(tripla)
            break

print("\n\nTriplas contendo keywords")
for tripla in triplas_var_keywords:
    print(tripla[:3])

for tripla in triplas_var_keywords:
    if s(tripla) not in keywords:
        tripla[3] += 1
        set_s(tripla, get_var_name(s(tripla)))

    if p(tripla) not in keywords:
        tripla[3] += 1
        set_p(tripla, get_var_name(p(tripla)))

    if o(tripla) not in keywords:
        tripla[3] += 1
        set_o(tripla, get_var_name(o(tripla)))


print("\n\nTriplas com variáveis: [sujeito, predicado, objeto] -> numero_variáveis")
triplas_var_keywords = sorted(triplas_var_keywords, key=lambda tripla: tripla[3])
for tripla in triplas_var_keywords:
    print(tripla[:3], '->', tripla[3])



lista_composta_2 = []
for index, tripla1 in enumerate(triplas_var_keywords):
    for tripla2 in triplas_var_keywords[index + 1:]:
        new_tripla_composta = []
        new_tripla_composta.append(tripla1)
        new_tripla_composta.append(tripla2)
        new_tripla_composta.append(tripla1[3] + tripla2[3])
        new_tripla_composta.append(0)
        for keyword in keywords:
            if keyword in tripla1 or keyword in tripla2:
                new_tripla_composta[3]+=1
        lista_composta_2.append(new_tripla_composta)



print("\n\nTriplas com variáveis: [sujeito, predicado, objeto] -> numero_variáveis, numero_keywords")
lista_composta_2 = sorted(lista_composta_2, key=lambda tripla: tripla[3], reverse=True)
for tripla in lista_composta_2:
    print(tripla[0][:3], tripla[1][:3], '->', tripla[2], tripla[3])