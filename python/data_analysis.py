import pandas as pd


# -------------------------
# Load Cleaned Dataset
# -------------------------

df = pd.read_csv(
    "../data/cleaned/amazon_sales_cleaned.csv",
    parse_dates=["date"]
)
# -------------------------
# Helper Functions
# -------------------------

def sum_min1(x):
    """Sum values while returning NaN, not 0, when all values are missing."""
    return x.sum(min_count=1)

def summarize(data, by, include_quantity=True):
    """
    Summarize unique orders, quantity, and recorded amount by group.
    Average recorded amount is divided by all unique orders,
    including orders with missing amount values.
    """
    agg = {
        "unique_orders": ("order_id", "nunique"),
        "recorded_amount": ("amount", sum_min1)
    }

    if include_quantity:
        agg["total_quantity"] = ("qty", "sum")

    result = data.groupby(by).agg(**agg).reset_index()

    result["average_recorded_amount_per_order"] = (
        result["recorded_amount"] / result["unique_orders"]
    )

    return result

def add_order_share(data):
    """
    Add order share for mutually exclusive groups such as B2B,
    fulfilment, and promotion.

    Do not use for category because one order can contain
    multiple categories.
    """
    result = data.copy()

    result["order_share_pct"] = (
        result["unique_orders"]
        / result["unique_orders"].sum()
        * 100
    )

    return result

def show(title, data):
    """Print a formatted analysis table with values rounded to two decimals."""
    print(f"\n{title}:")
    print(data.round(2).to_string(index=False))

# -------------------------
# Analysis Overview
# -------------------------

print("\nDataset Shape:")
print(df.shape)

print("\nDate Range:")
print(df["date"].min(), "to", df["date"].max())

print("\nUnique Orders:")
print(df["order_id"].nunique())

print("\nQuantity Summary:")
print(df["qty"].describe())

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

print("\nUnique Orders by Status:")
print(order_status["status"].value_counts())

