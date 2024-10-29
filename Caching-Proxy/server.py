from flask import Flask, request, Response
import requests
import threading
import signal
import cache

app = Flask(__name__)

def start_proxy(port, origin):
    app.config['ORIGIN'] = origin
    print(f"Servidor proxy iniciado en el puerto {port}, reenviando a {origin}")
    app.run(host='0.0.0.0', port=port)

@app.route('/<path:url>', methods=['GET'])
def proxy(url):
    origin_url = f"{app.config['ORIGIN']}/{url}"
    key = cache.generate_cache_key(request.method, origin_url, request.query_string)

    # Intenta obtener la respuesta de la caché de Redis
    cached_response = cache.get_cache(key)
    if cached_response:
        print(f"Caché HIT para {key}")
        return Response(cached_response['content'], headers={"X-Cache": "HIT", **cached_response['headers']})

    # Si no está en caché, realiza la solicitud al servidor de origen
    print(f"Caché MISS para {key}")
    resp = requests.get(origin_url, params=request.args)

    # Guarda la respuesta en Redis 
    response_data = {
        'content': resp.content.decode(),  # Guarda el contenido como texto
        'headers': {'Content-Type': resp.headers.get('Content-Type', 'text/plain')}
    }
    cache.set_cache(key, response_data)

    # Devuelve la respuesta con el encabezado "X-Cache: MISS"
    return Response(resp.content, headers={"X-Cache": "MISS", "Content-Type": resp.headers.get('Content-Type', 'text/plain')})
