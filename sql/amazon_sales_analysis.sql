-- Data validation

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT order_id) AS unique_orders,
    COUNT(DISTINCT order_id)
        FILTER (WHERE status <> 'Cancelled') AS non_cancelled_orders,
    SUM(amount)
        FILTER (WHERE status <> 'Cancelled') AS non_cancelled_amount
FROM sales;

-- 1. Top category by state

WITH state_category AS (
    SELECT
        ship_state,
        category,
        COUNT(DISTINCT order_id) AS unique_orders,
        SUM(amount) AS recorded_amount
    FROM sales
    WHERE status <> 'Cancelled'
      AND ship_state <> 'UNKNOWN'
    GROUP BY
        ship_state,
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
            ORDER BY recorded_amount DESC NULLS LAST
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
ORDER BY recorded_amount DESC NULLS LAST;

-- 2. Promotion usage by fulfilment method

WITH order_promotion AS (
    SELECT
        order_id,
        BOOL_OR(promotion_ids <> 'No Promotion ID') AS has_promotion_id
    FROM sales
    WHERE status <> 'Cancelled'
    GROUP BY order_id
),

promotion_fulfilment AS (
    SELECT
        s.fulfilment,
        op.has_promotion_id,
        COUNT(DISTINCT s.order_id) AS unique_orders,
        SUM(s.amount) AS recorded_amount
    FROM sales s
    JOIN order_promotion op
        ON s.order_id = op.order_id
    WHERE s.status <> 'Cancelled'
    GROUP BY
        s.fulfilment,
        op.has_promotion_id
)

SELECT
    fulfilment,
    CASE
        WHEN has_promotion_id THEN 'Has Promotion ID'
        ELSE 'No Promotion ID Recorded'
    END AS promotion_status,
    unique_orders,
    recorded_amount,
    ROUND(
        unique_orders * 100.0
        / SUM(unique_orders) OVER (PARTITION BY fulfilment),
        2
    ) AS order_share_pct
FROM promotion_fulfilment
ORDER BY fulfilment, has_promotion_id DESC;

-- 3. Order value segmentation
-- Thresholds are based on Q1 and Q3 calculated during Python EDA

WITH order_totals AS (
    SELECT
        order_id,
        SUM(amount) AS recorded_amount
    FROM sales
    WHERE status <> 'Cancelled'
    GROUP BY order_id
)

SELECT
    CASE
        WHEN recorded_amount < 459 THEN 'Low Value'
        WHEN recorded_amount <= 824 THEN 'Medium Value'
        ELSE 'High Value'
    END AS value_segment,
    COUNT(*) AS unique_orders,
    ROUND(SUM(recorded_amount), 2) AS recorded_amount,
    ROUND(AVG(recorded_amount), 2) AS average_order_value
FROM order_totals
WHERE recorded_amount IS NOT NULL
GROUP BY value_segment
ORDER BY average_order_value;

-- 4. Category contribution to total recorded amount

SELECT
    category,
    SUM(amount) as recorded_amount,
    ROUND(
    SUM(amount) * 100.0
    / SUM(SUM(amount)) OVER (),
    2
) AS contribution_pct
FROM sales
WHERE status <> 'Cancelled'
GROUP BY category
ORDER BY recorded_amount DESC;

-- 5. Top state by category

WITH ranked_states AS (
    SELECT
        category,
        ship_state,
        SUM(amount) AS recorded_amount,
        RANK() OVER (
            PARTITION BY category
            ORDER BY SUM(amount) DESC NULLS LAST
        ) AS state_rank
    FROM sales
    WHERE status <> 'Cancelled'
      AND ship_state <> 'UNKNOWN'
    GROUP BY
        category,
        ship_state
)

SELECT
    category,
    ship_state,
    recorded_amount
FROM ranked_states
WHERE state_rank = 1
ORDER BY recorded_amount DESC NULLS LAST;

-- 6. Running total of recorded amount over time

WITH monthly_amount AS (
    SELECT
        DATE_TRUNC('month', date)::DATE AS month,
        SUM(amount) AS recorded_amount
    FROM sales
    WHERE status <> 'Cancelled'
    GROUP BY DATE_TRUNC('month', date)
)

SELECT
    month,
    recorded_amount,
    SUM(recorded_amount) OVER (
        ORDER BY month
    ) AS running_total
FROM monthly_amount
ORDER BY month;