
import pandas as pd
from fastapi import FastAPI

df_reviews = pd.read_csv("df_reviews_data.csv")
df_items = pd.read_parquet("df_items_sample.parquet")
df_games = pd.read_csv("df_games_data.csv")

app = FastAPI()

#Funciones

@app.get("/PlayTimeGenre/{genre}")
async def PlayTimeGenre(genre: str):
    try:
        cadena_a_buscar = genre
        resultados = df_items[df_items['tags_and_genres'].str.contains(cadena_a_buscar, case=False, na=False)]

        if resultados.empty:
           return "Genero invalido."
        # Supongamos que tienes un DataFrame llamado df_items

        # Agrupa por la columna 'item_id' y suma la columna 'playtime_forever'
        resultados2 = resultados.groupby('item_id')['playtime_forever'].sum().reset_index()
        resultados2
        # 'resultados' ahora contiene la suma de 'playtime_forever' por 'item_id'
        
        # Suponiendo que 'resultados' es el DataFrame con la suma de 'playtime_forever' por 'item_id'
        # Y 'df_games' es el DataFrame con los datos de los juegos

        # Fusiona 'resultados' con 'df_games' usando 'item_id' como clave
        merged_df = pd.merge(resultados2, df_games[['id', 'release_date']], left_on='item_id', right_on='id', how='left')

        # Encuentra la fila con la suma máxima de 'playtime_forever'
        fila_max_playtime = merged_df[merged_df['playtime_forever'] == merged_df['playtime_forever'].max()]

        # Obtiene la fecha de lanzamiento correspondiente
        fecha_lanzamiento_max_playtime = fila_max_playtime['release_date'].values[0]

        return int(fecha_lanzamiento_max_playtime)


    except Exception as e:
        return {"message": f"Error: {str(e)}"}
    
@app.get("/UserForGenre/{genre}")
async def UserForGenre(genre : str):
    try:
        cadena_a_buscar = genre
        resultados = df_items[df_items['tags_and_genres'].str.contains(cadena_a_buscar, case=False, na=False)]
        if resultados.empty:
           return "Genero invalido."

        # Supongamos que tienes un DataFrame llamado df_items

        # Agrupa por la columna 'user_id' y suma la columna 'playtime_forever'
        resultados2 = resultados.groupby('user_id')['playtime_forever'].sum().reset_index()
        resultados2 = resultados2.sort_values(['playtime_forever'], ascending= False)
        userbuscado = resultados2.iloc[0]

        resultados3 = df_items[(df_items['user_id'] == userbuscado['user_id']) & (df_items['tags_and_genres'].str.contains(cadena_a_buscar, case=False, na=False))]

        resultados3 = resultados3.sort_values(['playtime_forever'], ascending= False)
        # 'resultados' ahora contiene la suma de 'playtime_forever' por 'item_id'
      
        resultados4 = pd.merge(resultados3, df_games[['id', 'release_date']], left_on='item_id', right_on='id', how='left')
        resultados4 = resultados4.groupby('release_date')['playtime_forever'].sum().reset_index()
        resultados4 = resultados4.sort_values(['release_date'], ascending= False)
        # Filtrar las filas donde 'playtime_forever' sea mayor que 0 y crear una lista de tuplas
        lista_anos_horas = [(f"Año: {int(ano)}", f"Horas: {int(hora)}") for ano, hora in zip(resultados4['release_date'], resultados4['playtime_forever'] / 60) if hora > 0]
        lista_anos_horas.insert(0,{"El usuario con mas horas jugados para el genero es",userbuscado['user_id']})
        # Imprimir la lista de años y horas
        return(lista_anos_horas)


    except Exception as e:
        return {"message": f"Error: {str(e)}"}
    
   

