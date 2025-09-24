import sqlite3


sql_files = [
    "queries/city_profile_summary.sql",
    "queries/city_weather_profile.sql",
    "queries/dominant_genre_bycity.sql",
    "queries/event_weather_conditions.sql",
    "queries/events_by_month.sql",
    "queries/monthly_city_event_weather.sql",
    "queries/top_10_cities_by_events.sql",
    "queries/total_events_by_genre_per_city.sql",
]

def create_views(conn):
    for sql_file_path in sql_files:
        try:
            with open(sql_file_path, 'r') as sql_file:
                sql_script = sql_file.read()
        except FileNotFoundError as e:
            print(f"SQL file not found at: {sql_file_path} - {e}")
            continue
        except Exception as e:
            print(f"Failed to read SQL file at: {sql_file_path} - {e}")
            continue

        try:
            conn.executescript(sql_script)
        except sqlite3.Error as e:
            print(f"Failed to execute SQL script from {sql_file_path}: {e}")
            continue

        try:
            conn.commit()
            print(f"Committed changes for SQL file: {sql_file_path}")
        except sqlite3.Error as e:
            print(f"Failed to commit changes for {sql_file_path}: {e}")

