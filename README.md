🌊 Flood Alert System
A Django-based web application that predicts the risk of flood in a specific region based on live weather data, historical rainfall patterns, and a machine learning model. It integrates OpenWeather and NASA POWER APIs and supports both live location and manual location input.

🚀 Features
📍 Live or Manual Location Input

🌦️ Current Weather Data via OpenWeather API

☁️ Historical Rainfall (7 days) from NASA POWER API

🤖 ML-Based Flood Risk Prediction (5 risk levels)

✅ User-friendly UI with Bootstrap

🔄 Rainfall data normalized using pre-trained Scaler

🛠️ Technologies Used
Backend: Django 5.2

Frontend: HTML, Bootstrap

APIs:

OpenWeather – for live weather data

NASA POWER – for historical rainfall

ML Model: Scikit-learn Linear Regression model (lr_model.pkl)

Geocoding: geopy + Nominatim

Web Server: Gunicorn

Static Files: WhiteNoise for production

📁 Project Structure
arduino
Copy code
flood-alert/
│
├── floodapp/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   └── flood_form.html
│   ├── ml_models/
│   │   ├── lr_model.pkl
│   │   └── scalar.pkl
│   └── views.py
│
├── static/
├── manage.py
├── requirements.txt
└── README.md
📦 Setup Instructions
Clone the Repository

bash
Copy code
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Create Virtual Environment

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Dependencies

bash
Copy code
pip install -r requirements.txt
Set Environment Variables

Create a .env file or update settings.py with:

bash
Copy code
OPENWEATHER_API_KEY=your_openweather_api_key
Run the App

bash
Copy code
python manage.py runserver
⚙️ How It Works
Users can choose:

Live location using geolocation

Manual input of city name or lat/lon

The backend:

Fetches current weather

Retrieves historical rainfall from NASA

Scales weather/rainfall data

Feeds data into the ML model

Returns a flood risk label like:
Minimum Risk, Low, Mild, Warning, or High

📸 UI Screenshots
Add screenshots here if available.

📌 Future Improvements
Email/SMS alerts

Auto-scheduled background flood scans

Flood maps integration

Admin dashboard for reports

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

