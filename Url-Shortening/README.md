# URL Shortening Service

This is a URL shortening service developed with Python that allows converting long URLs into short, easy-to-share codes.
![image](https://github.com/user-attachments/assets/f90b9620-5b0d-4df7-953d-5ec3770e7cce)

## 🚀 Features

- Long URL shortening
- Unique code generation 
- URL validation
- Original URL redirection
- RESTful API
---
## 🛠️ Technologies

- Python
- Flask
- MongoDB
---
## 📋 Prerequisites
- Python 3.x
- MongoDB
- pip (Python package manager)
---
## ⚙️ Installation

1. Clone repository:
```bash
git clone https://github.com/icyjkk/Backend-Projects.git
cd Url-Shortening
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure .env file:
```bash
DEBUG=True
RATE_LIMITS="5 per second; 10 per minute; 100 per hour; 1000 per day"
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/todo_db
```
---
## 🚀 Run project
```bash
py -m app.main
```

2. You can see it at `http://localhost:5000`
---
## 📌 Endpoints

### Short URL
```http
POST /url/shorten
Content-Type: application/json

{
    "url": "https://www.ejemplo-url-larga.com"
}
```
### Retrieve URL
```http
GET /url/shorten/{shortCode}
```

### Update URL
```http
PUT /url/shorten/{shortCode}
Content-Type: application/json

{
    "url": "https://www.nueva-url.com"
}
```
### Delete URL
```http
DELETE /url/shorten/{shortCode}
```
### Get Stats
```http
GET /url/shorten/{shortCode}/stats
```
---
## Contributing

Contributions are welcome! If you have suggestions or find a bug, feel free to create an issue or submit a pull request.
