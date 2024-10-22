from flask import Blueprint, request, jsonify,current_app
from app.weather.weather_service import WeatherService

weather_bp = Blueprint('weather', __name__, url_prefix='/weather')

@weather_bp.route('/current', methods=['GET'])
def get_weather():
    postal_code = request.args.get('postal_code')

    if not postal_code:
        return jsonify({"error": "Parameter is required 'postal_code'"}), 400

    weather_data = WeatherService.get_weather_data(postal_code)

    return jsonify(weather_data)


@weather_bp.route('/test', methods=['GET'])
def get_test():
    
    return "test"
