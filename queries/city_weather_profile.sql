CREATE VIEW city_weather_profile AS
SELECT
    c.city_id,
    c.city_name,
    c.country,
    c.state,
    c.population,
    COUNT(e.event_id) AS total_events,
    ROUND(
        CAST(COUNT(e.event_id) AS FLOAT) / c.population * 100000,
        2
    ) AS events_per_100k,
    ROUND(AVG(w.temperature), 1) AS avg_event_temp,
    ROUND(AVG(w.humidity), 1) AS avg_event_humidity,
    ROUND(AVG(w.precipitation), 1) AS avg_event_precipitation,
    ROUND(AVG(w.wind_speed), 1) AS avg_event_wind_speed
FROM
    dim_cities c
    LEFT JOIN fact_events e ON c.city_id = e.city_id
    LEFT JOIN dim_weather w ON e.city_id = w.city_id
GROUP BY
    c.city_id,
    c.city_name,
    c.country,
    c.state,
    c.population;