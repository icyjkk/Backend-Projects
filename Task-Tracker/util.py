

def obtain_next_id(tasks):
    
    if not tasks:
        return 1  # Si no hay tareas, empezar desde 1
    else:
        # Obtener el ID máximo actual y sumar 1
        max_id = max(task['id'] for task in tasks)
        return max_id + 1
