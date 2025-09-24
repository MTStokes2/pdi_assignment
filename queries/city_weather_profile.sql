CREATE VIEW city_weather_profile AS
SELECT
    c.city_name,
    c.population,
    COUNT(e.id) AS total_events,
    ROUND(
        CAST(COUNT(e.id) AS FLOAT) / c.population * 100000,
        2
    ) AS events_per_100k,
    ROUND(AVG(w.temperature), 1) AS avg_event_temp,
    ROUND(AVG(w.humidity), 1) AS avg_event_humidity,
    ROUND(AVG(w.precipitation), 1) AS avg_event_precipitation,
    ROUND(AVG(w.wind_speed), 1) AS avg_event_wind_speed
FROM
    cities c
    LEFT JOIN events e ON c.city_name = e.city_name
    LEFT JOIN weather w ON e.city_name = w.city_name
GROUP BY
    c.city_name,
    c.country,
    c.population;