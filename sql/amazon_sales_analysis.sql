SELECT COUNT(*)
FROM sales;

-- 1 Top category by state

WITH state_category AS (
    SELECT
        UPPER(TRIM(ship_state)) AS ship_state,
        category,
        COUNT(DISTINCT order_id) AS unique_orders,
        SUM(amount) AS recorded_amount
    FROM sales
    WHERE status <> 'Cancelled'
      AND ship_state IS NOT NULL
      AND UPPER(TRIM(ship_state)) <> 'UNKNOWN'
    GROUP BY
        UPPER(TRIM(ship_state)),
        category
),

ranked_categories AS (
    SELECT
        ship_state,
        category,
        unique_orders,
        recorded_amount,
        RANK() OVER (
            PARTITION BY ship_state
            ORDER BY recorded_amount DESC
        ) AS category_rank
    FROM state_category
)

SELECT
    ship_state,
    category,
    unique_orders,
    recorded_amount
FROM ranked_categories
WHERE category_rank = 1
ORDER BY recorded_amount DESC;