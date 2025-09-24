CREATE VIEW dominant_genre_by_city AS
WITH
    genre_counts AS (
        SELECT
            city_name,
            genre,
            COUNT(*) AS genre_count,
            RANK() OVER (
                PARTITION BY
                    city_name
                ORDER BY COUNT(*) DESC
            ) AS genre_rank
        FROM events
        GROUP BY
            city_name,
            genre
    )
SELECT city_name, genre, genre_count
FROM genre_counts
WHERE
    genre_rank = 1;