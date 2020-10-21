from json2csv.json2csv import obter_df
from aplicar_markov.aplicar_markov import aplicar as aplicar_markov
from aplicar_markov.gerar_json import criar_json_fromcsv


def main():
    dataframe = obter_df()
    df_markov = aplicar_markov(dataframe)

    nome_arquivo_markov = 'lista_movimentos.csv'
    df_markov.to_csv(nome_arquivo_markov)
    criar_json_fromcsv(nome_arquivo_markov)


if __name__ == "__main__":
    main()
