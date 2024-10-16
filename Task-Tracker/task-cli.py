import argparse #Libreria propia de python para crear el cli
import json
import util
from datetime import datetime


file_name = 'tasks.json'

def add_command(args):
    # Intentar leer el archivo JSON si existe
    try:
        with open(file_name, 'r') as file:
            tasks = json.load(file)  # Cargar las tareas existentes
    except FileNotFoundError:
        tasks = []  # Si el archivo no existe, comenzar con una lista vacía

    # Aqui obtenemos el nuevo id, que sera el ultimo + 1
    new_id = util.obtain_next_id(tasks)

    # Crear una nueva tarea con los campos necesarios
    new_task = {
        "id": new_id,  # ID único que incrementa
        "description": args.task,  # La descripción proporcionada por el usuario
        "status": "todo",  # Estado inicial de la tarea
        "createdAt": datetime.now().isoformat(),  # Fecha y hora de creación (llamada correcta)
        "updatedAt": datetime.now().isoformat()   # Fecha y hora de última actualización (llamada correcta)
    }

    # Agregar la nueva tarea
    tasks.append(new_task)

    # Escribir las tareas de vuelta en el archivo JSON
    with open(file_name, 'w') as file:
        json.dump(tasks, file, indent=4)

    print(f"Task added successfully (ID: {new_id})")

def main():
    # Crear el parser principal
    parser = argparse.ArgumentParser(description="Task tracket cli")

    # Crea un conjunto de subcomandos. Cada subcomando tendrá su propio parser y podrá tener sus propios argumentos.
    subparsers = parser.add_subparsers(title='Comandos', description='Comandos disponibles', dest='comando')

    # Se usa para definir un nuevo comando.
    parser_add = subparsers.add_parser('add', help='Add a task')
    parser_add.add_argument('task description', type=str, help='Task Description')
    
    #Establece una función predeterminada que se ejecutará cuando se invoque ese comando.
    parser_add.set_defaults(func=add_command)

    # Parsear los argumentos
    args = parser.parse_args()

    # Después de que argparse analice los argumentos, ejecutamos la función asignada al comando seleccionado.
    if args.comando:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
