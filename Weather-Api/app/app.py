from flask import Flask, jsonify
from app.config import Config
from app.weather.weather_module import WeatherModule
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded
from redis import Redis

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize the Limiter
    limiter = Limiter(
        get_remote_address,  # Use the client's IP address to limit requests
        app=app,
        default_limits=["100 per day", "10 per minute"]  # Global limit: 100 requests/day, 10 requests/minute
    )

    # Add the rate limit error handler
    @app.errorhandler(RateLimitExceeded)
    def rate_limit_handler(e):
        return jsonify(error="Too many requests. Please try again later."), 429


    # Inicializate Redis 
    redis_client = Redis(
        host='redis-10462.c339.eu-west-3-1.ec2.redns.redis-cloud.com',
        port=10462,
        password=app.config['CACHE_SECRET_KEY']
    )
    app.config['redis_client'] = redis_client  # Store redis_client in app config

    # Register the weather module
    WeatherModule.register(app)

    return app
