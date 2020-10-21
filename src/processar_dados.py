from json2csv.json2csv import obter_df
from aplicar_markov.aplicar_markov import aplicar as aplicar_markov


def main():
    dataframe = obter_df()
    df_markov = aplicar_markov(dataframe)

    df_markov.to_json('lista_movimentos.json')


if __name__ == "__main__":
    main()
