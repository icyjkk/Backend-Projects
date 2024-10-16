import json

def obtain_next_id(tasks):
    
    if not tasks:
        return 1  # Si no hay tareas, empezar desde 1
    else:
        # Obtener el ID máximo actual y sumar 1
        max_id = max(task['id'] for task in tasks)
        return max_id + 1

def search_task(id,tasks):
    # Buscar la tarea con el id proporcionado
    task_to_update = None

    for task in tasks:
        if task['id'] == id:
            task_to_update = task
            break

    return task_to_update

def load_tasks(show_message=True):
    try:
        with open("tasks.json", 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        if show_message:
            print("No tasks found. Please add a task first.")
        return []

def save_tasks(tasks):
    with open("tasks.json", 'w') as file:
        json.dump(tasks, file, indent=4)
