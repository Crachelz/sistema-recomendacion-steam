# Usar una imagen base de Python
FROM python:3.8-slim-buster

# Establecer el directorio de trabajo en /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

# Actualizar e instalar libpq-dev
RUN apt-get update && apt-get install -y libpq-dev

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt requirements.txt

# Copiar todo el contenido del directorio actual al contenedor en /app
COPY . .

# Comando para ejecutar la aplicación (ajústalo según tu estructura de directorios)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
