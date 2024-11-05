import os
from dotenv import load_dotenv

# Upload the .env file
load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    RATE_LIMITS = os.getenv('RATE_LIMITS', 'RATE_LIMITS').split(";")
