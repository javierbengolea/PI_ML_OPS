from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
    
@app.get("/{nombre}")
async def saludo(nombre: str):
    saludo_st: str = f"Hello {nombre}!!!"
    
    return {"message": saludo_st}
