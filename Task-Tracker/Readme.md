Aquí tienes el contenido del **README.md** completo, listo para que lo copies directamente:

```markdown
# Task Tracker CLI

A simple command-line interface (CLI) for managing tasks. With this tool, you can add, update, delete, list, and mark tasks with different statuses (`todo`, `in-progress`, and `done`).

## Features

- **Add tasks**: Add a new task with a description.
- **Update tasks**: Update the description of an existing task.
- **Delete tasks**: Remove tasks from the list.
- **List tasks**: List all tasks or filter by status.
- **Mark tasks**: Mark tasks as `in-progress` or `done`.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/task-tracker-cli.git
    cd task-tracker-cli
    ```

2. **Install Python dependencies** (if you have any external ones, otherwise skip this step):

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the CLI**:

    You can run the `task-cli.py` script directly from your terminal.

    ```bash
    python task-cli.py --help
    ```

## Usage

### 1. Adding a Task

To add a new task:

```bash
python task-cli.py add "Buy groceries"
```

Output:

```
Task added successfully (ID: 1)
```

### 2. Updating a Task

To update the description of an existing task:

```bash
python task-cli.py update 1 "Buy groceries and milk"
```

Output:

```
Task ID 1 updated successfully.
```

### 3. Deleting a Task

To delete a task by its ID:

```bash
python task-cli.py delete 1
```

Output:

```
Task ID 1 deleted successfully.
```

### 4. Listing Tasks

- **List all tasks**:

    ```bash
    python task-cli.py list
    ```

    Output:

    ```
    Listing all tasks:
    ID: 1 - Description: Buy groceries - Status: todo
    ID: 2 - Description: Clean the house - Status: in-progress
    ```

- **List tasks by status**:

    You can filter tasks by their status (`done`, `todo`, `in-progress`):

    ```bash
    python task-cli.py list todo
    ```

    Output:

    ```
    Listing tasks with status 'todo':
    ID: 1 - Description: Buy groceries - Status: todo
    ```

### 5. Marking Tasks as `in-progress` or `done`

- **Mark a task as `in-progress`**:

    ```bash
    python task-cli.py mark-in-progress 1
    ```

    Output:

    ```
    Task ID 1 marked as 'in-progress'.
    ```

- **Mark a task as `done`**:

    ```bash
    python task-cli.py mark-done 1
    ```

    Output:

    ```
    Task ID 1 marked as 'done'.
    ```

## Command Reference

| Command                     | Description                                                |
|------------------------------|------------------------------------------------------------|
| `add "task description"`      | Add a new task with the specified description.             |
| `update <id> "new description"` | Update the task with the given ID.                        |
| `delete <id>`                | Delete the task with the given ID.                         |
| `list [status]`              | List all tasks or filter by status (`done`, `todo`, `in-progress`). |
| `mark-in-progress <id>`      | Mark the task with the given ID as `in-progress`.          |
| `mark-done <id>`             | Mark the task with the given ID as `done`.                 |

## Future Improvements

- Add due dates to tasks.
- Allow prioritization of tasks.
- Add categories or tags to organize tasks.
- Add support for recurring tasks.

## Contributing

If you'd like to contribute to this project, feel free to submit pull requests or open issues with ideas, bug reports, or feature requests.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -m 'Add some new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Open a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### Instrucciones:
- Copia este contenido y pégalo en un archivo llamado **`README.md`** en el repositorio de tu proyecto en GitHub.
- Si no tienes dependencias externas (no usas ningún paquete externo), puedes omitir la sección de "Install Python dependencies".

Este README contiene todos los comandos y ejemplos de uso del CLI de tareas que has implementado.
