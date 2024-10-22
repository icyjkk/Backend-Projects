import os
from dotenv import load_dotenv

# Upload the .env file
load_dotenv()

class Config:
    # WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'WEATHER_API_KEY')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    # CACHE_SECRET_KEY = os.getenv('CACHE_SECRET_KEY', 'CACHE_SECRET_KEY')
