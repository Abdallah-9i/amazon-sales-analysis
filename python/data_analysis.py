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

# Compare Amount by order status
print("\nAmount by Status:")
print(
    df.groupby("status")["amount"]
    .agg(["count", "sum", "mean"])
    .sort_values("sum", ascending=False)
)

# -------------------------
# Sales Performance Analysis
# -------------------------

# Total recorded amount across all records
total_recorded_amount = df["amount"].sum()

# Total amount excluding cancelled records
non_cancelled_amount = df.loc[
    df["status"] != "Cancelled",
    "amount"
].sum()

# Amount from delivered records
delivered_amount = df.loc[
    df["status"] == "Shipped - Delivered to Buyer",
    "amount"
].sum()

print("\nTotal Recorded Amount:")
print(round(total_recorded_amount, 2))

print("\nNon-Cancelled Recorded Amount:")
print(round(non_cancelled_amount, 2))

print("\nDelivered Recorded Amount:")
print(round(delivered_amount, 2))

# Create a subset for delivered orders
delivered_df = df[
    df["status"] == "Shipped - Delivered to Buyer"
].copy()

# Create a subset for non-cancelled records
non_cancelled_df = df[
    df["status"] != "Cancelled"
].copy()

# -------------------------
# Category Analysis
# -------------------------

# Analyze category activity using non-cancelled records
category_activity = (
    non_cancelled_df.groupby("category")
    .agg(
        unique_orders=("order_id", "nunique"),
        total_quantity=("qty", "sum")
    )
    .sort_values("unique_orders", ascending=False)
)

print("\nCategory Activity:")
print(category_activity)

# Analyze delivered amount by category
category_delivered = (
    delivered_df.groupby("category")
    .agg(
        delivered_orders=("order_id", "nunique"),
        delivered_quantity=("qty", "sum"),
        delivered_amount=("amount", "sum"),
        average_amount=("amount", "mean")
    )
    .sort_values("delivered_amount", ascending=False)
)

print("\nDelivered Category Performance:")
print(category_delivered)


# -------------------------
# Sales Trends Over Time
# -------------------------

# Extract year-month from the date column for monthly analysis
delivered_df["month"] = (
    delivered_df["date"]
    .dt.to_period("M")
    .astype(str)
)

# Aggregate delivered orders, quantity, and amount by month
monthly_trends = (
    delivered_df.groupby("month")
    .agg(
        delivered_orders=("order_id", "nunique"),
        delivered_quantity=("qty", "sum"),
        delivered_amount=("amount", "sum")
    )
    .reset_index()
)

print("\nMonthly Delivered Trends:")
print(monthly_trends)

# Check delivered date coverage within each month
print("\nMonthly Date Coverage:")
print(
    delivered_df.groupby("month")["date"]
    .agg(["min", "max", "nunique"])
)

# Compare complete months only
complete_months = monthly_trends[
    monthly_trends["month"].isin(["2022-04", "2022-05"])
].copy()

complete_months["orders_change_pct"] = (
    complete_months["delivered_orders"]
    .pct_change()
    .mul(100)
)

complete_months["amount_change_pct"] = (
    complete_months["delivered_amount"]
    .pct_change()
    .mul(100)
)

print("\nComplete Month Comparison:")
print(complete_months.round(2))

# Calculate average amount per delivered order
complete_months["average_amount_per_order"] = (
    complete_months["delivered_amount"]
    / complete_months["delivered_orders"]
)

print("\nAverage Amount per Delivered Order:")
print(
    complete_months[
        ["month", "average_amount_per_order"]
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

# Analyze delivered performance by B2B segment
b2b_delivered = (
    delivered_df.groupby("b2b")
    .agg(
        delivered_orders=("order_id", "nunique"),
        delivered_quantity=("qty", "sum"),
        delivered_amount=("amount", "sum"),
        average_amount=("amount", "mean")
    )
    .reset_index()
)

# Calculate delivered order share
b2b_delivered["order_share_pct"] = (
    b2b_delivered["delivered_orders"]
    / b2b_delivered["delivered_orders"].sum()
    * 100
)

print("\nDelivered B2B Performance:")
print(b2b_delivered.round(2))