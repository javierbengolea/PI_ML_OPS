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


    matriz_dummies = pd.read_csv('matriz_dummies.csv', index_col='id_juego')

    lista = []
    # id_juego = matriz_dummies.sample().index

    for i in matriz_dummies.index.tolist():
        if i != id_juego:
            (a, b) = i, comparar(id_juego, i)
            if 0.5 < b[0][0] <= 1:
                lista.append((a, b[0][0]))
    
    juegos_rec = pd.DataFrame(lista, columns=['id_juego', 'similitud']).sort_values('similitud', ascending=False).head(5)


    return {"juegos": juegos_rec['id_juego'].tolist()}
