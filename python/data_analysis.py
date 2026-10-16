import pandas as pd

# Load cleaned dataset
df = pd.read_csv(
    "../data/cleaned/amazon_sales_cleaned.csv",
    parse_dates=["date"]
)

# -------------------------
# Analysis Overview
# -------------------------

# Check dataset shape
print("\nDataset Shape:")
print(df.shape)

# Check analysis date range
print("\nDate Range:")
print(df["date"].min(), "to", df["date"].max())

# Count unique orders
print("\nUnique Orders:")
print(df["order_id"].nunique())

# Quantity summary
print("\nQuantity Summary:")
print(df["qty"].describe())

# Amount summary
print("\nAmount Summary:")
print(df["amount"].describe())


# -------------------------
# Order Status Analysis
# -------------------------

# Check whether any order has more than one status
status_per_order = df.groupby("order_id")["status"].nunique()

print("\nOrders with More Than One Status:")
print((status_per_order > 1).sum())

# Create one row per unique order
order_status = df[["order_id", "status"]].drop_duplicates()

# Count unique orders by status
print("\nUnique Orders by Status:")
print(
    order_status["status"]
    .value_counts()
)

# Calculate percentage of unique orders by status
print("\nOrder Status Distribution (%):")
print(
    order_status["status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

# Compare recorded amount by order status
status_amount_analysis = (
    df.groupby("status")
    .agg(
        records=("order_id", "size"),
        amount_count=("amount", "count"),
        recorded_amount=(
            "amount",
            lambda x: x.sum(min_count=1)
        ),
        average_recorded_amount=("amount", "mean")
    )
    .sort_values("recorded_amount", ascending=False)
)

print("\nStatus Amount Analysis:")
print(status_amount_analysis.round(2))


# -------------------------
# Sales Performance Analysis
# -------------------------

# Total recorded amount across all records
total_recorded_amount = df["amount"].sum()

# Create a subset for non-cancelled records
non_cancelled_df = df[
    df["status"] != "Cancelled"
].copy()

# Total recorded amount excluding cancelled records
non_cancelled_amount = non_cancelled_df["amount"].sum()

# Recorded amount from explicitly delivered records
explicitly_delivered_amount = df.loc[
    df["status"] == "Shipped - Delivered to Buyer",
    "amount"
].sum()

print("\nTotal Recorded Amount:")
print(round(total_recorded_amount, 2))

print("\nNon-Cancelled Recorded Amount:")
print(round(non_cancelled_amount, 2))

print("\nExplicitly Delivered Recorded Amount:")
print(round(explicitly_delivered_amount, 2))



# -------------------------
# Category Analysis
# -------------------------

# Analyze category performance using non-cancelled records
category_analysis = (
    non_cancelled_df.groupby("category")
    .agg(
        unique_orders=("order_id", "nunique"),
        total_quantity=("qty", "sum"),
        recorded_amount=(
            "amount",
            lambda x: x.sum(min_count=1)
        )
    )
    .sort_values("recorded_amount", ascending=False)
    .reset_index()
)
# Calculate average recorded amount per unique order
category_analysis["average_recorded_amount_per_order"] = (
    category_analysis["recorded_amount"]
    / category_analysis["unique_orders"]
)

print("\nCategory Performance:")
print(category_analysis.round(2).to_string(index=False))


# -------------------------
# Sales Trends Over Time
# -------------------------

# Extract year-month from the date column for monthly analysis
non_cancelled_df["month"] = (
    non_cancelled_df["date"]
    .dt.to_period("M")
    .astype(str)
)

# Aggregate non-cancelled orders, quantity, and amount by month
monthly_trends = (
    non_cancelled_df.groupby("month")
    .agg(
        unique_orders=("order_id", "nunique"),
        total_quantity=("qty", "sum"),
        recorded_amount=(
            "amount",
            lambda x: x.sum(min_count=1)
        )
    )
    .reset_index()
)

print("\nMonthly Non-Cancelled Trends:")
print(monthly_trends)

# Check date coverage within each month
print("\nMonthly Date Coverage:")
print(
    non_cancelled_df.groupby("month")["date"]
    .agg(["min", "max", "nunique"])
)

# Compare complete months only
complete_months = monthly_trends[
    monthly_trends["month"].isin(["2022-04", "2022-05"])
].copy()

complete_months["orders_change_pct"] = (
    complete_months["unique_orders"]
    .pct_change()
    .mul(100)
)

complete_months["amount_change_pct"] = (
    complete_months["recorded_amount"]
    .pct_change()
    .mul(100)
)

print("\nComplete Month Comparison:")
print(complete_months.round(2))

# Calculate average recorded amount per unique order
complete_months["average_recorded_amount_per_order"] = (
    complete_months["recorded_amount"]
    / complete_months["unique_orders"]
)

print("\nAverage Recorded Amount per Order:")
print(
    complete_months[
        ["month", "average_recorded_amount_per_order"] 
        ].round(2)
)


# -------------------------
# Quantity Analysis
# -------------------------

# Calculate total quantity for each non-cancelled order
quantity_per_order = (
    non_cancelled_df.groupby("order_id")["qty"]
    .sum()
)

print("\nQuantity per Order Summary:")
print(quantity_per_order.describe())

# Count single-unit and multi-unit orders
single_unit_orders = (quantity_per_order == 1).sum()
multi_unit_orders = (quantity_per_order > 1).sum()

print("\nSingle-Unit Orders:")
print(single_unit_orders)

print("\nMulti-Unit Orders:")
print(multi_unit_orders)

# Calculate order quantity percentages
single_unit_pct = (
    single_unit_orders
    / len(quantity_per_order)
    * 100
)

multi_unit_pct = (
    multi_unit_orders
    / len(quantity_per_order)
    * 100
)

print("\nSingle-Unit Orders Percentage:")
print(round(single_unit_pct, 2))

print("\nMulti-Unit Orders Percentage:")
print(round(multi_unit_pct, 2))


# -------------------------
# B2B Analysis
# -------------------------

# Compare non-cancelled B2B and non-B2B orders
b2b_analysis = (
    non_cancelled_df.groupby("b2b")
    .agg(
        unique_orders=("order_id", "nunique"),
        total_quantity=("qty", "sum"),
        recorded_amount=(
            "amount",
            lambda x: x.sum(min_count=1)
        ),
    )
    .reset_index()
)
# Calculate average recorded amount per unique order
b2b_analysis["average_recorded_amount_per_order"] = (
    b2b_analysis["recorded_amount"]
    / b2b_analysis["unique_orders"]
)

# Calculate share of non-cancelled orders
b2b_analysis["order_share_pct"] = (
    b2b_analysis["unique_orders"]
    / b2b_analysis["unique_orders"].sum()
    * 100
)

print("\nNon-Cancelled B2B Performance:")
print(b2b_analysis.round(2).to_string(index=False))


# -------------------------
# Fulfilment Analysis
# -------------------------

# Compare non-cancelled activity by fulfilment method
fulfilment_analysis = (
    non_cancelled_df.groupby("fulfilment")
    .agg(
        unique_orders=("order_id", "nunique"),
        total_quantity=("qty", "sum"),
        recorded_amount=(
            "amount",
            lambda x: x.sum(min_count=1)
        ),
    )
    .reset_index()
)
# Calculate average recorded amount per unique order
fulfilment_analysis["average_recorded_amount_per_order"] = (
    fulfilment_analysis["recorded_amount"]
    / fulfilment_analysis["unique_orders"]
)

# Calculate share of non-cancelled orders
fulfilment_analysis["order_share_pct"] = (
    fulfilment_analysis["unique_orders"]
    / fulfilment_analysis["unique_orders"].sum()
    * 100
)

print("\nNon-Cancelled Fulfilment Performance:")
print(
    fulfilment_analysis.round(2).to_string(index=False))

# Check how order status differs by fulfilment method
print("\nFulfilment by Status:")
print(
    pd.crosstab(
        df["fulfilment"],
        df["status"]
    )
)
# -------------------------
# Geographic Analysis
# -------------------------

# Prepare geographic data from non-cancelled records
geo_df = non_cancelled_df[
    (non_cancelled_df["ship_state"] != "Unknown")
    & (non_cancelled_df["ship_city"] != "Unknown")
].copy()

# Standardize geographic values
geo_df["ship_state"] = (
    geo_df["ship_state"]
    .str.strip()
    .str.upper()
)

geo_df["ship_city"] = (
    geo_df["ship_city"]
    .str.strip()
    .str.upper()
)

# Analyze states
state_analysis = (
    geo_df.groupby("ship_state")
    .agg(
        unique_orders=("order_id", "nunique"),
        recorded_amount=(
            "amount",
            lambda x: x.sum(min_count=1)
        )
    )
    .reset_index()
)

state_analysis["average_recorded_amount_per_order"] = (
    state_analysis["recorded_amount"]
    / state_analysis["unique_orders"]
)

print("\nTop 10 States:")
print(
    state_analysis
    .sort_values("unique_orders", ascending=False)
    .head(10)
    .round(2)
    .to_string(index=False)
)

# Analyze cities
city_analysis = (
    geo_df.groupby("ship_city")
    .agg(
        unique_orders=("order_id", "nunique"),
        recorded_amount=(
            "amount",
            lambda x: x.sum(min_count=1)
        )
    )
    .reset_index()
)

city_analysis["average_recorded_amount_per_order"] = (
    city_analysis["recorded_amount"]
    / city_analysis["unique_orders"]
)

print("\nTop 10 Cities:")
print(
    city_analysis
    .sort_values("unique_orders", ascending=False)
    .head(10)
    .round(2)
    .to_string(index=False)
)

# -------------------------
# Promotion Analysis
# -------------------------

# Identify whether each order has at least one recorded promotion ID
order_promotion_status = (
    non_cancelled_df.groupby("order_id")["promotion_ids"]
    .apply(lambda x: (x != "No Promotion ID").any())
)

# Add the order-level promotion status to each record
promotion_df = non_cancelled_df.copy()

promotion_df["has_promotion_id"] = (
    promotion_df["order_id"]
    .map(order_promotion_status)
)

# Compare orders by promotion ID availability
promotion_analysis = (
    promotion_df.groupby("has_promotion_id")
    .agg(
        unique_orders=("order_id", "nunique"),
        total_quantity=("qty", "sum"),
        recorded_amount=(
            "amount",
            lambda x: x.sum(min_count=1)
        )
    )
    .reset_index()
)

# Calculate average recorded amount per unique order
promotion_analysis["average_recorded_amount_per_order"] = (
    promotion_analysis["recorded_amount"]
    / promotion_analysis["unique_orders"]
)

# Calculate share of non-cancelled orders
promotion_analysis["order_share_pct"] = (
    promotion_analysis["unique_orders"]
    / promotion_analysis["unique_orders"].sum()
    * 100
)

# Make the labels easier to understand
promotion_analysis["promotion_status"] = (
    promotion_analysis["has_promotion_id"]
    .map({
        True: "Has Promotion ID",
        False: "No Promotion ID Recorded"
    })
)

print("\nPromotion Analysis:")
print(
    promotion_analysis[
        [
            "promotion_status",
            "unique_orders",
            "total_quantity",
            "recorded_amount",
            "average_recorded_amount_per_order",
            "order_share_pct"
        ]
    ]
    .round(2)
    .to_string(index=False)
)

# -------------------------
# Correlation Analysis
# -------------------------

# Aggregate quantity and recorded amount by order
order_correlation = (
    non_cancelled_df.groupby("order_id")
    .agg(
        total_quantity=("qty", "sum"),
        recorded_amount=(
            "amount",
            lambda x: x.sum(min_count=1)
        )
    )
    .dropna()
)

# Calculate correlation between quantity and recorded amount
quantity_amount_correlation = (
    order_correlation["total_quantity"]
    .corr(order_correlation["recorded_amount"])
)

print("\nQuantity and Recorded Amount Correlation:")
print(round(quantity_amount_correlation, 3))

# -------------------------
# Outlier Analysis
# -------------------------

# Calculate IQR for recorded amount per order
q1 = order_correlation["recorded_amount"].quantile(0.25)
q3 = order_correlation["recorded_amount"].quantile(0.75)

iqr = q3 - q1

# Calculate the upper threshold for high-value outliers
upper_bound = q3 + (1.5 * iqr)

print("\nHigh Recorded Amount Outlier Threshold:")
print(round(upper_bound, 2))

# Identify high recorded amount outliers
high_amount_outliers = order_correlation[
    order_correlation["recorded_amount"] > upper_bound
]

print("\nHigh Recorded Amount Outliers:")
print(len(high_amount_outliers))

# Display the top 10 orders by recorded amount
print("\nTop 10 Orders by Recorded Amount:")
print(
    order_correlation
    .sort_values("recorded_amount", ascending=False)
    .head(10)
    .round(2)
)

# Display the top 10 orders by quantity
print("\nTop 10 Orders by Quantity:")
print(
    order_correlation
    .sort_values("total_quantity", ascending=False)
    .head(10)
)