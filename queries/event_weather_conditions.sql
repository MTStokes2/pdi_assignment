CREATE VIEW events_weather_conditions AS
SELECT e.city_name, e.name AS event_name, e.start_time, e.start_date, w.temperature, w.humidity, w.weather_description
FROM events e
    LEFT JOIN weather w ON e.start_date = w.datetime
WHERE
    e.city_name = w.city_name