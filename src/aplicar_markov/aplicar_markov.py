import pandas as pd
import networkx as nx
import numpy as np


# FUNÇÃO: Inserir dado em DF_final


def insert(DF_final, row):
    insert_loc = DF_final.index.max()

    if np.isnan(insert_loc):
        DF_final.loc[0] = row
    else:
        DF_final.loc[insert_loc + 1] = row

    return DF_final


# FUNÇÃO: Converte a matriz em dados antes de inserir no DF_final


def save_in_df(DF_final, movimentos_, A_, P_, Global_, Alerta_, Classes_, Trib_, g, PG_df):
    for i in range(len(movimentos_.index)):
        # print(x.iat[i,0],"->",x.iat[i,1],":",g.number_of_edges(x.iat[i,0],x.iat[i,1]))
        insert(DF_final, [
            movimentos_.iat[i, 0],
            movimentos_.iat[i, 1],
            g.number_of_edges(movimentos_.iat[i, 0], movimentos_.iat[i, 1]),
            P_.at[movimentos_.iat[i, 0], movimentos_.iat[i, 1]],
            Alerta_,
            PG_df.at[movimentos_.iat[i, 0], movimentos_.iat[i, 1]],
            Classes_,
            Trib_
        ])

    return DF_final


def aplicar(processos):
    DF_final = pd.DataFrame(columns=['mov_origem', 'mov_destino', 'ocorrencias',
                                     'prob', 'alerta', 'prob_Nac', 'classe_processual', 'siglaTribunal'])

    df = processos.dropna(subset=['movimentos'])

    classes_escolhidas = [1116, 7, 159, 283]
    tribunais = ['TJSP', 'TJPR', 'TJRJ', 'TJBA', 'TJSC', 'TJES', 'TJPE', 'TJGO', 'TJRO', 'TJAM', 'TJAL', 'TJMG', 'TJMT',
                 'TJCE', 'TJRN', 'TJTO', 'TJPB', 'TJDFT', 'TJPA', 'TJMS', 'TJSE', 'TJAC', 'TJPI', 'TJRS', 'TJMA', 'TJRR', 'TJAP']

    for classe_escolhida in classes_escolhidas:
        df_classe = df[(df.classe_processual == classe_escolhida)]
        g_nacional = nx.MultiDiGraph()

        count2 = 0
        for row in df_classe.index:  # Percorre todas a linhas do df
            # captura os movimentos e transforma em uma lista (vetor)
            mov2 = df.iloc[row]['movimentos'].split(",")
            # percorre a lista de movimentos para gerar os Nós
            for st2 in range(0, len(mov2)-1):
                origem2 = mov2[st2]
                destino2 = mov2[st2+1]
                if destino2 != None:  # eliminas processos com somente um movimento
                    # adicionamos as transições (arestas)
                    g_nacional.add_edge(origem2, destino2)
            count2 = count2+1

        print(classe_escolhida, " GLOBAL analisado!")
        # 2)MATRIZ DE TRANSIÇÃO UNITÁRIA
        AG = nx.to_numpy_matrix(g_nacional)
        ndg = g_nacional.nodes()
        AG_df = pd.DataFrame(AG, index=ndg, columns=ndg)
        # 2)MATRIZ DE PROBABILIDADE
        PG = AG/AG.sum(axis=1)
        PG_df = pd.DataFrame(PG, index=ndg, columns=ndg)

        for tribunal in tribunais:
            df_tribunal = df_classe[(df_classe.siglaTribunal == tribunal)]

            # MultiDiGraph - Gráfos direcionados com auto-loops e arestas paralelas
            g = nx.MultiDiGraph()

            count = 0
            for row in df_tribunal.index:  # Percorre todas a linhas do df
                # captura os movimentos e transforma em uma lista (vetor)
                mov = df.iloc[row]['movimentos'].split(",")
                # percorre a lista de movimentos para gerar os Nós
                # com base da origem -> destivo
                for st in range(0, len(mov)-1):
                    origem = mov[st]
                    destino = mov[st+1]
                    if destino != None:  # eliminas processos com somente um movimento
                        # print(count,":",origem,"-->",destino)
                        # adicionamos as transições (arestas)
                        g.add_edge(origem, destino)
                        # MELHORAR: add_path([0,1,2,3,4,5,6,7,8,9]) https://networkx.github.io/documentation/networkx-1.11/reference/classes.multidigraph.html
                count = count+1
            print(classe_escolhida, ":", tribunal, " analisado!")

            movimentos = pd.DataFrame(g.edges()).drop_duplicates()

            # 2)MATRIZ DE TRANSIÇÃO UNITÁRIA
            A = nx.to_numpy_matrix(g)
            nd = g.nodes()
            A_df = pd.DataFrame(A, index=nd, columns=nd)
            # print(A_df)
            # 2)MATRIZ DE PROBABILIDADE
            P = A/A.sum(axis=1)
            P_df = pd.DataFrame(P, index=nd, columns=nd)
            # print(P_df)

            # 2)MATRIZ DE ESCALA
            P = A/A.sum(axis=1)
            P_df = pd.DataFrame(P, index=nd, columns=nd)
            # print(P_df)

            # Salva no DF_final
            save_in_df(DF_final, movimentos, A_df, P_df, PG_df,
                       'xxx', classe_escolhida, tribunal, g, PG_df)

            print(DF_final.head)

    DF_final['alerta'] = DF_final['prob'] - DF_final['prob_Nac']
    DF_final['alerta'] = DF_final['alerta'] / DF_final['prob_Nac']
    DF_final['alerta'] = DF_final['alerta'].abs()

    DF_final = DF_final[(DF_final['alerta'] > 10.34)]

    DF_final = DF_final.sort_values('alerta', ascending=False)

    return DF_final
