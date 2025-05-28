# Usa una imagen oficial de Python
FROM python:3.11-slim

# Crea y usa un directorio de trabajo
WORKDIR /app

# Copia tus archivos al contenedor
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expón el puerto (Fly usará este)
EXPOSE 8080

# Comando para ejecutar con gunicorn
CMD ["gunicorn", "bot:app", "-b", "0.0.0.0:8080"]
