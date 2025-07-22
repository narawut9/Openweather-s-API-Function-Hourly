import json
import requests
import psycopg2
from datetime import datetime
from dotenv import load_dotenv
import os
from database_manager import get_db_connection ,DB_CONFIG
from test import print_weather_data_types
load_dotenv()
# --- API_KEY ----
API_KEY = os.getenv("API_KEY")

# --- url ---
# url = os.getenv("OPENWEATHER_API_KEY")

# 1. Connect to DB
conn = get_db_connection(DB_CONFIG)
cur = conn.cursor()
# 2. ดึง station จาก master
def get_weather_station_id_list(conn):

    try:
        query = '''
            SELECT weather_station_id, latitude, longitude
            FROM weather."tblWeather_station_tmd"
            WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
        '''
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()

        # แปลงเป็น list ของ dict
        stations = []
        for r in rows:
            stations.append({
                "weather_station_id": r[0],
                "lat": r[1],
                "lon": r[2]
            })

        return stations

    except Exception as e:
        print(f"[Error]: {e}")
        return []

# stations = get_weather_station_list(conn)

# for station in stations:
#     print(station)


# 3. ดึง weather daily
def fetch_weather_daily (lat, lon):

    try: 
        weather_url = (
            "https://api.openweathermap.org/data/2.5/weather"
            "?lat={lat}&lon={lon}"
            "&appid={api_key}&units=metric"
        ).format(lat=lat, lon=lon, api_key=API_KEY)

        response = requests.get(weather_url)
        weather_data = response.json()
        return weather_data
    
    except requests.exceptions.RequestException as e: 
        print(f"Error fetching station data from {weather_url}: {e}")
        return None
    except json.JSONDecodeError as e: 
        print(f"Error fetching station data from {weather_url}: {e}")
        return None
    except ValueError as e :
        print(f"Error decoding station data JSON from {weather_url}: {e}")
        return None
    except Exception as e : 
        print(f"[Database ERROR] {e}")

#  4. Extract Station (lat, lon)
create_by = 'Narawut.T'
update_by = 'Narawut.T'
create_date = datetime.now()
update_date = datetime.now()

stations = get_weather_station_id_list(conn) # จาก MS table

for s in stations:
    try:
        weather_station_id = s["weather_station_id"]
        lat = s["lat"]
        lon = s["lon"]

    except Exception as e:
        print(f"[Error] Failed to process station: {s} → {e}")

    weather_daily = fetch_weather_daily(lat, lon)

    try: obs_datetime = datetime.fromtimestamp(weather_daily['dt'])
    except: obs_datetime = None

    try: temp = float(weather_daily['main']['temp'])
    except: temp = None
    
    try: temp_max = float(weather_daily['main']['temp_max'])
    except: temp_max = None
    
    try: temp_min = float(weather_daily['main']['temp_min'])
    except: temp_min = None

    try: feels_like = float(weather_daily['main']['feels_like'])
    except: feels_like = None
    
    try: humidity = float(weather_daily['main']['humidity'])
    except: humidity = None
    
    try: pressure = float(weather_daily['main']['pressure'])
    except: pressure = None
    
    try: rain_1h = float(weather_daily.get['rain']['1h']) # แก้ <------ หาโครงสร้าง JSON ที่มี rain 
    except: rain_1h = None

    try: wind_speed = float(weather_daily['wind']['speed'])
    except: wind_speed = None

    try: wind_gust = float(weather_daily['wind']['gust'])
    except: wind_gust = None

    try: cloud_all = float(weather_daily['clouds']['all'])
    except: cloud_all = None

    try: weather_main = str(weather_daily['weather'][0]['main'])
    except: weather_main = None
    
    try: weather_description = str(weather_daily['weather'][0]['description'])
    except: weather_description = None

    # print(weather_main)
    # print(f"{obs_datetime}, {temp}, {weather_main}, {weather_description}, {lat}, {lon}, {rain_1h}")
    
# # Insert 
#     # if weather_station_id != None:
#     try:
#         cur = conn.cursor()
#         sql_query = '''
#             INSERT INTO weather."tblWeather_daily_os"(
#                 weather_station_id, obs_datetime, temp, temp_max, temp_min, 
#                 feels_like, humidity, pressure, rain_1h, wind_speed, wind_gust, cloud_all, 
#                 weather_main, weather_description, create_date, create_by, update_date, update_by)
#             VALUES (
#                 %s, %s, %s, %s, %s, 
#                 %s, %s, %s, %s, %s, 
#                 %s, %s, %s, %s, %s, 
#                 %s, %s, %s
#             );
#         '''
#         cur.execute(sql_query, (
#             weather_station_id, obs_datetime, temp, temp_max, temp_min, 
#             feels_like, humidity, pressure, rain_1h, wind_speed, wind_gust, cloud_all, 
#             weather_main, weather_description, create_date, create_by ,update_date, update_by
#         ))
#         conn.commit()
#         cur.close()
#         print(f"Complete to insert weather. (WeatherStationID: {weather_station_id}, DateTime = {obs_datetime})")
#         # print("ETL Completed")
#     except Exception as e:
#         print(e)
        # print(f"Failed to insert WeatherStationID = {weather_station_id}: {e}")

# if conn:
#     try:
#         conn.close()
#         print("Database connection closed successfully.")
#     except psycopg2.Error as e:
#         print(f"Error closing database connection: {e}")