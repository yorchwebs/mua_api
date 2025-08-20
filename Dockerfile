# Imagen base
FROM python:3.12.11-alpine3.22

# Establece el directorio de trabajo
WORKDIR /app

# Copia dependencias primero (para aprovechar caché)
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto (por defecto Flask/Gunicorn usa 5000/8000)
EXPOSE 8080

# Comando de arranque con Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "wsgi:app"]
