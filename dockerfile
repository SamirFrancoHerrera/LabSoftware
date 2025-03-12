# Dockerfile
FROM python:3.11

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y postgresql-client

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]