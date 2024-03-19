from typing import Optional
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from fastapi import FastAPI

app = FastAPI()

df_example = pd.DataFrame([[1,2],[3,4]], columns=['col1', 'col2'])


@app.get("/")
async def root():
    return {"juegos": df_example['col1'].tolist()}
    # return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
    
@app.get("/{nombre}")
async def saludo(nombre: str):
    saludo_st: str = f"Hello {nombre}!!!"
    
    return {"message": saludo_st}

@app.get("/recommend/{id_juego}")
async def recommend(id_juego: int):
    
    def comparar(id_1, id_2):
        row1 = matriz_dummies.loc[id_1].values.reshape(1, -1)
        row2 = matriz_dummies.loc[id_2].values.reshape(1, -1)
        return cosine_similarity(row1, row2)    

    matriz_dummies = pd.read_csv('matriz_dummies.csv', index_col='id_game')
    
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

@app.get("/UsersRecommend/{anio}")
async def UsersRecommend(anio: int):
    df_revs_filtrada = pd.read_csv('df_revs_filtrada.csv')
    disponibles = df_revs_filtrada.year_posted.unique()
    if anio not in disponibles:
        return {"Error": "Año no encontrado"}
    top3 = df_revs_filtrada.query("year_posted == 2016").groupby(['item_id', 'year_posted']).sum(['reviews_sent', 'recommend']).sort_values(by='recommend', ascending=False).head(3)
    top3.reset_index(inplace=True)
    
    salida = [{f'Puesto {i+1}': str(row[0])} for i, row in enumerate(top3.values)]

    print(salida)
    # anio_maximo = genero_estadisticas.query(f"genres_x == '{genero}'")['playtime_forever'].sort_values(ascending=False)
    # anio: str = pd.DataFrame(anio_maximo).reset_index().release_year.values[0]
    return salida
