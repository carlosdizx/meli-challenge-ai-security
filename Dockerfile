# Usamos una imagen base de Python
FROM python:3.11-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias (requirements.txt) para instalar las dependencias
COPY requirements.txt .

# Instalamos las dependencias desde requirements.txt sin usar caché
RUN pip install --no-cache-dir -r requirements.txt

# Instalamos supervisord para gestionar múltiples procesos dentro del contenedor
RUN apt-get update && apt-get install -y supervisor curl && rm -rf /var/lib/apt/lists/*

# Copiamos t0d0 el código de la aplicación al contenedor
COPY . .

# Exponemos los puertos necesarios
EXPOSE 8501 4200

# Copiamos el archivo de configuración de supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Comando para ejecutar el supervisord (gestiona ambos procesos)
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
