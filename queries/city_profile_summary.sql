CREATE VIEW city_profile_summary AS
SELECT
    c.city_id,
    c.city_name,
    c.state,
    c.country,
    c.population,
    c.latitude,
    c.longitude,
    w.datetime AS latest_weather_date,
    w.temperature AS latest_temperature,
    w.humidity AS latest_humidity,
    COUNT(e.event_id) AS total_events
FROM
    dim_cities c
    LEFT JOIN dim_weather w ON c.city_id = w.city_id
    AND w.datetime = (
        SELECT MAX(w2.datetime)
        FROM dim_weather w2
        WHERE
            w2.city_id = c.city_id
    )
    LEFT JOIN fact_events e ON c.city_id = e.city_id
GROUP BY
    c.city_id,
    c.city_name,
    c.state,
    c.country,
    c.population,
    c.latitude,
    c.longitude;