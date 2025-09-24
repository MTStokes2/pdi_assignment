CREATE VIEW IF NOT EXISTS top_cities_by_events AS
SELECT c.city_name, c.country, COUNT(f.event_id) AS total_events
FROM fact_events f
    JOIN dim_cities c ON f.city_id = c.city_id
GROUP BY
    c.city_name,
    c.country
ORDER BY total_events DESC
LIMIT 10;