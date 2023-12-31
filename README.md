<<<<<<< HEAD
=======

>>>>>>> caf92fc0ec8fb35652fd4e22ef2d94a350ce182e
# Sistema de Recomendación de Videojuegos en Steam

Este proyecto es un Sistema de Recomendación de Videojuegos en Steam que utiliza análisis de sentimiento de reseñas de usuarios y datos de juegos para proporcionar recomendaciones personalizadas.

<<<<<<< HEAD
=======

>>>>>>> caf92fc0ec8fb35652fd4e22ef2d94a350ce182e
## Introducción

Este proyecto tiene como objetivo proporcionar recomendaciones de videojuegos personalizadas a los usuarios de la plataforma Steam utilizando análisis de sentimiento de reseñas de juegos y datos de juegos disponibles públicamente.

## Requisitos

- Python 3.8 o superior
- Bibliotecas Python (ver archivo requirements.txt para la lista completa de dependencias)
- Cuenta en Railway (para el despliegue en línea)

## Instalación

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/tu-usuario/sistema-recomendacion-steam.git
   ```

2. Navega al directorio del proyecto:

   ```bash
   cd sistema-recomendacion-steam
   ```

3. Instala las dependencias del proyecto:

   ```bash
   pip install -r requirements.txt
   ```

## Ejecución Local

Para ejecutar la aplicación localmente, utiliza el siguiente comando:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

La API estará disponible en http://localhost:8000.

## Despliegue en Railway

Este proyecto se encuentra desplegado en Railway. Puedes acceder a la API en [este enlace](URL_DE_TU_API_EN_RAILWAY).

## Uso

Para obtener recomendaciones de videojuegos, puedes hacer consultas a los endpoints proporcionados por la API. Aquí hay algunos ejemplos:

- Obtener información de usuario: `/userdata/{user_id}`
- Obtener recuento de reseñas entre fechas: `/countreviews/{start_date}/{end_date}`
- Obtener el ranking de géneros: `/genre/{genre}`
- Obtener los mejores usuarios por género: `/userforgenre/{genre}`
- Obtener estadísticas por desarrollador: `/developer/{developer}`
- Obtener análisis de sentimiento por año: `/sentiment_analysis/{year}`


## Contribución

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Realiza un fork del repositorio.
2. Crea una rama para tu contribución: `git checkout -b mi-contribucion`.
3. Realiza tus cambios y commits: `git commit -m "Añadir nueva funcionalidad"`.
4. Envía una solicitud de extracción (pull request) a la rama principal del proyecto.


## Contacto

Si tienes preguntas o sugerencias, no dudes en ponerte en contacto con el equipo de desarrollo:

<<<<<<< HEAD
- [LinkedIn](https://www.linkedin.com/in/carolina-zamora-61494656/)

=======

https://www.linkedin.com/in/carolina-zamora-61494656/

>>>>>>> caf92fc0ec8fb35652fd4e22ef2d94a350ce182e
