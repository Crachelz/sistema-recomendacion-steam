# %%
import pandas as pd
from fastapi import FastAPI
from datetime import datetime
from collections import defaultdict  

app = FastAPI()


# %%
df_reseñas = pd.read_parquet('dataframe_resenias_usuarios.parquet')
df_juegos = pd.read_parquet('caracteristicas_juegos.parquet')

# %%
# crear los endpoints para las diferentes funciones que vamos a implementar en la API.
# Endpoint 1: userdata(User_id)
# def userdata( User_id : str ): Debe devolver cantidad de dinero gastado por el usuario,
# el porcentaje de recomendación en base a reviews.recommend y cantidad de items.


# Función para calcular el gasto del usuario
def calcular_gasto(user_id):
    # Filtra las reseñas del usuario en df_reseñas
    reseñas_usuario = df_reseñas[df_reseñas['user_id'] == user_id]
    
    # Obtiene los IDs de los juegos que ha revisado el usuario
    ids_juegos_reseñados = [item['item_id'] for reseña in reseñas_usuario['reviews'] for item in reseña]
    
    # Filtra los juegos que ha revisado el usuario en df_juegos
    juegos_reseñados = df_juegos[df_juegos['app_name'].isin(ids_juegos_reseñados)]
    
    # Calcula el gasto sumando los precios de los juegos revisados
    gasto = juegos_reseñados['price'].sum()
    
    return gasto

# Función para calcular el porcentaje de recomendación
def calcular_porcentaje_recomendación(user_id):
    # Filtra las reseñas del usuario en df_reseñas
    reseñas_usuario = df_reseñas[df_reseñas['user_id'] == user_id]
    
    # Obtiene el promedio de las recomendaciones en las reseñas del usuario
    promedio_recomendaciones = reseñas_usuario['sentiment_analysis'].mean()
    
    return promedio_recomendaciones

# Función para obtener la cantidad de items del usuario
def obtener_cantidad_items(user_id):
    # Filtra las reseñas del usuario en df_reseñas
    reseñas_usuario = df_reseñas[df_reseñas['user_id'] == user_id]
    
    # Obtiene la cantidad total de items revisados por el usuario
    cantidad_items = reseñas_usuario['items_count'].sum()
    
    return cantidad_items

# Ruta para la función userdata(User_id)
@app.get("/userdata/{user_id}")
async def userdata(user_id: str):
    gasto = calcular_gasto(user_id)
    porcentaje_recomendación = calcular_porcentaje_recomendación(user_id)
    cantidad_items = obtener_cantidad_items(user_id)
    
    return {
        "User_id": user_id,
        "Gasto": gasto,
        "Porcentaje_Recomendación": porcentaje_recomendación,
        "Cantidad_Items": cantidad_items
    }



# %%
# Endpoint 2: countreviews(YYYY-MM-DD y YYYY-MM-DD)
@app.get("/countreviews/{start_date}/{end_date}")
async def countreviews(start_date: str, end_date: str):
    try:
        # Convertir las fechas de inicio y fin a objetos datetime
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Filtrar las reseñas dentro del rango de fechas
        filtered_reviews = df_reseñas[(df_reseñas['release_date'] >= start_date) & (df_reseñas['release_date'] <= end_date)]

        # Contar la cantidad de usuarios únicos que realizaron reseñas
        unique_users = filtered_reviews['user_id'].nunique()

        # Calcular el porcentaje de recomendación en base a reviews.recommend
        total_reviews = len(filtered_reviews)
        if total_reviews > 0:
            recommended_reviews = filtered_reviews['recommend'].sum()
            recommendation_percentage = (recommended_reviews / total_reviews) * 100
        else:
            recommendation_percentage = 0.0

        return {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "unique_users": unique_users,
            "recommendation_percentage": recommendation_percentage
        }
    except Exception as e:
        return {"error": "Ocurrió un error al procesar la solicitud.", "details": str(e)}


# %%
# Endpoint 3: genre(género)
#def genre( género : str ): 
# Devuelve el puesto en el que se encuentra un género sobre el ranking de los mismos analizado bajo la columna PlayTimeForever.
@app.get("/genre/{genero}")
def genre(genero: str):
    # Encontrar el índice (puesto) del género especificado en el ranking
    df_filtered = df_juegos[df_juegos['genres'].str.contains(genero, case=False)]
    df_filtered.sort_values(by='PlayTimeForever', ascending=False, inplace=True)
    
    puesto = df_filtered.index[0] + 1
    
    return {"genero": genero, "puesto": puesto}

# %%
# Endpoint 4: userforgenre(género)
# def userforgenre( género : str ): Top 5 de usuarios con más horas de juego en el género dado, con su URL (del user) y user_id.

