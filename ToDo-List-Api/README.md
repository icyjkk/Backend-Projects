# To-Do List API

This project is a Flask-based to-do list API that allows users to authenticate, create, read, update, and delete tasks. It includes JWT authentication and features like pagination.

![alt text](image.png)

## Features

- User authentication with JWT.
- CRUD operations for tasks.
- **Pagination** for easy task management.
- Error handling for invalid requests and access permissions.

## Project Structure

```
.
├── app/
│   ├── user/                          # User-related functionality
│   │   ├── user_service.py            # Business logic for user operations (e.g., authentication)
│   │   ├── user_module.py             
│   │   └── user_controller.py         # Routes and endpoints for user-related actions
│   ├── task/                          # Task-related functionality
│   │   ├── task_service.py            # Business logic for task operations (e.g., CRUD)
│   │   ├── task_module.py             
│   │   └── task_controller.py         # Routes and endpoints for task-related actions
│   ├── schemas/                       # Schema definitions for data validation
│   │   └── schema.py                  # Schema classes for request data validation (Marshmallow)
│   ├── decorators/                    # Custom decorators for route protection and validation
│   │   └── decorators.py              # Decorators for token authentication, etc.
│   ├── util/                          # Utility functions and helpers
│   │   └── util.py                    # Utility functions for response formatting, etc.
│   ├── app.py                         # Flask application initialization and setup
│   ├── config.py                      # Configuration settings (e.g., database URIs, API keys)
│   └── main.py                        # Main script to run the application
├── .env.example                       # Example environment variable file for sensitive data (e.g., keys)
├── README.md                          
└── requirements.txt                   # Python dependencies
        

```

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/icyjkk/Backend-Projects.git
   cd todo-list-api
   ```

3. **Install Python** (if not already installed):  

4. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

5. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Configure the `.env` file:**
   ```bash
   cp .env.example .env
   ```
   Inside `.env`, set up your API keys and environment variables:
   ```env
    DEBUG=True
    MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/todo_db
    JWT_SECRET_KEY=your_jwt_secret_key
    RATE_LIMITS="5 per second; 10 per minute; 100 per hour; 1000 per day"
   ```

7. **Ensure MongoDB is running** (or your MongoDB Atlas URI is correctly set up).

8. **Run the application:**
   ```bash
   py -m app.main 
   ```

## API Endpoints

### Auth Endpoints
| Method | Endpoint         | Description                                             |
|--------|------------------|---------------------------------------------------------|
| POST   | `/user/register` | Register a new user and return a JWT                    |
| POST   | `/user/login`    | Authenticate a user and return a JWT                    |

### Task Endpoints
| Method | Endpoint                    | Description                                       |
|--------|-----------------------------|---------------------------------------------------|
| POST   | `/task/todos`               | Create a new task                                 |
| GET    | `/task/todos`               | List tasks with pagination options                |
| PUT    | `/task/todos/<task_id>`     | Update a specific task                            |
| DELETE | `/task/todos/<task_id>`     | Delete a specific task                            |

### Example Requests
#### Register
```json
POST /user/register
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword"
}
```

#### Login
```json
POST /user/login
{
  "email": "john@example.com",
  "password": "securepassword"
}
```

#### Create Task
```json
POST /task/todos
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

## Error Handling

The API returns errors in the following JSON format:
```json
{
  "status": "error",
  "message": "Description of the error",
  "errors": {
    "field": "Details about the error"
  }
}
```

Common status codes:
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Technologies Used

- **Flask**: Web framework for handling routes and requests.
- **MongoDB**: Database to store users and tasks.
- **JWT**: Tokens for secure authentication.
- **Marshmallow**: Data validation.
- **dotenv**: Loading environment variables from `.env`.

## Contributing

Contributions are welcome! If you have suggestions or find a bug, feel free to create an issue or submit a pull request.
