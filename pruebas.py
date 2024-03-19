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
    

id_juego = 323900

# recomendados = get_recommended(id_juego)

# for i in recomendados.index:
    # print(recomendados.loc[i])
# print(matriz_dummies.index)
# print(recomendados.to_json())

# genero_estadisticas = pd.read_csv('generos_estadisticas.csv')
# genero_estadisticas = genero_estadisticas.set_index(['genres_x', 'release_year'])
# anio_maximo = genero_estadisticas.query(f"genres_x == 'Action'")['playtime_forever'].sort_values(ascending=False).head(1)
# anio = pd.DataFrame(anio_maximo).reset_index().release_year.values[0]

# print(anio)

df_revs_filtrada = pd.read_csv('df_revs_filtrada.csv')

print(df_revs_filtrada.info())

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def comparar(row1, row2):
    return cosine_similarity(row1, row2)

matriz_dummies = pd.read_csv('matriz_dummies_filtrada.csv', index_col='id_game')

def find_similar_games(id_juego, matriz_dummies):
    if id_juego not in matriz_dummies.index:
        return {'Error': f'{id_juego} No Encontrado'}

    row1 = matriz_dummies.loc[id_juego].values.reshape(1, -1)
    similarities = cosine_similarity(matriz_dummies.values, row1)
    similar_games = [(game_id, sim) for game_id, sim in zip(matriz_dummies.index, similarities) if 0.5 < sim[0] <= 1 and game_id != id_juego]
    juegos_rec = pd.DataFrame(similar_games, columns=['id_game', 'similitud']).sort_values('similitud', ascending=False).head(5)
    return juegos_rec

id_juego =  4000# Your game ID here
result = find_similar_games(id_juego, matriz_dummies)
print(result)
