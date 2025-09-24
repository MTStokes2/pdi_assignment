CREATE VIEW monthly_city_event_weather AS
SELECT
    c.city_name,
    strftime('%Y-%m', f.start_date) AS month,
    c.population,
    ROUND(
        (
            COUNT(f.event_id) * 100000.0 / c.population
        ),
        2
    ) AS events_per_100k,
    ROUND(AVG(w.temperature), 1) AS avg_temp,
    ROUND(AVG(w.humidity), 1) AS avg_humidity
FROM
    fact_events f
    JOIN dim_cities c ON f.city_id = c.city_id
    LEFT JOIN dim_weather w ON f.city_id = w.city_id
GROUP BY
    c.city_name,
    month
ORDER BY c.city_name, month;