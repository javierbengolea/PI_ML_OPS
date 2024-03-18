import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def get_recommended(id_juego):
    def comparar(id_1, id_2):
        row1 = matriz_dummies.loc[id_1].values.reshape(1, -1)
        row2 = matriz_dummies.loc[id_2].values.reshape(1, -1)
        return cosine_similarity(row1, row2)    


    matriz_dummies = pd.read_csv('matriz_dummies.csv', index_col='id_juego')

    lista = []
    # id_juego = matriz_dummies.sample().index

    for i in matriz_dummies.index.tolist():
        if i != id_juego:
            (a, b) = i, comparar(id_juego, i)
            if 0.5 < b[0][0] <= 1:
                lista.append((a, b[0][0]))
    
    return pd.DataFrame(lista, columns=['id_juego', 'similitud']).sort_values('similitud', ascending=False).head(5)
    

id_juego = 314010

recomendados = get_recommended(id_juego)

# for i in recomendados.index:
    # print(recomendados.loc[i])
# print(matriz_dummies.index)
print(recomendados.to_json())
