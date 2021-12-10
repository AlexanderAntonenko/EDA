import requests
import json
import pprint
from datetime import datetime
import pandas as pd


ONE_DAY = 86400


class Weather:
    
    def __init__(self, first_date, cities_info, api_key):
        self.first_date = first_date
        self.cities_info = cities_info
        self.api_key = api_key

        
    def parse_data(self):
        weather_descriptions = []
        for city in self.cities_info.keys():

            for i in range(5):  
                parse_date = self.first_date + i * ONE_DAY

                url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={self.cities_info[city]['lat']}&lon={self.cities_info[city]['lon']}&dt={parse_date}&appid={self.api_key}"

                r = requests.get(url)

                data = json.loads(r.text)
                for hour in  data['hourly']:
                    weather_descriptions.append({'city': city,
                                             'dt': hour['dt'], 
                                             'humidity': hour['humidity'], 
                                             'pressure': hour['pressure'],
                                             'description': hour['weather'][0]['description'],
                                             'wind_speed': hour['wind_speed'],
                                             'wind_deg': hour['wind_deg'],
                                             'temp': hour['temp']
                                            })
        return {'weather': weather_descriptions}


def create_json_file(weather_descriptions, file_name):
    with open(file_name, 'w') as f:
        json.dump(weather_descriptions, f)

        
def create_dataframe(file_name):
    with open(file_name, 'r') as file:
        file_data = json.load(file)

    return pd.DataFrame(file_data['weather'])