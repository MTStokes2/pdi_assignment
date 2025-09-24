# City Events & Weather ETL Project

## Overview
This project builds an ETL pipeline that extracts, transforms, and loads data from:
- **[Ticketmaster API](https://developer.ticketmaster.com/products-and-docs/apis/getting-started/)** for Event Data
- **[API Ninjas City API](https://api-ninjas.com/api/city)** for City Demographics & Location Data
- **[Weatherstack API](https://weatherstack.com/documentation)** for Current Weather Data
> All require a key and the worst one is Weatherstack...sorry
> 
> Weatherstack wants address and email and restricts to 100 requests per month hence the hardcoded city list (reduce it to use less requests)
> 
> Would switch to using [Open-Meteo](https://open-meteo.com/en/docs) if I had found it earlier

Some Questions answered through this:
- Which Cities host the most events?
- What are the diminant genres in each city?
- What is the average temperature and humidity of a city?
- How does weather impact the events?

## Structure
```
├── queries/
│ ├── city_profile_summary.sql
│ ├── city_weather_profile.sql
│ ├── dominant_genre_bycity.sql
│ ├── event_weather_conditions.sql
│ └── ... (others)
│
├── scripts/
│ ├── create_views.py          Creates the views (city_profile_summary.sql, etc)
│ ├── ddl.py                   Creates tables and indexes (dim_cities, dim_weather, fact_events)
│ ├── extract_data.py          Holds the scripts that extract the data from the APIs
│ ├── load_data.py             Holds the scripts that load the extracted and transformed data into the database
│
│ README.md
│ database_design.png
│.env                          Stores API keys
│ main.py                      Main python file that executes all of the scripts
│ pdi_assignment.db            SQLite database (generated after ETL run of multiple days. It's a "backup")
│ pdi_assignment_new.db        SQLite database (generated from script)
│ requirements.txt             Package and version requirements
```
## Setup
### Install Dependencies
> personally havent used this method before so listed below is what I used
```
pip install -r requirements.txt
```
### Dependencies
```
requests
traceback
python-dotenv
sqlite3
```
### Configure .env file
```
TICKETMASTER_API_KEY = "your_key"
NINJA_CITY_API_KEY = "your_key"
WEATHERSTACK_API_KEY = "your_key"
```
## Run
```
python .\main.py
```

