import requests
from datetime import datetime
import pytz
from twilio.rest import Client
from keys import Keys


new_key = Keys()


api_key = new_key.open_weather_appid
forecast_end_point = "https://api.openweathermap.org/data/2.5/forecast"
lat_long_end_point = "http://api.openweathermap.org/geo/1.0/direct"

lat_long_parameters = {
    "q": "Ubatuba, BR",
    "appid": api_key,
    }
response = requests.get(lat_long_end_point, params=lat_long_parameters)
response.raise_for_status()
data_list = response.json()
#print(data_list)
lat = data_list[0]["lat"]
long = data_list[0]["lon"]
#print(f"lat {lat} long {long}")
forecast_parameters = {
    "lat": lat,
    "lon": long,
    "cnt": "4",
    "appid": api_key,
    "units": "metric",
    "lang": "pt_br"
    }
response = requests.get(forecast_end_point, params=forecast_parameters)
response.raise_for_status()
data = response.json()

brazil_timezone = pytz.timezone('America/Sao_Paulo')


will_rain = False
data_list = data["list"]
for index, element in enumerate(data_list):
  dt = element["dt"]
  weather = element["weather"]
  temp = element["main"]["temp"]
  for index_w, element_w in enumerate(weather):
      #print(f"Element {index + 1}: dt {dt} weather {weather}")
      weather_code = element_w["id"]
      # Convert the timestamp to Brazil time directly
      brazil_datetime = datetime.fromtimestamp(dt, tz=pytz.utc).astimezone(brazil_timezone)
      if weather_code < 700:
          will_rain = True
          #print(f"dt {brazil_datetime} weather_code {weather_code}")

if will_rain:
    # sending SMS via Twilio
    client = Client(new_key.twilio_account_sid, new_key.twilio_auth_token)
    message = client.messages.create(
        body="It's going to rain today, remember to bring an Umbrella",
        from_=new_key.twilio_from,
        to=new_key.twilio_to
    )

    print(message.status)
