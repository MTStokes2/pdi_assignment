from typing import Dict, Any

def load_city_data(conn, city_data: Dict[str, Any]):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO dim_cities (city_name, country, state, population, latitude, longitude)
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

def get_city_id(conn, city_name):
    cursor = conn.cursor()
    cursor.execute("SELECT city_id FROM dim_cities WHERE city_name = ?", (city_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def load_event_data(conn, ev: Dict[str, Any]):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO fact_events (event_id, city_id, name, url, start_date, start_time, venue, segment, genre, sub_genre)
        VALUES (:event_id, :city_id, :name, :url, :start_date, :start_time, :venue, :segment, :genre, :subGenre)
    """, {
        "event_id": ev["ticketmaster_id"], 
        "city_id": get_city_id(conn, ev["city_name"]),
        "name": ev["name"],
        "url": ev["url"],
        "start_date": ev["start_date"],
        "start_time": ev["start_time"],
        "venue": ev["venue"],
        "segment": ev["segment"],
        "genre": ev["genre"],
        "subGenre": ev["sub_genre"]
    })
    conn.commit()

def load_weather_data(conn, weather: Dict[str, Any]):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO dim_weather (datetime, city_id, temperature, humidity, wind_speed, wind_direction, precipitation, weather_description)
        VALUES (:datetime, :city_id, :temp, :humidity, :wind_speed, :wind_direction, :precipitation, :weather_desc)
    """, {
        "city_id": get_city_id(conn, weather["city_name"]),
        "datetime": weather["datetime"],
        "temp": weather["temperature"],
        "humidity": weather["humidity"],
        "wind_speed": weather["wind_speed"],
        "wind_direction": weather["wind_direction"],
        "precipitation": weather["precipitation"],
        "weather_desc": weather["weather_descriptions"]
    })
    conn.commit()