CREATE VIEW total_events_by_genre_per_city AS
SELECT c.city_name, f.genre, COUNT(f.event_id) AS genre_count
FROM fact_events f
    JOIN dim_cities c ON f.city_id = c.city_id
GROUP BY
    c.city_name,
    f.genre
ORDER BY c.city_name, genre_count DESC;