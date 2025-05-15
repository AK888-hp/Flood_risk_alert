import requests
from datetime import datetime, timedelta

def fetch_nasa_power_rainfall(lat, lon, days=7):
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)
    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point"
        f"?parameters=PRECTOT"
        f"&community=AG"
        f"&longitude={lon}"
        f"&latitude={lat}"
        f"&start={start_str}"
        f"&end={end_str}"
        f"&format=JSON"
    )

    response = requests.get(url)
    data = response.json()
    
    rainfall_dict = data.get('properties', {}).get('parameter', {}).get('PRECTOT', {})
    
    cleaned_data = {
        datetime.strptime(date_str, "%Y%m%d").date(): rainfall_mm
        for date_str, rainfall_mm in rainfall_dict.items()
    }
    return cleaned_data
