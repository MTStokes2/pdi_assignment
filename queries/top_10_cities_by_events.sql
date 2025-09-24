CREATE VIEW IF NOT EXISTS top_cities_by_events AS
SELECT
    city_name,
    country,
    COUNT(*) AS total_events
FROM events
GROUP BY
    city_name,
    country
ORDER BY total_events DESC
LIMIT 10;