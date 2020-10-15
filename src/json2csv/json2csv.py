import glob
import os

import pandas as pd


# extrair dados das colunas


def assunto_principal(row):
    assuntos = row.get('dadosBasicos').get('assunto')
    if not assuntos:
        return None
    assuntos_principais = [
        assunto for assunto in assuntos if assunto.get('principal')]
    if not assuntos_principais:
        return None
    assunto_principal = assuntos_principais[0]
    if 'codigoNacional' in assunto_principal:
        return assunto_principal.get('codigoNacional')
    if 'codigoPaiNacional' in assunto_principal:
        return assunto_principal.get('codigoPaiNacional')
    return None


def classe_processual(row):
    return row.get('dadosBasicos').get('classeProcessual')


def data_ajuizamento(row):
    return row.get('dadosBasicos').get('dataAjuizamento')


def numero(row):
    return row.get('dadosBasicos').get('numero')


def prioridade(row):
    return row.get('dadosBasicos').get('prioridade')


def valor_causa(row):
    return row.get('dadosBasicos').get('valor_causa')


def competencia(row):
    return row.get('dadosBasicos').get('competencia')


def movimentos(row):
    movimentos = row.get('movimento')
    if not movimentos:
        return ''
    movimentos_com_codigo_nacional = list(
        filter(possui_codigo_movimento_nacional, movimentos))
    movimentos_ordenados = sorted(
        movimentos_com_codigo_nacional, key=lambda mov: mov.get('dataHora'))
    codigos_movimento = list(map(lambda mov: mov.get(
        'movimentoNacional').get('codigoNacional'), movimentos_ordenados))
    str_codigos_movimento = [str(int) for int in codigos_movimento]
    return ','.join(str_codigos_movimento)


def possui_codigo_movimento_nacional(movimento):
    if 'movimentoNacional' not in movimento:
        return False
    return 'codigoNacional' in movimento.get('movimentoNacional')


# gerar dfs


cols = [
    'numero',
    'classe_processual',
    'assunto_principal',
    'competencia',
    'data_ajuizamento',
    'prioridade',
    'valor_causa',
    'movimentos']


def gerar_df(jsonFile, indice, total):
    print('%d de %d |' % (indice+1, total), jsonFile)
    df = pd.read_json(open(jsonFile))
    df['numero'] = df.apply(numero, axis=1)
    df['classe_processual'] = df.apply(classe_processual, axis=1)
    df['assunto_principal'] = df.apply(assunto_principal, axis=1)
    df['competencia'] = df.apply(competencia, axis=1)
    df['data_ajuizamento'] = df.apply(data_ajuizamento, axis=1)
    df['prioridade'] = df.apply(prioridade, axis=1)
    df['valor_causa'] = df.apply(valor_causa, axis=1)
    df['movimentos'] = df.apply(movimentos, axis=1)
    return df[cols]


searchPath = os.getcwd() + '/data/justica_estadual/**/*.json'

jsonFiles = glob.glob(searchPath, recursive=True)
qtdeJsons = len(jsonFiles)
print('%d jsons encontrados...' % qtdeJsons)

dfs = [gerar_df(jsonFile, ind, qtdeJsons)
       for ind, jsonFile in enumerate(jsonFiles)]

print('Concatenando os dataframes...')
df = pd.concat(dfs)

print('Transformando em csv...')
os.makedirs('out', exist_ok=True)
csv = df.to_csv(
    path_or_buf='out/data.csv',
    index=False,
    header=True,
    columns=cols)
