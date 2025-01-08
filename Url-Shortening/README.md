# URL Shortening Service

This is a URL shortening service developed with Python that allows converting long URLs into short, easy-to-share codes.

## 🚀 Features

- Long URL shortening
- Unique code generation 
- URL validation
- Original URL redirection
- RESTful API

## 🛠️ Technologies

- Python
- Flask
- MongoDB

## 📋 Prerequisites

- Python 3.x
- MongoDB
- pip (Python package manager)

## ⚙️ Installation

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/url-shortening.git
cd url-shortening
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita el archivo .env con tus configuraciones
```

## 🚀 Uso

1. Inicia el servidor:
```bash
python run.py
```

2. La API estará disponible en `http://localhost:5000`

## 📌 Endpoints

### Acortar URL
```http
POST /api/v1/urls
Content-Type: application/json

{
    "url": "https://www.ejemplo-url-larga.com"
}
```

### Obtener URL Original
```http
GET /api/v1/urls/{shortCode}
```

### Actualizar URL
```http
PUT /api/v1/urls/{shortCode}
Content-Type: application/json

{
    "url": "https://www.nueva-url.com"
}
```


```
