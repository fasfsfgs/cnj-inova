# import boto3
# from boto3.dynamodb.conditions import Key, Attr
import json
import csv

# #instanciando o db
# dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# def get_alertabd(classe_processual, mov_origem, mov_destino, tribunal):
#
#     #     nome da tabela é formado pela classe processual, eu dividi em mais tabelas pra ficar mais rápido acessar os dados
#     table_name = 'markov_estatisticas_' + str(classe_processual)
#     table = dynamodb.Table(table_name)
#
#
#     # o campo id primário da tabela é formado pelo mov_origem_movi_destino
#     mov_origem_destino = str(mov_origem) + '_' + str(mov_destino)
#     # o campo de id secundário é formado pelo tribunal
#
#     response = table.query(
#         KeyConditionExpression=Key('mov_origem_destino').eq(mov_origem_destino) & Key('siglaTribunal').eq(tribunal)
#     )
#
#     # ele pode encontrar mais de um item, eu pego o primeiro para não ter erro
#     alertas = response['Items']
#     alerta = alertas[0]
#
#     # alerta é um dicionário contendo todos os dados da linha {nomedacoluna: resultado}
#     return alerta

def getjson_alertabd(classe_processual, mov_origem, mov_destino, tribunal):

    with open('lista_movimentos.json', 'r') as arquivo:
        data = json.load(arquivo)

    movimento = mov_origem + '_' + mov_destino + '_' + classe_processual + '_' + tribunal

    alerta = data[movimento]

    # alerta é um dicionário contendo todos os dados da linha {nomedacoluna: resultado}
    return alerta

# def get_textos(classe_processual, mov_origem, mov_destino):
#
#     table = dynamodb.Table('marko_movimentos')
#
#     response_origem = table.query(KeyConditionExpression=Key('codigo').eq(mov_origem))
#     mov_origem_texto_raw = response_origem['Items'][0]
#     mov_origem_texto = mov_origem_texto_raw.get('descricao')
#
#     response_destino = table.query(KeyConditionExpression = Key('codigo').eq(mov_destino))
#     mov_destino_texto_raw = response_destino['Items'][0]
#     mov_destino_texto = mov_destino_texto_raw.get('descricao')
#
#     dict_classes = {'7': 'Procedimento Comum Cível', '1116': 'Execução Fiscal', '159' : 'Execução de Título Extrajudicial', '283': 'Ação Penal - Procedimento Ordinário'}
#     classe_texto = dict_classes.get(str(classe_processual))
#
#     dict_textos = {'mov_origem': mov_origem_texto, 'mov_destino': mov_destino_texto, 'classe': classe_texto}
#
#     return dict_textos

def getjson_textos(classe_processual, mov_origem, mov_destino):

    with open('sgt_movimentos.json' , 'r') as arquivo:
        data = json.load(arquivo)

    mov_origem_texto_raw = data[mov_origem]
    mov_origem_texto = mov_origem_texto_raw.get('descricao')

    mov_destino_texto_raw = data[mov_destino]
    mov_destino_texto = mov_destino_texto_raw.get('descricao')

    dict_classes = {'7': 'Procedimento Comum Cível', '1116': 'Execução Fiscal', '159' : 'Execução de Título Extrajudicial', '283': 'Ação Penal - Procedimento Ordinário'}
    classe_texto = dict_classes.get(str(classe_processual))

    dict_textos = {'mov_origem': mov_origem_texto, 'mov_destino': mov_destino_texto, 'classe': classe_texto}

    return dict_textos

def consulta_cor(movimento):
    with open('analisados.json', 'r') as arquivo:
        data = json.load(arquivo)
        cor_tabela = data.get(movimento)
        if cor_tabela:
            color = cor_tabela
        else:
            color = 'secondary'

    return color


def mudar_cor(movimento, novacor):
    with open('analisados.json', 'r') as arquivo:
        data = json.load(arquivo)

    if data.get(movimento):
        data[movimento] = novacor

    with open('analisados.json', 'w') as arquivo:
        json.dump(data, arquivo)

# # criar_json_cores
# data_jsoncores = {}
#
# for i in lista_movimentos:
#     data_jsoncores[i] = 'secondary'
#
# with open('analisados.json' , 'w') as arquivo:
#     json.dump(data_jsoncores , arquivo)


# criar_json estatisticas

# dict_criarjsonestatiticas = {}
#
# with open('lista_movimentos.csv') as csvfile:
#     data = csv.reader(csvfile, delimiter=';')
#
#     for row in data:
#
#         if str(row[1][0:3]) == 'mov':
#             pass
#         else:
#             dict_linha = {'mov_origem': str(row[1]), 'mov_destino': str(row[2]), 'classe_processual': row[7],
#                           'siglaTribunal': row[8], 'ocorrencias': row[3], 'prob': row[4], 'alerta': row[5],
#                           'prob_nacional': row[6]}
#
#             key_principal = str(row[1]) + '_' + str(row[2]) + '_' + row[7] + '_' + row[8]
#
#             dict_criarjsonestatiticas[key_principal] = dict_linha
#
# with open('lista_movimentos.json' , 'w') as arquivo:
#     json.dump(dict_criarjsonestatiticas, arquivo)

# criar json movimentos
#
# dict_criarjsonmovimentos = {}
#
# with open('sgt_movimentos.csv') as csvfile:
#     data = csv.reader(csvfile, delimiter=';')
#
#     for row in data:
#
#         if str(row[1][0:3]) == 'cod':
#             pass
#         else:
#
#             dict_linha = {'codigo': str(row[0]), 'descricao': str(row[1]), 'cod_pai': row[2][0:-3], 'cod_filhos': row[3]}
#             key_principal = str(row[0])
#             dict_criarjsonmovimentos[key_principal] = dict_linha
#
# with open('sgt_movimentos.json' , 'w') as arquivo:
#     json.dump(dict_criarjsonmovimentos, arquivo)