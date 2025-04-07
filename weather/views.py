import requests
from django.shortcuts import render
import os

API_KEY = "0d328630cf40bde10e6239f70ac57df7"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
LAST_CITY_FILE = "last_city.txt"

def fetch_weather(city):
    try:
        response = requests.get(BASE_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        })
        data = response.json()
        if response.status_code == 200:
            return {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temp": data["main"]["temp"],
                "condition": data["weather"][0]["main"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"]
            }, None
        else:
            return None, data.get("message", "City not found")
    except requests.exceptions.RequestException:
        return None, "Network error. Please check your connection."

def save_last_city(city):
    with open(LAST_CITY_FILE, "w") as file:
        file.write(city)

def load_last_city():
    if os.path.exists(LAST_CITY_FILE):
        with open(LAST_CITY_FILE, "r") as file:
            return file.read().strip()
    return ""

def index(request):
    weather = None
    error = None
    city = ""

    if request.method == "POST":
        city = request.POST.get("city")
        if city:
            weather, error = fetch_weather(city)
            if not error:
                save_last_city(city)
    else:
        city = load_last_city()
        if city:
            weather, error = fetch_weather(city)

    return render(request, "index.html", {
        "weather": weather,
        "error": error,
        "city": city
    })
