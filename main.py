from typing import Optional
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    '''
    Mensaje de Inicio
    
    '''
    return {"titulo": "PROYECTO INDIVIDUAL Nº1", "tema": "Machine Learning Operations (MLOps)",
            "autor": "Javier Bengolea"}


@app.get("/PlayTimeGenre/{genero}")
async def PlayTimeGenre(genero: str):
    '''
    Devuelve el año con más horas jugadas para el genero provisto.
    
    Parámetros:
        genero (string): _Genero de Juego_.        
        Ejemplo: 'Action'
    '''
    genero_estadisticas = pd.read_csv('datasets/generos_estadisticas.csv')
    disponibles = genero_estadisticas.genres_x.unique()
    if genero not in disponibles:
        return {"Error": "Género no encontrado"}
    genero_estadisticas = genero_estadisticas.set_index(['genres_x', 'release_year'])
    anio_maximo = genero_estadisticas.query(f"genres_x == '{genero}'")['playtime_forever'].sort_values(ascending=False)
    anio: str = pd.DataFrame(anio_maximo).reset_index().release_year.values[0]
    return {f'Año Lanzamiento con màs horas jugadas para el genero {genero}: ': str(anio)}

@app.get("/UserForGenre/{genero}")
async def UserForGenre( genero : str ):
    
    '''
    Devuelve el usuario que más hora jugó a un género y lo detalla por año.
    
    Parámetros:
        genero (string): _Genero de Juego_.
        Ejemplo: 'Indie'
    '''
    
    usuario_genero = pd.read_csv('datasets/usuario_genero.csv').reset_index()
    disponibles = usuario_genero.genres.unique()
    if genero not in disponibles:
        return {"Error": f"Genero '{genero}' no encontrado"}
    usuario = usuario_genero.query(f'genres == "{genero}"').head(1).user_id.values[0]
    usuarios_genero_horas = pd.read_csv('datasets/merged_2.csv')
    # print(usuarios_genero_horas.query(f"user_id =='{usuario}' and genres == '{genero}'"))
    query = usuarios_genero_horas.query(f"user_id =='{usuario}' and genres == '{genero}'")
    query = query.reset_index()
    salida = [{f'Año {row[3]}': str(round(row[4]/60))} for i, row in enumerate(query.values)]
    # print(salida)
    return {f"Usuario con más horas jugadas para el género '{genero}': ": str(usuario),
            'Horas Jugadas: ': salida}

@app.get("/UserRecommend/{anio}")
async def UserRecommend(anio: int):
    '''
    Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. 
    
    Parámetros:
        anio (int): _Año de Recomendación y/o Review_.        
        Example: '2015'
    '''
    df_revs_filtrada = pd.read_csv('datasets/df_revs_filtrada.csv')
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



@app.get("/UsersWorstDeveloper/{anio}")
async def UsersWorstDeveloper( anio : int ): 
    '''
    Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado.
    
    Parámetros:
        anio (int): _Año de Recomendación y/o Review_.        
        Example: 2015
    '''
    dev_rec = pd.read_csv('datasets/developer_year_rec.csv')
    disponibles = dev_rec.year_posted.unique()
    if anio not in disponibles:
        return {"Error": f"Año '{anio}' no encontrado"}

    query = dev_rec.query(f"year_posted == {anio}").head(3)

    print(anio)

    salida = [{f'Puesto {i+1}': str(row[0])} for i, row in enumerate(query.values)]
    return salida

@app.get("/SentimentAnalysis/{developer}")
async def sentiment_analysis(developer : str ):
    '''
    Devuelve la desarrolladora y una lista con la cantidad total 
    de registros de reseñas de usuarios que se encuentren categorizados 
    con un análisis de sentimiento como valor.
    
    Parámetros:
    Developer (int): _Desarrolladora_.        
    Ejemplo: 'Valve'
    '''
    df_rev_sent = pd.read_csv('datasets/des_reviews_sent.csv')
    # developer = 'Valve'
    
    if developer not in df_rev_sent.developer.unique():
        return {"Error": f"Developer '{developer}' no encontrado"}
    
    print(df_rev_sent.query(f"developer == '{developer}' and review_sent == 0").count().review_sent)
    negativas = df_rev_sent.query(f"developer == '{developer}' and review_sent == 0").count().review_sent
    neutrales = df_rev_sent.query(f"developer == '{developer}'  and review_sent == 1").count().review_sent
    positivas = df_rev_sent.query(f"developer == '{developer}'  and review_sent == 2").count().review_sent
    salida = {'Negativas': str(negativas), 'Neutrales': str(neutrales), 'Positivas': str(positivas)}
    
    return {"developer": developer, 'reviews':salida}

@app.get("/recommend/{id_juego}")
async def recommend(id_juego: int):
    """
    Retorna una recomendación de 5 juegos en base al parámetro id_juego.

    Parámetros:
        id_juego (int): _id de juego_
    """
    def comparar(id_1, id_2):
        row1 = matriz_dummies.loc[id_1].values.reshape(1, -1)
        row2 = matriz_dummies.loc[id_2].values.reshape(1, -1)
        return cosine_similarity(row1, row2)    

    matriz_dummies = pd.read_csv('datasets/matriz_dummies_filtrada.csv', index_col='id_game')


    if id_juego not in matriz_dummies.index:
        return {'Error' : f'Id de juego {id_juego} no encontrado!!!'}
    
    row1 = matriz_dummies.loc[id_juego].values.reshape(1, -1)
    
    similarities = cosine_similarity(matriz_dummies.values, row1)
    similar_games = [(game_id, sim) for game_id, sim in zip(matriz_dummies.index, similarities) if 0.5 < sim[0] <= 1 and game_id != id_juego]
    juegos_rec = pd.DataFrame(similar_games, columns=['id_game', 'similitud']).sort_values('similitud', ascending=False).head(5)

    df_names = pd.read_csv('datasets/df_games_names.csv')
    nombres = []
    ids = juegos_rec['id_game'].tolist()

    
    salida = [{ids[i] : df_names.query(f"id_game == {x}").app_name.values[0]} for i, x in enumerate(ids)]

    return {"juego: ":  {id_juego : df_names.query(f"id_game == {id_juego}").app_name.values[0]}, "recomendados": salida}