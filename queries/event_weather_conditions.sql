CREATE VIEW events_weather_conditions AS
SELECT c.city_name, e.name AS event_name, e.start_date, e.start_time, w.temperature, w.humidity, w.weather_description
FROM
    fact_events e
    JOIN dim_cities c ON e.city_id = c.city_id
    LEFT JOIN dim_weather w ON e.city_id = w.city_id
    AND DATE(e.start_date) = DATE(w.datetime);