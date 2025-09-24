CREATE VIEW monthly_city_event_weather AS
SELECT
    e.city_name,
    strftime('%Y-%m', e.start_date) AS month,
    c.population,
    ROUND(
        (
            COUNT(e.id) * 100000.0 / population
        ),
        2
    ) AS events_per_100k,
    ROUND(AVG(w.temperature), 1) AS avg_temp,
    ROUND(AVG(w.humidity), 1) AS avg_humidity
FROM
    events e
    JOIN weather w ON e.city_name = w.city_name
    AND date(e.start_date) = date(w.datetime)
    JOIN cities c ON e.city_name = c.city_name
GROUP BY
    e.city_name,
    month
ORDER BY e.city_name, month;