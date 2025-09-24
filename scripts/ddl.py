import sqlite3

def create_events_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                name TEXT,
                url TEXT,
                start_date TEXT,
                start_time TEXT,
                venue TEXT,
                city_name TEXT,
                country TEXT,
                segment TEXT,
                genre TEXT,
                sub_genre TEXT
            )
        """)
    except sqlite3.Error as e:
        print(f"Failed to execute the SQL for Events table: {e}")
        return

    try:
        conn.commit()
        print("Events table created successfully.")
    except sqlite3.Error as e:
        print(f"Failed to commit Events table: {e}")


def create_cities_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cities (
                city_id INTEGER PRIMARY KEY AUTOINCREMENT
                city_name TEXT,
                country TEXT,
                state TEXT,
                population INTEGER,
                latitude REAL,
                longitude REAL,
                PRIMARY KEY (city_name, country)
            )
        """)
    except sqlite3.Error as e:
        print(f"Failed to execute the SQL for Cities table: {e}")
        return

    try:
        conn.commit()
        print("Cities table created successfully.")
    except sqlite3.Error as e:
        print(f"Failed to commit Cities table: {e}")


def create_weather_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                city_name TEXT,
                country TEXT,
                datetime TEXT,
                temperature REAL,
                humidity REAL,
                wind_speed REAL,
                wind_direction TEXT,
                precipitation REAL,
                weather_description TEXT,
                PRIMARY KEY (city_name, country, datetime)
            )
        """)
    except sqlite3.Error as e:
        print(f"Failed to execute SQL for the Weather table: {e}")
        return

    try:
        conn.commit()
        print("Weather table created successfully.")
    except sqlite3.Error as e:
        print(f"Failed to commit Weather table: {e}")
