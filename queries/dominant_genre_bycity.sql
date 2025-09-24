CREATE VIEW dominant_genre_by_city AS
WITH
    genre_counts AS (
        SELECT
            c.city_id,
            c.city_name,
            c.country,
            c.state,
            e.genre,
            COUNT(*) AS genre_count,
            RANK() OVER (
                PARTITION BY
                    c.city_id
                ORDER BY COUNT(*) DESC
            ) AS genre_rank
        FROM fact_events e
            JOIN dim_cities c ON e.city_id = c.city_id
        GROUP BY
            c.city_id,
            c.city_name,
            c.country,
            c.state,
            e.genre
    )
SELECT
    city_id,
    city_name,
    country,
    state,
    genre,
    genre_count
FROM genre_counts
WHERE
    genre_rank = 1;