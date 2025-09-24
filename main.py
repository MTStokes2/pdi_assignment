#!/usr/bin/env python3
import os
import sqlite3
import requests
import time
import traceback
from datetime import datetime
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

import scripts.load_data as data
import scripts.ddl as ddl
import scripts.create_views as views

load_dotenv() 

TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
NINJA_CITY_API_KEY = os.getenv("NINJA_CITY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

CITIES_TO_PROCESS = [
    "New York", "Los Angeles",  "Chicago", "Houston", "Phoenix", "San Antonio", "Philadelphia", "San Diego", "Dallas", "Fort Worth", "Jacksonville", "Austin"
] 



# ----------------------------------------
#               API Ninjas
# ----------------------------------------
def fetch_api_ninjas_city(city_name: str):
     url = f"https://api.api-ninjas.com/v1/city?name={city_name}"
     headers = {"X-API-Key": NINJA_CITY_API_KEY}
     request = requests.get(url, headers=headers)
     try:
          data = request.json()
          city = data[0]
          return {
            "city_name": city.get("name"),
            "country": city.get("country"),
            "region": city.get("region"), 
            "population": city.get("population"),
            "lat": city.get("latitude"),
            "lon": city.get("longitude"),
          }
     except Exception as e:
          print(f"API Ninjas City parsing failed for {city_name}: {e}")

# ----------------------------------------
#             Ticket Master
# ----------------------------------------
def fetch_ticketmaster_events_for_city(city_name: str):
    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"

    events = []

    while True:
        params = {
            "apikey": TICKETMASTER_API_KEY,
            "city": city_name,
        }

        request = requests.get(base_url, params=params)
        response = request.json()

        if "_embedded" not in response or "events" not in response["_embedded"]:
            break
        
        for event in response["_embedded"]["events"]:
            try:
                classification = event.get("classifications", [{}][0])
                venue = event["_embedded"].get("venues")[0]
                dates = event["dates"]["start"]

                ev = {
                    "ticketmaster_id": event.get("id"),
                    "name": event.get("name"),
                    "url": event.get("url"),
                    "start_date": dates.get("localDate"),
                    "start_time": dates.get("localTime"),
                    "segment": "N/A" if classification == {} else classification[0]["segment"]["name"],
                    "genre": "N/A" if classification == {} else classification[0]["genre"]["name"],
                    "sub_genre": "N/A" if classification == {} else classification[0]["subGenre"]["name"],
                    "venue": venue.get("name"),
                    "city_name": venue.get("city")["name"],
                    "country": venue.get("country")["name"],
                }
                events.append(ev)
            except KeyError as ke:
                print(f"Event is missing a {ke}")
            except Exception as e:
                print(f"Error: {e}")
                traceback.print_exc()
                try:
                    print(f"Partial event data: {ev}")
                except UnboundLocalError:
                    print("Event dict not created yet.")
            
                    
        return events

# ----------------------------------------
#              WeatherStack
# ----------------------------------------
def fetch_weather_for_city(city_name: str, country: str):
    base_url = "http://api.weatherstack.com/current"
    params = {"access_key": WEATHERSTACK_API_KEY, "query": f"{city_name}, {country}", "units": "f"}

    request = requests.get(base_url, params=params)

    try:
        response = request.json()
        if "error" in response:
            print(f"Weatherstack error for {city_name}, {country}: {response['error']}")
            return None
        location = response.get("location", {})
        current = response.get("current", {})
        if not location or not current:
            return None
        
        localtime = location.get("localtime", "")
        return {
            "city_name": location.get("name"),
            "country": location.get("country"),
            "datetime": localtime,
            "temperature": current.get("temperature"),
            "humidity": current.get("humidity"),
            "wind_speed": current.get("wind_speed"),
            "wind_direction": current.get("wind_dir"),
            "precipitation": current.get("precip"),
            "weather_descriptions": (current.get("weather_descriptions") or [None])[0]
        }
    except ValueError:
        print("Weatherstack returned a non-json response")
        return None


if __name__ == "__main__":
    conn = sqlite3.connect("events_project.db")
    ddl.create_events_table(conn)
    ddl.create_cities_table(conn)
    ddl.create_weather_table(conn)

    views.create_views(conn)

    start_time = time.time()
    for city in CITIES_TO_PROCESS:
        city_start = time.time()
        print("\n" + "-" * 50)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Processing {city}")
        print("-" * 50)

        # City data
        step_start = time.time()
        print("\n" + "=" * 50)
        print(f"Step 1: Loading {city} City Data")
        print("=" * 50)
        city_data = fetch_api_ninjas_city(city)
        if city_data:
            data.load_city_data(conn, city_data)
        print(f"Finished loading City Data in {time.time() - step_start:.2f} seconds")

        # Events data
        """ step_start = time.time()
        print("\n" + "=" * 50)
        print(f"Step 2: Loading {city} Events")
        print("=" * 50)
        events = fetch_ticketmaster_events_for_city(city)
        for ev in events:
            data.load_event_data(conn, ev)
        print(f"Finished loading Events Data in {time.time() - step_start:.2f} seconds") """

        # Weather data
        """ step_start = time.time()
        print("\n" + "=" * 50)
        print(f"Step 3: Loading {city} Weather")
        print("=" * 50)
        weather = fetch_weather_for_city(city, "United States of America")
        if weather:
            data.load_weather_data(conn, weather)
        print(f"Finished loading Weather Data in {time.time() - step_start:.2f} seconds") """

        print(f"\n Total time for {city}: {time.time() - city_start:.2f} seconds")

    conn.close()
    print("\n" + "#" * 60)
    print(f"Finished all Cities in {time.time() - start_time:.2f} seconds")
    print("#" * 60) 


