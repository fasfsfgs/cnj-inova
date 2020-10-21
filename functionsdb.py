import json
import csv

def getjson_alertabd(classe_processual, mov_origem, mov_destino, tribunal):

    with open('lista_movimentos.json', 'r') as arquivo:
        data = json.load(arquivo)

    movimento = mov_origem + '_' + mov_destino + '_' + classe_processual + '_' + tribunal

    alerta = data[movimento]

    # alerta é um dicionário contendo todos os dados da linha {nomedacoluna: resultado}
    return alerta

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
