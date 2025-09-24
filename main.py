import os
import sqlite3
import requests
import time
import traceback
from datetime import datetime
from dotenv import load_dotenv

import scripts.load_data as data
import scripts.ddl as ddl
import scripts.create_views as views
import scripts.extract_data as extract

load_dotenv() 
TICKETMASTER_API_KEY = os.getenv("TICKETMASTER_API_KEY")
NINJA_CITY_API_KEY = os.getenv("NINJA_CITY_API_KEY")
WEATHERSTACK_API_KEY = os.getenv("WEATHERSTACK_API_KEY")

#List of cities to query the apis (based on the top 12 populated cities)
CITIES_TO_PROCESS = [
    "New York", "Los Angeles",  "Chicago", "Houston", "Phoenix", "San Antonio", "Philadelphia", "San Diego", "Dallas", "Fort Worth", "Jacksonville", "Austin"
]


if __name__ == "__main__":
    conn = sqlite3.connect("pdi_assignment_new.db")
    ddl.create_events_table(conn)
    ddl.create_cities_table(conn)
    ddl.create_weather_table(conn)
    ddl.create_indexes(conn)

    views.create_views(conn)
    print(CITIES_TO_PROCESS)

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
        city_data = extract.fetch_api_ninjas_city(city, NINJA_CITY_API_KEY)
        if city_data:
            data.load_city_data(conn, city_data)
        print(f"Finished loading City Data in {time.time() - step_start:.2f} seconds")

        # Events data
        step_start = time.time()
        print("\n" + "=" * 50)
        print(f"Step 2: Loading {city} Events")
        print("=" * 50)
        events = extract.fetch_ticketmaster_events_for_city(city, TICKETMASTER_API_KEY)
        for ev in events:
            data.load_event_data(conn, ev)
        print(f"Finished loading Events Data in {time.time() - step_start:.2f} seconds")

        # Weather data
        step_start = time.time()
        print("\n" + "=" * 50)
        print(f"Step 3: Loading {city} Weather")
        print("=" * 50)
        weather = extract.fetch_weather_for_city(city, "United States of America", WEATHERSTACK_API_KEY)
        if weather:
            data.load_weather_data(conn, weather)
        print(f"Finished loading Weather Data in {time.time() - step_start:.2f} seconds")

        print(f"\n Total time for {city}: {time.time() - city_start:.2f} seconds")

    conn.close()
    print("\n" + "#" * 60)
    print(f"Finished all Cities in {time.time() - start_time:.2f} seconds")
    print("#" * 60) 


