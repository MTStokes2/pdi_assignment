CREATE VIEW total_events_by_genre_per_city AS
SELECT city_name, genre, COUNT(*) AS genre_count
FROM events
GROUP BY
    city_name,
    genre
ORDER BY city_name, genre_count DESC;