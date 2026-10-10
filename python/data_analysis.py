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
