from redis import Redis
import os
from dotenv import load_dotenv
import hashlib
import json

# Cargar las variables de entorno del archivo .env
load_dotenv()

# Inicializar Redis usando las variables de entorno
redis_client = Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    password=os.getenv('CACHE_SECRET_KEY')
)

def generate_cache_key(method, url, query_string):
    """Genera una clave hash única basada en el método, URL y parámetros de consulta."""
    key = f"{method} {url}?{query_string.decode()}"
    return hashlib.sha256(key.encode()).hexdigest()

def get_cache(key):
    """Obtiene la respuesta en caché de Redis si existe."""
    data = redis_client.get(key)
    return json.loads(data) if data else None

def set_cache(key, response_data, expiration=86400):  # 24 horas
    """Guarda la respuesta en Redis con una expiración de 24 horas por defecto."""
    redis_client.setex(key, expiration, json.dumps(response_data))

def clear_cache():
    """Limpia todos los datos almacenados en la caché de Redis."""
    redis_client.flushdb()
    print("Caché en Redis limpiada")
