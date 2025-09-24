CREATE VIEW city_profile_summary AS
SELECT
    c.city_name,
    c.state,
    c.country,
    c.population,
    c.latitude,
    c.longitude,
    w.datetime AS latest_weather_date,
    w.temperature AS latest_temperature,
    w.humidity AS latest_humidity,
    COUNT(e.id) AS total_events
FROM
    cities c
    LEFT JOIN weather w ON c.city_name = w.city_name
    AND w.datetime = (
        SELECT MAX(w2.datetime)
        FROM weather w2
        WHERE
            w2.city_name = c.city_name
    )
    LEFT JOIN events e ON c.city_name = e.city_name
GROUP BY
    c.city_name,
    c.state,
    c.country;