print("\nOrder Status Distribution (%):")
print(
    order_status["status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

# Compare recorded amount by status
status_amount_analysis = (
    df.groupby("status")
    .agg(
        records=("order_id", "size"),
        amount_count=("amount", "count"),
        recorded_amount=("amount", sum_min1),
        average_recorded_amount=("amount", "mean")
    )
    .sort_values("recorded_amount", ascending=False)
)

print("\nStatus Amount Analysis:")
print(status_amount_analysis.round(2))


# -------------------------
# Sales Performance Analysis
# -------------------------

total_recorded_amount = df["amount"].sum()

# Non-cancelled includes every status except "Cancelled",
# including returned, failed, pending, and other non-final statuses.
non_cancelled_df = df[
    df["status"] != "Cancelled"
].copy()

non_cancelled_amount = non_cancelled_df["amount"].sum()

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

category_analysis = (
    summarize(non_cancelled_df, "category")
    .sort_values("recorded_amount", ascending=False)
)

show("Category Performance", category_analysis)


# -------------------------
# Sales Trends Over Time
# -------------------------

non_cancelled_df["month"] = (
    non_cancelled_df["date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_trends = summarize(non_cancelled_df, "month")

days_covered = (
    non_cancelled_df.groupby("month")["date"]
    .nunique()
)

monthly_trends["days_covered"] = (
    monthly_trends["month"].map(days_covered)
)

monthly_trends["orders_per_day"] = (
    monthly_trends["unique_orders"]
    / monthly_trends["days_covered"]
)

monthly_trends["recorded_amount_per_day"] = (
    monthly_trends["recorded_amount"]
    / monthly_trends["days_covered"]
)

show("Monthly Non-Cancelled Trends", monthly_trends)

# Use months with enough date coverage
comparable_months = monthly_trends[
    monthly_trends["days_covered"] >= 28
].copy()

comparable_months["orders_per_day_change_pct"] = (
    comparable_months["orders_per_day"]
    .pct_change()
    .mul(100)
)

comparable_months["amount_per_day_change_pct"] = (
    comparable_months["recorded_amount_per_day"]
    .pct_change()
    .mul(100)
)

show(
    "Comparable Monthly Trends",
    comparable_months[
        [
            "month",
            "days_covered",
            "orders_per_day",
            "recorded_amount_per_day",
            "average_recorded_amount_per_order",
            "orders_per_day_change_pct",
            "amount_per_day_change_pct"
        ]
    ]
)


# -------------------------
# Quantity Analysis
# -------------------------

quantity_per_order = (
    non_cancelled_df.groupby("order_id")["qty"]
    .sum()
)

print("\nQuantity per Order Summary:")
print(quantity_per_order.describe())

single_unit_orders = (quantity_per_order == 1).sum()
multi_unit_orders = (quantity_per_order > 1).sum()

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

print("\nSingle-Unit Orders:")
print(single_unit_orders)

print("\nMulti-Unit Orders:")
print(multi_unit_orders)

print("\nSingle-Unit Orders Percentage:")
print(round(single_unit_pct, 2))

print("\nMulti-Unit Orders Percentage:")
print(round(multi_unit_pct, 2))


# -------------------------
# B2B Analysis
# -------------------------

b2b_analysis = add_order_share(
    summarize(non_cancelled_df, "b2b")
)

show(
    "Non-Cancelled B2B Performance",
    b2b_analysis
)


# -------------------------
# Fulfilment Analysis
# -------------------------

fulfilment_analysis = add_order_share(
    summarize(non_cancelled_df, "fulfilment")
)

show(
    "Non-Cancelled Fulfilment Performance",
    fulfilment_analysis
)

# Check status differences by fulfilment using record counts
print("\nFulfilment by Status (Record Counts):")
print(
    pd.crosstab(
        df["fulfilment"],
        df["status"]
    )
)

# Calculate cancellation rate using unique orders
order_fulfilment = (
    df[["order_id", "fulfilment", "status"]]
    .drop_duplicates()
)

order_fulfilment["is_cancelled"] = (
    order_fulfilment["status"] == "Cancelled"
)

cancellation_by_fulfilment = (
    order_fulfilment.groupby("fulfilment")
    .agg(
        total_orders=("order_id", "nunique"),
        cancelled_orders=("is_cancelled", "sum")
    )
    .reset_index()
)

cancellation_by_fulfilment["cancellation_rate_pct"] = (
    cancellation_by_fulfilment["cancelled_orders"]
    / cancellation_by_fulfilment["total_orders"]
    * 100
)

show(
    "Cancellation Rate by Fulfilment",
    cancellation_by_fulfilment
)


# -------------------------
# Promotion Analysis
# -------------------------

# Check whether each order has at least one Promotion ID
order_promotion_status = (
    non_cancelled_df.groupby("order_id")["promotion_ids"]
    .apply(lambda x: (x != "No Promotion ID").any())
)

promotion_df = non_cancelled_df.copy()

promotion_df["has_promotion_id"] = (
    promotion_df["order_id"]
    .map(order_promotion_status)
)

promotion_analysis = add_order_share(
    summarize(promotion_df, "has_promotion_id")
)

promotion_analysis["promotion_status"] = (
    promotion_analysis["has_promotion_id"]
    .map({
        True: "Has Promotion ID",
        False: "No Promotion ID Recorded"
    })
)

show(
    "Promotion Analysis",
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
)

# Check relationship between Promotion ID and fulfilment
promotion_orders = promotion_df.drop_duplicates("order_id")

print("\nPromotion by Fulfilment:")
print(
    pd.crosstab(
        promotion_orders["has_promotion_id"],
        promotion_orders["fulfilment"]
    )
)


# -------------------------
# Geographic Analysis
# -------------------------

geo_df = non_cancelled_df.copy()

# Standardize geographic values
for col in ["ship_state", "ship_city"]:
    geo_df[col] = (
        geo_df[col]
        .str.strip()
        .str.upper()
    )

# Remove unknown geographic values
geo_df = geo_df[
    (geo_df["ship_state"] != "UNKNOWN")
    & (geo_df["ship_city"] != "UNKNOWN")
].copy()

state_analysis = summarize(
    geo_df,
    "ship_state",
    include_quantity=False
)

city_analysis = summarize(
    geo_df,
    ["ship_state", "ship_city"],
    include_quantity=False
)

show(
    "Top 10 States",
    state_analysis
    .sort_values("unique_orders", ascending=False)
    .head(10)
)

show(
    "Top 10 Cities",
    city_analysis
    .sort_values("unique_orders", ascending=False)
    .head(10)
)


# -------------------------
# Correlation Analysis
# -------------------------

order_correlation = (
    non_cancelled_df.groupby("order_id")
    .agg(
        total_quantity=("qty", "sum"),
        recorded_amount=("amount", sum_min1)
    )
    .dropna()
)

quantity_amount_correlation = (
    order_correlation["total_quantity"]
    .corr(order_correlation["recorded_amount"])
)

print("\nQuantity and Recorded Amount Correlation:")
print(round(quantity_amount_correlation, 3))


# -------------------------
# Outlier Analysis
# -------------------------

q1 = order_correlation["recorded_amount"].quantile(0.25)
q3 = order_correlation["recorded_amount"].quantile(0.75)
iqr = q3 - q1

upper_bound = q3 + (1.5 * iqr)

print("\nHigh Recorded Amount Outlier Threshold:")
print(round(upper_bound, 2))

high_amount_outliers = order_correlation[
    order_correlation["recorded_amount"] > upper_bound
]

print("\nHigh Recorded Amount Outliers:")
print(len(high_amount_outliers))

print("\nTop 10 Orders by Recorded Amount:")
print(
    order_correlation
    .sort_values("recorded_amount", ascending=False)
    .head(10)
    .round(2)
)

print("\nTop 10 Orders by Quantity:")
print(
    order_correlation
    .sort_values("total_quantity", ascending=False)
    .head(10)
)

# Calculate recorded amount per unit
order_correlation["amount_per_unit"] = (
    order_correlation["recorded_amount"]
    / order_correlation["total_quantity"]
)

print("\nAmount per Unit Summary:")
print(
    order_correlation["amount_per_unit"]
    .describe()
    .round(2)
)

# Count records with zero recorded amount
zero_amount_records = (
    non_cancelled_df["amount"] == 0
).sum()

print("\nZero Recorded Amount Records:")
print(zero_amount_records)


# -------------------------
# Validation Checks
# -------------------------

assert (status_per_order > 1).sum() == 0
assert df["order_id"].nunique() == 120378
assert non_cancelled_df["order_id"].nunique() == 103193