@app.get("/UsersRecommend/{year}")
async def UsersRecommend(year : int):
    try:
        year_buscado = int(year)
        recommend_year = df_reviews[df_reviews['posted'] == year_buscado]
        if recommend_year.empty:
           return "Año invalido."

        recommend_true = recommend_year[recommend_year['recommend'] & ((recommend_year['sentiment_analysis'] == 1) | (recommend_year['sentiment_analysis'] == 2))]

        top3most = recommend_true.groupby('item_id')['sentiment_analysis'].count().reset_index()
        
        top3most = pd.merge(top3most, df_games[['id', 'title']], left_on='item_id', right_on='id', how='left')

        top3m = top3most.sort_values(['sentiment_analysis'], ascending= False).head(3)

        listafuncion = [(f'Puesto {i + 1}', top3m['title'].iloc[i]) for i in range(len(top3m))]

        return(listafuncion)


    except Exception as e:
        return {"message": f"Error: {str(e)}"} 
    
@app.get("/UsersNOTRecommend/{year}")
async def UsersNOTRecommend(year : int):
    try:
        year_buscado = int(year)
        recommend_year = df_reviews[df_reviews['posted'] == year_buscado]
        if recommend_year.empty:
           return "Año invalido."
    
        recommend_false = recommend_year[(recommend_year['recommend'] == False) & (recommend_year['sentiment_analysis'] == 0)]

        top3least = recommend_false.groupby('item_id')['sentiment_analysis'].count().reset_index()

        top3least = pd.merge(top3least, df_games[['id', 'title']], left_on='item_id', right_on='id', how='left')

        top3l = top3least.sort_values(['sentiment_analysis'], ascending= False).head(3)

        listafuncion = [(f'Puesto {i + 1}', top3l['title'].iloc[i]) for i in range(len(top3l))]

        return(listafuncion)


    except Exception as e:
        return {"message": f"Error: {str(e)}"} 
    
@app.get("/SentimentAnalysis/{year}")
async def SentimentAnalysis(year : int):
    try:
        year_buscado = int(year)

        sentiment_year = df_reviews[df_reviews['posted'] == year_buscado]
        sentiment_year = sentiment_year.groupby('sentiment_analysis').size().reset_index(name='count')

        listafuncion = []
        listafuncion.insert(0,"Segun el año de lanzamiento "+ str(year_buscado))
        listafuncion.insert(1, "Análisis de Sentimiento negativos : " + str(sentiment_year['count'].iloc[0]))
        listafuncion.insert(2, "Análisis de Sentimiento neutrales : " + str(sentiment_year['count'].iloc[1]))
        listafuncion.insert(3, "Análisis de Sentimiento positivos : " + str(sentiment_year['count'].iloc[2]))
        return(listafuncion)


    except Exception as e:
        return {"message": f"Error: {str(e)}"}     
#Modelo de recomendación

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@app.get("/recomend_games/{product_id}")
async def recommend_games(product_id : int):
    try:
        # Obtén el juego de referencia
        target_game = df_games[df_games['id'] == int(product_id)]

        num_recommendations = 5

        if target_game.empty:
            return "No se encontró el juego de referencia."

        # Combina las etiquetas (tags) y géneros en una sola cadena de texto
        target_game_tags_and_genres = ' '.join(target_game['tags'].fillna('') + ' ' + target_game['genres'].fillna(''))

        # Crea un vectorizador TF-IDF y ajústalo una vez
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(df_games['tags'].fillna('') + ' ' + df_games['genres'].fillna(''))

        # Calcula la similitud entre el juego de referencia y todos los juegos
        similarity_scores = cosine_similarity(tfidf_vectorizer.transform([target_game_tags_and_genres]), tfidf_matrix)

        # Obtiene los índices de los juegos más similares
        similar_games_indices = similarity_scores[0].argsort()[::-1]

        # Recomienda los juegos más similares
        recommended_games = df_games.loc[similar_games_indices[1:num_recommendations + 1]]
        listarecommended = recommended_games['title'].tolist()
        
        # Devuelve la lista de juegos recomendados
        return listarecommended

    except Exception as e:
        return {"message": f"Error: {str(e)}"}