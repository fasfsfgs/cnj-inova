import csv
import json


def criar_json_fromcsv(arquivocsv):

    dict_criarjsonestatiticas = {}

    with open(arquivocsv) as csvfile:
        data = csv.reader(csvfile, delimiter=',')

        for row in data:

            if str(row[1][0:3]) == 'mov':
                pass

            else:
                dict_linha = {'mov_origem': str(row[1]), 'mov_destino': str(row[2]), 'classe_processual': row[7],
                              'siglaTribunal': row[8], 'ocorrencias': row[3], 'prob': row[4], 'alerta': row[5],
                              'prob_nacional': row[6]}

                key_principal = str(row[1]) + '_' + \
                    str(row[2]) + '_' + row[7] + '_' + row[8]

                dict_criarjsonestatiticas[key_principal] = dict_linha

    with open('lista_movimentos.json', 'w') as arquivo:
        json.dump(dict_criarjsonestatiticas, arquivo)
