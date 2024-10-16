import argparse #Libreria propia de python para crear el cli
import json
import util
from datetime import datetime

file_name = 'tasks.json'

def add_command(args):
    tasks = util.load_tasks(show_message=False)
    new_id = util.obtain_next_id(tasks) # Aqui obtenemos el nuevo id, que sera el ultimo + 1
    new_task = {
        "id": new_id,  # ID único que incrementa
        "description": args.task,  # La descripción proporcionada por el usuario
        "status": "todo",  # Estado inicial de la tarea
        "createdAt": datetime.now().isoformat(),  # Fecha y hora de creación (llamada correcta)
        "updatedAt": datetime.now().isoformat()   # Fecha y hora de última actualización (llamada correcta)
    }
    tasks.append(new_task) # Agregar la nueva tarea.
    util.save_tasks(tasks) #Guardar la nueva tarea.
    print(f"Task added successfully (ID: {new_id})")

def update_command(args):
    tasks = util.load_tasks(show_message=True)
    if not tasks:
        return
    
    task_to_update=util.search_task(args.id, tasks)

    if task_to_update:
        
        task_to_update['description'] = args.description
        task_to_update['updatedAt'] = datetime.now().isoformat()
        util.save_tasks(tasks)

        print(f"Task ID {args.id} updated successfully.")
    else:
        print(f"Task with ID {args.id} not found.")

def delete_command(args):
    tasks = util.load_tasks(show_message=True)
    if not tasks:
        return
    
    task_to_delete = util.search_task(args.id, tasks)

    if task_to_delete:
        
        tasks.remove(task_to_delete)

        util.save_tasks(tasks)

        print(f"Task ID {args.id} deleted successfully.")
    else:
        print(f"Task with ID {args.id} not found.")

def mark_status_command(args):
    tasks = util.load_tasks(show_message=True)
    if not tasks:
        return
    
    task_to_update = util.search_task(args.id, tasks)

    if task_to_update:
    
        task_to_update['status'] = args.status
        task_to_update['updatedAt'] = datetime.now().isoformat()

        util.save_tasks(tasks)

        print(f"Task ID {args.id} marked as '{args.status}'.")
    else:
        print(f"Task with ID {args.id} not found.")


def main():
# Crear el parser principal
    parser = argparse.ArgumentParser(description="Task tracker CLI")

    # Crea un conjunto de subcomandos
    subparsers = parser.add_subparsers(title='Comandos', description='Comandos disponibles', dest='comando')

    # Comando add
    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_add.add_argument('task', type=str, help='Task description')
    parser_add.set_defaults(func=add_command)

    # Comando update
    parser_update = subparsers.add_parser('update', help='Update a task')
    parser_update.add_argument('id', type=int, help='Task ID')
    parser_update.add_argument('description', type=str, help='New task description')
    parser_update.set_defaults(func=update_command)

    # Comando delete
    parser_delete = subparsers.add_parser('delete', help='Delete a task')
    parser_delete.add_argument('id', type=int, help='Task ID')
    parser_delete.set_defaults(func=delete_command)

    # Comando mark-in-progress
    parser_mark_in_progress = subparsers.add_parser('mark-in-progress', help='Mark a task as in-progress')
    parser_mark_in_progress.add_argument('id', type=int, help='Task ID')
    parser_mark_in_progress.set_defaults(func=mark_status_command, status='in-progress')

    # Comando mark-done
    parser_mark_done = subparsers.add_parser('mark-done', help='Mark a task as done')
    parser_mark_done.add_argument('id', type=int, help='Task ID')
    parser_mark_done.set_defaults(func=mark_status_command, status='done')

    # Parsear los argumentos
    args = parser.parse_args()

    # Ejecutar la función correspondiente al comando
    if args.comando:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
