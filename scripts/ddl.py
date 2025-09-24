import sqlite3

def create_events_table(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fact_events (
                event_id TEXT PRIMARY KEY,
                city_id INTEGER NOT NULL,
                name TEXT,
                url TEXT,
                start_date TEXT,
                start_time TEXT,
                venue TEXT,
                segment TEXT,
                genre TEXT,
                sub_genre TEXT,
                FOREIGN KEY (city_id) REFERENCES dim_cities (city_id)
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
            CREATE TABLE IF NOT EXISTS dim_cities (
                city_id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_name TEXT NOT NULL,
                country TEXT NOT NULL,
                state TEXT,
                population INTEGER,
                latitude REAL,
                longitude REAL,
                UNIQUE (city_name, country)
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
            CREATE TABLE IF NOT EXISTS dim_weather (
                weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_id INTEGER NOT NULL,
                datetime TEXT NOT NULL,
                temperature REAL,
                humidity REAL,
                wind_speed REAL,
                wind_direction TEXT,
                precipitation REAL,
                weather_description TEXT,
                FOREIGN KEY (city_id) REFERENCES dim_cities (city_id),
                UNIQUE (city_id, datetime)
            );
        """)
    except sqlite3.Error as e:
        print(f"Failed to execute SQL for the Weather table: {e}")
        return

    try:
        conn.commit()
        print("Weather table created successfully.")
    except sqlite3.Error as e:
        print(f"Failed to commit Weather table: {e}")

def create_indexes(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_city ON fact_events (city_id);

            CREATE INDEX IF NOT EXISTS idx_weather_city_date ON dim_weather (city_id, datetime);

            CREATE INDEX IF NOT EXISTS idx_cities_name_country ON dim_cities (city_name, country);
        """)
    except sqlite3.Error as e:
        print(f"Failed to execute the SQL for the indexes: {e}")
        return

    try:
        conn.commit()
        print("Indexes created successfully.")
    except sqlite3.Error as e:
        print(f"Failed to commit indexes: {e}")