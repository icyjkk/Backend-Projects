import os
from dotenv import load_dotenv

# Upload the .env file
load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    MONGO_URI = os.getenv('MONGO_URI', 'MONGO_URI')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'JWT_SECRET_KEY')
    RATE_LIMITS = os.getenv('RATE_LIMITS', 'RATE_LIMITS')
    THROTTLING_LIMITS = os.getenv('THROTTLING_LIMITS', 'THROTTLING_LIMITS')
