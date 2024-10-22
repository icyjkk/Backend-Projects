from flask import Flask, jsonify
from app.config import Config
from app.weather.weather_module import WeatherModule
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.errors import RateLimitExceeded

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

    # Register the weather module
    WeatherModule.register(app)

    return app
