# PROYECTO INDIVIDUAL N° 1

## Machine Learning Operations

* **Alumno**: Javier Bengolea.
* **Carrera**: Data Science.
* **Cohorte**: Data PT 07.

## Descripción del Proyecto

Se nos da el acceso a 3 Datasets de la Empresa [Steam](https://store.steampowered.com/?l=spanish) con información de Productos (Juegos de video), las reseñas de Usuarios y estadísticas de juego.

Realizamos un proceso de ETL (Extracción y Carga de Datos) para obtener la información y procesarla, para luego desarrollar un EDA (Análisis Exploratorio de Datos) con el fin de extraer la mayor información disponible.

El objetivo es llegar a un MVP (Producto Mínimo Viable), consistente en una API con Endpoints que devuelvan información sobre estadísticas (juegos, desarrolladoras, usuarios), Análisis de Sentimiento en base a las reseñas dejadas de cada producto por los usuarios y un Sistema de Recomendación.

## Estructura

El proyecto está constituido por:

1. Notebook de Jupyter [main.ipynb](https://github.com/javierbengolea/PI_ML_OPS/blob/master/main.ipynb): Es en donde se lleva a cabo todo el proceso de Transformación y Análisis de datos y la generación de Datasets necesarios para la API.
2. Archivo [main.py](https://github.com/javierbengolea/PI_ML_OPS/blob/master/main.py): Es el archivo de Python donde se encuentra implementada la API. Se utiliza el Framework [FastAPI](https://fastapi.tiangolo.com/).
3. Archivo [Requeriments.txt](https://github.com/javierbengolea/PI_ML_OPS/blob/master/requirements.txt): Es necesario para llevar a cabo el Deployment de la Aplicación, nos dice las librerías de Python necesarias. Se utiliza el servicio de [Render](https://render.com/) para tal fin.
4. Carpeta [datasets](https://github.com/javierbengolea/PI_ML_OPS/tree/master/datasets): En esta carpeta se encuentran los datasets generados para la ejecución de los Endpoints de la API.

## Producto Mínimo Viable

El producto mínimo viable consiste en una API con 6 Endpoints:

* ```GET /PlayTimeGenre/{genero}```: Año que más horas se jugaron a un género.
* ```GET /UserForGenre/{genero}```: Usuario que jugó más tiempo a un género y detalle de horas anuales.
* ```GET /UserRecommend/{anio}```: Top 3 de juegos más recomendados para un año dado.
* ```GET /UsersWorstDeveloper/{anio}```: Top 3 de desarrolladoras menos recomendadas para un año dado.
* ```GET /SentimentAnalysis/{developer}```: Análisis de Sentimiento para una desarrolladora dada, se toman las reseñas y se categorizan y contabilizan en negativas, neutrales y positivas.
* ```GET /recommend/{id_juego}```: Dado un juego como parámetro se aplica un algoritmo que devuelve 5 juegos similares.

Estas funcionalidades están implementadas y documentadas en [Link Render](https://pi-ml-ops-b4cf.onrender.com/docs).

## Implementación de Machine Learning

Para el Sistema de Recomendación, se utiliza un algoritmo que implica la `Similitud del Coseno`, métrica que trabaja sobre vectores y da una aproximación de la similitud entre ellos. Por lo tanto, si caracterizamos cada juego y lo comparamos con los demás podremos tener una medida muy acertada sobre su similaridad o no, lo que nos permite hacer muy buenas sugerencias.


## Links

**Producto**: [API MLOPs](https://pi-ml-ops-b4cf.onrender.com/docs#/).

**API Framework**: https://fastapi.tiangolo.com/.

**Deployment Service**: https://render.com/.




