# Caching Proxy with CLI Project

This project implements a caching proxy server in Python. The server receives requests, forwards them to an origin server, and caches the response. For subsequent requests to the same URL, it returns the response from the cache, reducing response time and load on the origin server.

## Project Structure

- **main.py**: Main script to run the caching proxy and the command-line interface (CLI).
- **server.py**: Implementation of the proxy server using Flask.
- **cache.py**: Module for managing the cache using Redis.
- **cli.py**: Configuration of the command-line interface to start the server and clear the cache.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/icyjkk/Backend-Projects.git
   cd Caching-Proxy
   ```

2. **Install Python** (if not already installed):  

3. **Create a virtual environment and activate it**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

4. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the `.env` file with your configuration:**
   ```bash
   cp .env.example .env
   ```
   To ensure the proxy functions correctly, make sure Redis is configured. You can customize the environment variables in the `.env` file to set up the Redis connection.
   ```env
   CACHE_SECRET_KEY=your_redis_password_here
   REDIS_HOST=your_redis_host_here
   REDIS_PORT=your_redis_port_here
   ```

## Usage

### Start the Proxy Server

To start the proxy server, run the following command:

```bash
python main.py start --port <port> --origin <origin_url>
```

- `--port`: Port on which the proxy server will run.
- `--origin`: URL of the origin server to which requests will be forwarded.

**Example:**

```bash
python main.py start --port 3000 --origin http://dummyjson.com
```

### Clear the Cache

To clear the cache, you can use the following command from another terminal:

```bash
python main.py clear-cache
```

## How It Works

- Upon receiving a request, the proxy server checks if it already has the response in the cache.
  - If the response is in the cache, it returns the response directly with a `X-Cache: HIT` header.
  - If the response is not in the cache, it forwards the request to the origin server, saves the response in the cache, and returns it with a `X-Cache: MISS` header.

## Technologies Used

- **Flask**: Web framework used to build the API.
- **Redis**: Used for caching data to improve performance.
- **Requests**: Python library for making HTTP requests.
- **dotenv**: For loading environment variables from a `.env` file.
- **argparse**: Standard Python library for creating command-line interfaces.

## Contributing

Contributions are welcome! If you have suggestions or find a bug, feel free to create an issue or submit a pull request.

