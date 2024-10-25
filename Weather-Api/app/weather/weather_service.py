import requests
from flask import current_app
import json

class WeatherService:

    @staticmethod
    def get_weather_data(postal_code):
        
        redis_client = current_app.config['redis_client']

        # Check if the postal code is in the cache
        print(f"Checking cache for postal code: {postal_code}")
        cached_data = redis_client.get(postal_code)
        
        if cached_data:
            # If the data is in the cache, return it from there
            print("Data found in cache.")
            return json.loads(cached_data)
        else:
            # If the data is not in the cache, make a request to the external API
            print("Data not found in cache, making request to external API...")
            weather_data = WeatherService.request_data_to_API(postal_code)
            
            # If the response is valid, store it in the cache for 12 hours (43200 seconds)
            if "error" not in weather_data:
                print("Storing data in cache for 12 hours.")
                redis_client.setex(postal_code, 43200, json.dumps(weather_data))  # 12 hours = 43200 seconds

            return weather_data
        

    @staticmethod
    def request_data_to_API(postal_code):
        api_key = current_app.config['WEATHER_API_KEY']

        if not api_key or api_key == 'WEATHER_API_KEY':
            print("Invalid API key.")
            return {"error": "Invalid API key. Please check the configuration."}

        url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{postal_code}?unitGroup=us&include=days&key={api_key}&contentType=json'
        
        try:
            print(f"Making request to: {url}")
            response = requests.get(url, timeout=10)  

            if response.status_code == 200:
                print("API request successful.")
                return response.json()
            elif response.status_code == 400:
                print("Postal code not found.")
                return {"error": "Postal code not found. Please verify the postal code."}
            else:
                print(f"API returned error: {response.status_code}")
                return {"error": f"API error: {response.status_code}, {response.text}"}

        except requests.exceptions.Timeout:
            print("The request to the API timed out.")
            return {"error": "The request to the API timed out. Please try again later."}

        except requests.exceptions.RequestException as e:
            print(f"Error communicating with the API: {str(e)}")
            return {"error": f"Error communicating with the API: {str(e)}"}
