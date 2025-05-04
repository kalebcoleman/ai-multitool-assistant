import requests
from dotenv import load_dotenv
import os
from llama_index.core.tools import FunctionTool, ToolMetadata
import re

load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
        return f"The weather in {weather['city']} is {weather['description']} with a temperature of {weather['temperature']}°C."
    else:
        return 'City not found.'

def weather_tool(prompt):
    match = re.search(r'weather in ([\w\s]+)', prompt, re.IGNORECASE)
    if match:
        city = match.group(1).strip()
        return get_weather(city)
    else:
        return 'Invalid prompt. Please ask for the weather using the format: "weather in [CITY or STATE]"'

weather_engine = FunctionTool.from_defaults(
    fn=weather_tool,
    name="weather_information",
    description="This tool provides weather information for a specified city. you MUST ask for the weather using the format: 'weather in [CITY or STATE]' or it WILL NOT WORK!"
)
