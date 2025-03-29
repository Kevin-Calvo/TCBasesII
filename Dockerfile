# Usa Python como base
FROM python:3.13.2

# Define el directorio de trabajo dentro del contenedor
WORKDIR /backend

# Copia todos los archivos del proyecto dentro del contenedor
COPY backend/ /backend/

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

# Expone el puerto donde correrá la API
EXPOSE 8080

# Comando para ejecutar el servidor
CMD ["python", "main.py"]
