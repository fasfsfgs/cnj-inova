import csv
import json

lista_movimentos = []

with open('lista_movimentos.csv') as csvfile:
    data = csv.reader(csvfile, delimiter=',')

    for row in data:

        if str(row[1][0:3]) == 'mov':
            pass
        else:
            mov_origem_destino = str(row[1]) + '_' + str(row[2])
            classe_processual = '_' + row[7]
            siglaTribunal = '_' + row[8]
            item = mov_origem_destino + classe_processual + siglaTribunal

            lista_movimentos.append(item)
