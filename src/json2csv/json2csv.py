import glob
import os

import pandas as pd


###
#  funções para extrair dados das colunas
###


def assunto_principal(row):
    # Obter assunto principal que possui código nacional
    # Se não tiver código nacional, obter código pai nacional
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


def processo_vinculado(row):
    return row.get('dadosBasicos').get('processoVinculado')


def relacao_incidental(row):
    return row.get('dadosBasicos').get('relacaoIncidental')


def outros_numeros(row):
    return row.get('dadosBasicos').get('outrosnumeros')


def codigo_localidade(row):
    return row.get('dadosBasicos').get('codigoLocalidade')


def intervencao_mp(row):
    return row.get('dadosBasicos').get('intervencaoMP')


def proc_el(row):
    return row.get('dadosBasicos').get('procEl')


def dsc_sistema(row):
    return row.get('dadosBasicos').get('dscSistema')


def orgao_julgador_nome(row):
    return orgao_julgador_param(row, 'nomeOrgao')


def orgao_julgador_cod_municipio_ibge(row):
    return orgao_julgador_param(row, 'codigoMunicipioIBGE')


def orgao_julgador_cod_orgao(row):
    return orgao_julgador_param(row, 'codigoOrgao')


def orgao_julgador_instancia(row):
    return orgao_julgador_param(row, 'instancia')


def orgao_julgador_param(row, param):
    orgao_julgador = row.get('dadosBasicos').get('orgaoJulgador')
    if not orgao_julgador:
        return None
    return orgao_julgador.get(param)


def movimentos(row):
    # Obter os movimentos que possuem código nacional entre vírgulas
    movimentos = row.get('movimento')
    if not movimentos:
        return ''
    movimentos_com_codigo_nacional = list(
        filter(possui_codigo_movimento_nacional, movimentos)
    )
    movimentos_ordenados = sorted(
        movimentos_com_codigo_nacional, key=lambda mov: mov.get('dataHora')
    )
    codigos_movimento = list(
        map(
            lambda mov: mov.get('movimentoNacional').get('codigoNacional'),
            movimentos_ordenados,
        )
    )
    str_codigos_movimento = [str(int) for int in codigos_movimento]
    return ','.join(str_codigos_movimento)


def possui_codigo_movimento_nacional(movimento):
    if 'movimentoNacional' not in movimento:
        return False
    if not movimento.get('movimentoNacional'):
        return False
    return 'codigoNacional' in movimento.get('movimentoNacional')


###
# gerar df
###

def colunas():
    return [
        'millisInsercao',
        'grau',
        'siglaTribunal',
        'numero',
        'classe_processual',
        'assunto_principal',
        'competencia',
        'data_ajuizamento',
        'prioridade',
        'valor_causa',
        'processo_vinculado',
        'relacao_incidental',
        'outros_numeros',
        'codigo_localidade',
        'intervencao_mp',
        'proc_el',
        'dsc_sistema',
        'orgao_julgador_nome',
        'orgao_julgador_cod_municipio_ibge',
        'orgao_julgador_cod_orgao',
        'orgao_julgador_instancia',
        'movimentos',
    ]


def gerar_df(jsonFile, indice, total):
    print('%d de %d |' % (indice + 1, total), jsonFile)
    df = pd.read_json(open(jsonFile))
    df['numero'] = df.apply(numero, axis=1)
    df['classe_processual'] = df.apply(classe_processual, axis=1)
    df['assunto_principal'] = df.apply(assunto_principal, axis=1)
    df['competencia'] = df.apply(competencia, axis=1)
    df['data_ajuizamento'] = df.apply(data_ajuizamento, axis=1)
    df['prioridade'] = df.apply(prioridade, axis=1)
    df['valor_causa'] = df.apply(valor_causa, axis=1)
    df['processo_vinculado'] = df.apply(processo_vinculado, axis=1)
    df['relacao_incidental'] = df.apply(relacao_incidental, axis=1)
    df['outros_numeros'] = df.apply(outros_numeros, axis=1)
    df['codigo_localidade'] = df.apply(codigo_localidade, axis=1)
    df['intervencao_mp'] = df.apply(intervencao_mp, axis=1)
    df['proc_el'] = df.apply(proc_el, axis=1)
    df['dsc_sistema'] = df.apply(dsc_sistema, axis=1)
    df['orgao_julgador_nome'] = df.apply(orgao_julgador_nome, axis=1)
    df['orgao_julgador_cod_municipio_ibge'] = df.apply(
        orgao_julgador_cod_municipio_ibge, axis=1
    )
    df['orgao_julgador_cod_orgao'] = df.apply(orgao_julgador_cod_orgao, axis=1)
    df['orgao_julgador_instancia'] = df.apply(orgao_julgador_instancia, axis=1)
    df['movimentos'] = df.apply(movimentos, axis=1)
    return df[colunas()]


def obter_df():
    searchPath = os.getcwd() + '/data/justica_estadual/**/*.json'

    jsonFiles = glob.glob(searchPath, recursive=True)
    qtdeJsons = len(jsonFiles)
    print('%d jsons encontrados...' % qtdeJsons)

    dfs = [gerar_df(jsonFile, ind, qtdeJsons)
           for ind, jsonFile in enumerate(jsonFiles)]

    print('Concatenando os dataframes...')
    df = pd.concat(dfs)

    return df
