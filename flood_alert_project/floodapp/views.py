import requests
from datetime import datetime, timedelta
from django.shortcuts import render
from geopy.geocoders import Nominatim
from django.conf import settings
from .models import FloodDataRecord
import joblib
import os

MODEL_PATH = os.path.join("floodapp", "ml_models", "lr_model.pkl")
SCALER_PATH = os.path.join("floodapp", "ml_models", "scalar.pkl")

# Load model and scaler once at module load
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
except Exception as e:
    model = None
    scaler = None
    print(f"Error loading model or scaler: {e}")

def fetch_nasa_power_rainfall_avg(lat, lon, days=7):
    end_date = datetime.utcnow().date() - timedelta(days=2)
    start_date = end_date - timedelta(days=days - 1)
    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters=PRECTOTCORR"
        f"&community=AG"
        f"&longitude={lon}"
        f"&latitude={lat}"
        f"&start={start_str}"
        f"&end={end_str}"
        f"&format=JSON"
    )

    print("Fetching rainfall from NASA POWER API with URL:", url)
    try:
        response = requests.get(url)
        data = response.json()
        print("Response data:", data)
        rainfall_dict = data.get('properties', {}).get('parameter', {}).get('PRECTOTCORR', {})
        print("Rainfall data dictionary:", rainfall_dict)
        valid_rainfall = [v for v in rainfall_dict.values() if v not in (-999, -999.0)]

        if not valid_rainfall:
            print("No valid rainfall data found.")
            return None

        avg_rainfall = sum(valid_rainfall) / len(valid_rainfall)
        print(f"Average rainfall over {days} days: {avg_rainfall}")
        return round(avg_rainfall, 2)
    except Exception as e:
        print("Error fetching rainfall data:", e)
        return None


def location_submit_view(request):
    lat, lon = None, None
    message = ""
    weather_data = {}
    average_rainfall = None
    flood_occurred = 0
    flood_risk = None

    if request.method == 'POST':
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')
        flood_occurred_input = request.POST.get('flood_occurred')
        flood_occurred = 1 if flood_occurred_input == 'yes' else 0

        if lat and lon:
            message = f"Your live location is: Latitude {lat}, Longitude {lon}"
        else:
            manual_input = request.POST.get('manual_location')
            if manual_input:
                geolocator = Nominatim(user_agent="flood_alert_app")
                try:
                    if ',' in manual_input:
                        lat, lon = map(str.strip, manual_input.split(','))
                        message = f"Manual Coordinates: Latitude {lat}, Longitude {lon}"
                    else:
                        location = geolocator.geocode(manual_input)
                        if location:
                            lat, lon = location.latitude, location.longitude
                            message = f"{manual_input.title()} is at: Latitude {lat}, Longitude {lon}"
                        else:
                            message = "Could not find location. Please check your input."
                except Exception as e:
                    message = f"Error: {e}"

        if lat and lon and model and scaler:
            try:
                lat = float(lat)
                lon = float(lon)

                # Fetch current weather
                current_url = (
                    f"https://api.openweathermap.org/data/2.5/weather"
                    f"?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
                )
                current_res = requests.get(current_url).json()

                forecast_url = (
                    f"https://api.openweathermap.org/data/2.5/forecast"
                    f"?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
                )
                forecast_res = requests.get(forecast_url).json()
                forecast_list = forecast_res.get("list", [])

                rain_3h = forecast_list[0].get("rain", {}).get("3h", 0) if forecast_list else 0
                rain_6h = sum(forecast_list[i].get("rain", {}).get("3h", 0) for i in range(min(2, len(forecast_list))))
                rain_24h = sum(entry.get("rain", {}).get("3h", 0) for entry in forecast_list[:8])

                weather_data = {
                    "temperature": current_res.get("main", {}).get("temp", 0),
                    "humidity": current_res.get("main", {}).get("humidity", 0),
                    "wind_speed": current_res.get("wind", {}).get("speed", 0),
                    "condition": current_res.get("weather", [{}])[0].get("main", "N/A"),
                    "description": current_res.get("weather", [{}])[0].get("description", "N/A"),
                    "rain_1h": current_res.get("rain", {}).get("1h", 0),
                    "rain_3h": rain_3h,
                    "rain_6h": rain_6h,
                    "rain_24h": rain_24h,
                }

                average_rainfall = fetch_nasa_power_rainfall_avg(lat, lon, days=7)
                if average_rainfall is None:
                    average_rainfall = 0  # fallback if no data

                # Feature vector [avg_rainfall, rain_24h, temperature, humidity, flood_occurred]
                features = [
                    #average_rainfall,
                    rain_24h,
                    weather_data.get("temperature", 0),
                    weather_data.get("humidity", 0),
                    flood_occurred,
                ]

                # Scale features
                scaled_features = scaler.transform([features])

                # Predict flood risk
                prediction = model.predict(scaled_features)[0]
                risk_levels = {
                    0: "Minimum Risk",
                    1: "Low",
                    2: "Mild",
                    3: "Warning",
                    4: "High",
                }
                flood_risk = risk_levels.get(prediction, "Unknown")

            except Exception as e:
                flood_risk = f"Error in processing: {e}"
                weather_data = {}

    else:
        message = "Please submit location data."

    return render(request, 'floodapp/flood_form.html', {
        'message': message,
        'lat': lat,
        'lon': lon,
        'weather': weather_data,
        'average_rainfall': average_rainfall,
        'flood_risk': flood_risk,
    })

def home(request):
    return render(request, 'floodapp/home.html')
