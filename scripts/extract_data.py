import requests
import traceback

# ----------------------------------------
#            API Ninjas(Cities)
# ----------------------------------------
def fetch_api_ninjas_city(city_name: str, api_key: str):
     url = f"https://api.api-ninjas.com/v1/city?name={city_name}"
     headers = {"X-API-Key": api_key}
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
#           Ticket Master(Events)
# ----------------------------------------
def fetch_ticketmaster_events_for_city(city_name: str, api_key: str):
    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"

    events = []

    while True:
        params = {
            "apikey": api_key,
            "city": city_name,
        }

        request = requests.get(base_url, params=params)
        response = request.json()

        if "_embedded" not in response or "events" not in response["_embedded"]:
            break
        
        for event in response["_embedded"]["events"]:
            try:
                classification = event.get("classifications", [{}][0]) #sometimes an event has no classifications
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
#           WeatherStack(Weather)
# ----------------------------------------
def fetch_weather_for_city(city_name: str, country: str, api_key: str):
    base_url = "http://api.weatherstack.com/current"
    params = {"access_key": api_key, "query": f"{city_name}, {country}", "units": "f"}

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