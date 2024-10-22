from app.weather.weather_controller import weather_bp

class WeatherModule:
    
    @staticmethod
    def register(app):
        app.register_blueprint(weather_bp)
