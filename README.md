# PIMLopsSTEAM
Proyecto Individual MLops SoyHenry

Machine Learning Operations (MLOps)

ETL y EDA

El proyecto consiste en hacer un Data Engineering con los tres datasets provistos para el trabajo. Los mismos representan una dataset de usuarios y sus items, un dataset de reviews por usuarios y un dataset de juegos.
Ante estos datos deberemos hacer un ETL, extraer los datos que no seran valiosos. Transformar aquellos que no podemos utilizar como estan provistos y cargarlos en nuevos archivos para optimizar el codigo.

Una vez limpio y ordenado nuestros tres datasets podemos continuar haciendo un EDA, exploratory data analysis para dar luz sobre las tendencias de los usuarios y los juegos. No obstante se obtiene gran informacion en el proceso de ETL sobre las estructuras y tendencias con las que estamos trabajando.

Feature Engineering 
 
 Realizaremos sobre el dataset de reviews ya optimizado un analisis de sentimiento para poder complejizar la relacion de los usuarios con los juegos mas y menos recomendados. Este sentiment analysis lo realizamos con la libreria TextBlob sobre el review de cada usuario registrado, generando 0 ante una critica negativa, 1 ante una neutral y finalmente 2 ante una positiva. Ante la imposibilidad de generar un analisis se da 1 por default

Desarrollo de API

Se nos propone realizar una API utilizando el framework FastAPI que pueda ser consumida por RENDER, se debe proveer cinco funciones para los endpoints y una sexta que sera el machine learning que consumira la API : 

+ def **PlayTimeGenre( *`genre` : str* )**:
    Debe devolver `año` con mas horas jugadas para dicho género.
  

+ def **UserForGenre( *`genre` : str* )**:
    Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.

+ def **UsersRecommend( *`year` : int* )**:
   Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. 

+ def **UsersNotRecommend( *`year` : int* )**:
   Devuelve el top 3 de juegos MENOS recomendados por usuarios para el año dado. 

+ def **sentiment_analysis( *`year` : int* )**:
    Según el año de lanzamiento, se devuelve una lista con la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento. 

Modelo de aprendizaje automático:

El proyecto nos indica proporcionar un modelo de recomendacion de aprendizaje automatico basado en el juego pasado por parametro por el cliente. Este deberá tener una relación ítem-ítem, se toma el item pasado por product_id el mismo contiene tags y genres en el dataset que se utilizaran para poder recomendar al usuario otros 5 juegos con caracteristicas similares y asi proporcionar una recomendacion acorde.
Usamos en esta oportunidad la libreria Scikit-learn y usamos el modelo de similaridad del coseno.

Links

Repositorio (Github): https://github.dev/MDPizzio/PIMLopsSTEAM/
Deploy del Proyecto (Render): https://pisteamdataset.onrender.com/docs
Video (Youtube): subir