from typing import Dict, Any

def load_city_data(conn, city_data: Dict[str, Any]):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO cities (city_name, country, state, population, latitude, longitude)
        VALUES (:city, :country, :state, :population, :latitude, :longitude)
    """, {
        "city": city_data.get("city_name"),
        "country": "United States of America" if city_data.get("country") == "US" else city_data.get("country"),
        "state": city_data.get("region"),
        "population": city_data.get("population"),
        "latitude": city_data.get("lat"),
        "longitude": city_data.get("lon")
    })
    conn.commit()

def load_event_data(conn, ev: Dict[str, Any]):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO events (id, name, url, start_date, start_time, venue,
            city_name, country, segment, genre, sub_genre)
        VALUES (:id, :name, :url, :start_date, :start_time, :venue, :city_name, :country, :segment, :genre, :subGenre)
    """, {
        "id": ev["ticketmaster_id"], 
        "name": ev["name"],
        "url": ev["url"],
        "start_date": ev["start_date"],
        "start_time": ev["start_time"],
        "venue": ev["venue"],
        "city_name": ev["city_name"],
        "country": "United States of America" if ev["country"] == "US" else ev["country"],
        "segment": ev["segment"],
        "genre": ev["genre"],
        "subGenre": ev["sub_genre"]
    })
    conn.commit()

def load_weather_data(conn, weather: Dict[str, Any]):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO weather (datetime, city_name, country, temperature, humidity, wind_speed, wind_direction, precipitation, weather_description)
        VALUES (:datetime, :city_name, :country, :temp, :humidity, :wind_speed, :wind_direction, :precipitation, :weather_desc)
    """, {
        "city_name": weather["city_name"],
        "country": weather["country"],
        "datetime": weather["datetime"],
        "temp": weather["temperature"],
        "humidity": weather["humidity"],
        "wind_speed": weather["wind_speed"],
        "wind_direction": weather["wind_direction"],
        "precipitation": weather["precipitation"],
        "weather_desc": weather["weather_descriptions"]
    })
    conn.commit()