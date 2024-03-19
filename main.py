from typing import Optional
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from fastapi import FastAPI

app = FastAPI()



@app.get("/")
async def root():
    # return {"juegos": df_example['col1'].tolist()}
    return {"message": "Hello World"}

@app.get("/recommend/{id_juego}")
async def recommend(id_juego: int):
    
    def comparar(id_1, id_2):
        row1 = matriz_dummies.loc[id_1].values.reshape(1, -1)
        row2 = matriz_dummies.loc[id_2].values.reshape(1, -1)
        return cosine_similarity(row1, row2)    

    matriz_dummies = pd.read_csv('matriz_dummies_filtrada.csv', index_col='id_game')
    
    # print(matriz_dummies.loc[id_juego])

    lista = []
    # id_juego = matriz_dummies.sample().index

    if id_juego not in matriz_dummies.index:
        return {'message' : 'id_game not found!!!'}

    for i in matriz_dummies.index.tolist():
        if i != id_juego:
            (a, b) = i, comparar(id_juego, i)
            if 0.5 < b[0][0] <= 1:
                lista.append((a, b[0][0]))
    
    juegos_rec = pd.DataFrame(lista, columns=['id_game', 'similitud']).sort_values('similitud', ascending=False).head(5)


    return {"juegos": juegos_rec['id_game'].tolist()}

@app.get("/PlayTimeGenre/{genero}")
async def PlayTimeGenre(genero: str):
    genero_estadisticas = pd.read_csv('generos_estadisticas.csv')
    disponibles = genero_estadisticas.genres_x.unique()
    if genero not in disponibles:
        return {"Error": "Género no encontrado"}
    genero_estadisticas = genero_estadisticas.set_index(['genres_x', 'release_year'])
    anio_maximo = genero_estadisticas.query(f"genres_x == '{genero}'")['playtime_forever'].sort_values(ascending=False)
    anio: str = pd.DataFrame(anio_maximo).reset_index().release_year.values[0]
    return {'Año Lanzamiento: ': str(anio)}

@app.get("/UserRecommend/{anio}")
async def UserRecommend(anio: int):
    df_revs_filtrada = pd.read_csv('df_revs_filtrada.csv')
    disponibles = df_revs_filtrada.year_posted.unique()
    if anio not in disponibles:
        return {"Error": "Año no encontrado"}
    top3 = df_revs_filtrada.query(f"year_posted == {anio}").groupby(['item_id', 'year_posted']).sum(['reviews_sent', 'recommend']).sort_values(by='recommend', ascending=False).head(3)
    top3.reset_index(inplace=True)
    
    salida = [{f'Puesto {i+1}': str(row[0])} for i, row in enumerate(top3.values)]

    print(salida)
    # anio_maximo = genero_estadisticas.query(f"genres_x == '{genero}'")['playtime_forever'].sort_values(ascending=False)
    # anio: str = pd.DataFrame(anio_maximo).reset_index().release_year.values[0]
    return salida

@app.get("/UsersForGenre/{genero}")
async def UserForGenre( genero : str ):
    usuario_genero = pd.read_csv('usuario_genero.csv').reset_index()
    disponibles = usuario_genero.genres.unique()
    if genero not in disponibles:
        return {"Error": f"Genero '{genero}' no encontrado"}
    usuario = usuario_genero.query(f'genres == "{genero}"').head(1).user_id.values[0]
    usuarios_genero_horas = pd.read_csv('merged_2.csv')
    # print(usuarios_genero_horas.query(f"user_id =='{usuario}' and genres == '{genero}'"))
    query = usuarios_genero_horas.query(f"user_id =='{usuario}' and genres == '{genero}'")
    query = query.reset_index()
    salida = [{f'Año {row[3]}': str(round(row[4]/60))} for i, row in enumerate(query.values)]
    print(salida)
    return {f"Usuario con más horas jugadas para el género '{genero}': ": str(usuario),
            'Horas Jugadas: ': salida}

@app.get("/UsersWorstDeveloper/{anio}")
def UsersWorstDeveloper( anio : int ): 
    '''
    Retorna las compañías desarrolladoras con menos recomendaciones y más comentarios negativos por
    '''
    dev_rec = pd.read_csv('developer_year_rec.csv')
    disponibles = dev_rec.year_posted.unique()
    if anio not in disponibles:
        return {"Error": f"Año '{anio}' no encontrado"}

    query = dev_rec.query(f"year_posted == {anio}").head(3)

    print(anio)

    salida = [{f'Puesto {i+1}': str(row[0])} for i, row in enumerate(query.values)]
    return salida