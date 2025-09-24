CREATE VIEW events_by_month AS
SELECT strftime('%Y-%m', start_date) AS month, COUNT(*) AS total_events
FROM fact_events
GROUP BY
    month
ORDER BY month;