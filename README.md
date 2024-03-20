# PROYECTO INDIVIDUAL N° 1

## Machine Learning Operations

* **Alumno**: Javier Bengolea.
* **Carrera**: Data Science.
* **Cohorte**: Data PT 07.

## Descripción del Proyecto

Se nos da el acceso a 3 Datasets de la Empresa Steam (https://store.steampowered.com/?l=spanish) con información de Productos (Juegos de video), las reseñas de Usuarios y estadísticas de juego.

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

* GET /PlayTimeGenre/{genero}
* GET /UserForGenre/{genero}
* GET /UserRecommend/{anio}
* GET /UsersWorstDeveloper/{anio}
* GET /SentimentAnalysis/{developer}
* GET /recommend/{id_juego}



