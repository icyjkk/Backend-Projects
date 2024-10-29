import argparse
from server import start_proxy
from cache import clear_cache

def main():
    # Crear el parser principal
    parser = argparse.ArgumentParser(description="Servidor proxy con caché.")
    
    # Crea un conjunto de subcomandos
    subparsers = parser.add_subparsers(title='Comandos', description='Comandos disponibles', dest='command')
    
    # Comando para iniciar el servidor
    parser_start = subparsers.add_parser('start', help='Iniciar el servidor de caché proxy')
    parser_start.add_argument('--port', type=int, default=3000, help='Puerto en el que se ejecutará el servidor proxy.')
    parser_start.add_argument('--origin', help='URL del servidor de origen.', required=True)


    # Comando para limpiar la caché
    parser_clear = subparsers.add_parser('clear-cache', help='Limpiar la caché del proxy')

    args = parser.parse_args()
    
    if args.command == 'start':
        start_proxy(args.port, args.origin)
    elif args.command == 'clear-cache':
        clear_cache()
    else:
        parser.print_help()