@app.get("/userforgenre/{genero}")
def userforgenre(genero: str):
    # Filtrar las reseñas por género
    df_filtered = df_reseñas[df_reseñas['review_text'].str.contains(genero, case=False)]
    
    # Agrupar por usuario y calcular las horas totales de juego
    user_genre_hours = df_filtered.groupby('user_id')['PlayTimeForever'].sum().reset_index()
    
    # Ordenar en orden descendente
    user_genre_hours.sort_values(by='PlayTimeForever', ascending=False, inplace=True)
    
    # Tomar los primeros 5 usuarios
    top_users = user_genre_hours.head(5)
    
    # Crear una lista de resultados
    results = []
    
    # Recorrer los usuarios y obtener sus URLs
    for index, row in top_users.iterrows():
        user_id = row['user_id']
        user_url = df_reseñas[df_reseñas['user_id'] == user_id]['user_url'].iloc[0]
        results.append({"user_id": user_id, "user_url": user_url, "PlayTimeForever": row['PlayTimeForever']})
    
    return {"genero": genero, "top_users": results}

# Ejemplo de uso: http://localhost:8000/userforgenre/Action

# %%
# Endpoint 5: developer(desarrollador)
# def developer( desarrollador : str ): Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora. Ejemplo de salida:

"""Activision	
Año	Contenido Free
2023	27%
2022	25%
xxxx	xx%"""


# Definir la ruta para la función developer
@app.get("/developer/{desarrollador}")
def developer(desarrollador: str):
    # Filtrar juegos por desarrollador
    df_filtered = df_juegos[df_juegos['developer'] == desarrollador]
    
    # Verificar si se encontraron juegos del desarrollador
    if df_filtered.empty:
        return {"mensaje": "No se encontraron juegos para el desarrollador proporcionado."}
    
    # Crear un DataFrame para el cálculo de contenido gratuito
    df_free_content = df_filtered[['release_date', 'price', 'early_access']]
    
    # Convertir 'release_date' a tipo de dato datetime
    df_free_content['release_date'] = pd.to_datetime(df_free_content['release_date'])
    
    # Extraer el año de la fecha de lanzamiento
    df_free_content['year'] = df_free_content['release_date'].dt.year
    
    # Calcular el número total de juegos por año
    games_per_year = df_free_content['year'].value_counts().reset_index()
    games_per_year.columns = ['Año', 'Cantidad de juegos']
    
    # Calcular el número de juegos gratuitos por año
    free_games_per_year = df_free_content[df_free_content['price'] == 0]['year'].value_counts().reset_index()
    free_games_per_year.columns = ['Año', 'Cantidad de juegos gratuitos']
    
    # Fusionar los DataFrames para calcular el porcentaje de contenido gratuito
    merged_df = pd.merge(games_per_year, free_games_per_year, on='Año', how='left')
    
    # Llenar NaN con 0 en caso de que no haya juegos gratuitos en cierto año
    merged_df['Cantidad de juegos gratuitos'].fillna(0, inplace=True)
    
    # Calcular el porcentaje de contenido gratuito
    merged_df['Porcentaje de contenido gratuito'] = (merged_df['Cantidad de juegos gratuitos'] / merged_df['Cantidad de juegos']) * 100
    
    # Formatear el porcentaje como cadena
    merged_df['Porcentaje de contenido gratuito'] = merged_df['Porcentaje de contenido gratuito'].map('{:.2f}%'.format)
    
    return {"desarrollador": desarrollador, "informacion_por_anio": merged_df.to_dict(orient='records')}

# Ejemplo de uso: http://localhost:8000/developer/Activision



# %%
# Endpoint 6: sentiment_analysis(año)
# def sentiment_analysis( año : int ): Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se 
# encuentren categorizados con un análisis de sentimiento.

    #Ejemplo de retorno: {Negative = 182, Neutral = 120, Positive = 278}#
    
@app.get("/sentiment_analysis/{año}")
def sentiment_analysis(año: int):
    # Filtrar reseñas por el año de lanzamiento
    df_filtered = df_reseñas[df_reseñas['release_date'].dt.year == año]
    
    # Verificar si se encontraron reseñas para el año proporcionado
    if df_filtered.empty:
        return {"mensaje": f"No se encontraron reseñas para el año {año}."}
    
    # Inicializar un diccionario para contar las categorías de sentimiento
    sentiment_counts = defaultdict(int)
    
    # Contar las categorías de sentimiento
    for sentiment in df_filtered['sentiment_analysis']:
        if sentiment == 0:
            sentiment_counts['Negative'] += 1
        elif sentiment == 1:
            sentiment_counts['Neutral'] += 1
        elif sentiment == 2:
            sentiment_counts['Positive'] += 1
    
    return {"Sentimiento por año": sentiment_counts}


# %%
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)



