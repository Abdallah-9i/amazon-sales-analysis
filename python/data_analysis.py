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

# Count records by order status
print("\nRecords by Status:")
print(
    df["status"]
    .value_counts()
)

# Calculate percentage of each status
print("\nStatus Distribution (%):")
print(
    df["status"]
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
        recorded_amount=("amount", "sum"),
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
        recorded_amount=("amount", "sum")
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
        recorded_amount=("amount", "sum"),
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
        recorded_amount=("amount", "sum"),
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
        recorded_amount=("amount", "sum")
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
        recorded_amount=("amount", "sum")
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