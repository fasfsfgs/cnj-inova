from flask import Flask, render_template, flash, redirect, session
from flask_bootstrap import Bootstrap
from functionsdb import getjson_alertabd, getjson_textos, consulta_cor, mudar_cor
from subir_csv import lista_movimentos


application = app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'jkjkjhkjhkhk'


@app.route('/')
def index():
    return redirect('/analisar')


@app.route('/alerta/<classe_processual>/<mov_origem>/<mov_destino>/<tribunal>')
def alerta(classe_processual, mov_origem, mov_destino, tribunal):
    alerta = getjson_alertabd(
        classe_processual, mov_origem, mov_destino, tribunal)
    textos = getjson_textos(classe_processual, mov_origem, mov_destino)

    alerta['linksim'] = '/acao/' + classe_processual + '/' + \
        mov_origem + '/' + mov_destino + '/' + tribunal + '/sim'
    alerta['linknao'] = '/acao/' + classe_processual + '/' + \
        mov_origem + '/' + mov_destino + '/' + tribunal + '/nao'

    return render_template('alerta.html', alerta=alerta, textos=textos)


@app.route('/analisar')
def analisar():

    lista_movimentos_display = []

    for i in lista_movimentos:

        cor = consulta_cor(i)
        movimento = i.split('_')
        movimento_display = f'Movimento {movimento[0]} ---> Movimento {movimento[1]} no {movimento[3]}'
        link_movimento = f'/alerta/{movimento[2]}/{movimento[0]}/{movimento[1]}/{movimento[3]}'
        dict_movimento_display = {
            'display': movimento_display, 'link_movimento': link_movimento, 'cor': cor}
        lista_movimentos_display.append(dict_movimento_display)

    return render_template('analisar.html', lista_movimentos_display=lista_movimentos_display)


@app.route('/acao/<classe_processual>/<mov_origem>/<mov_destino>/<tribunal>/<acao>')
def acao_mudar_cor(classe_processual, mov_origem, mov_destino, tribunal, acao):

    mov_origem_destino = str(mov_origem) + '_' + str(mov_destino)
    classe_processual = '_' + classe_processual
    siglaTribunal = '_' + tribunal
    movimento = mov_origem_destino + classe_processual + siglaTribunal

    if acao == 'sim':
        mudar_cor(movimento, 'success')

    if acao == 'nao':
        mudar_cor(movimento, 'danger')

    return redirect('/analisar')


if __name__ == '__main__':
    app.run()
