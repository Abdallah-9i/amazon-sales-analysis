import pandas as pd

# Load raw dataset
raw_df = pd.read_csv("../data/raw/Amazon Sale Report.csv")

# -------------------------
# Basic Dataset Inspection
# -------------------------

# Dataset size
print("Dataset Shape:")
print(raw_df.shape)

# Column names
print("\nColumns:")
print(raw_df.columns.tolist())

# First 5 rows
print("\nFirst 5 Rows:")
print(raw_df.head())

# Data types
print("\nData Types:")
print(raw_df.dtypes)

# Missing values
print("\nMissing Values:")
print(raw_df.isnull().sum())

# Duplicate rows
print("\nDuplicates:")
print(raw_df.duplicated().sum())


# -------------------------
# Amount Investigation
# -------------------------

# Filter rows with missing Amount
missing_amount = raw_df[raw_df["Amount"].isnull()]

# Check Status for missing Amount rows
print("\nMissing Amount by Status:")
print(missing_amount["Status"].value_counts())

# Show non-cancelled orders with missing Amount
print("\nNon-cancelled orders with missing Amount:")
print(missing_amount[
    missing_amount["Status"] != "Cancelled"
][["Order ID", "Status", "Qty", "Category", "currency", "Amount"]].head(30))

# Check if Amount and currency are missing together
print("\nAmount and currency missing together:")
print((raw_df["Amount"].isnull() == raw_df["currency"].isnull()).value_counts())

# Count missing Amount rows by quantity
print("\nQty = 0:")
print((missing_amount["Qty"] == 0).sum())

print("\nQty > 0:")
print((missing_amount["Qty"] > 0).sum())

# Filter missing Amount rows with positive quantity
positive_qty_missing_amount = missing_amount[missing_amount["Qty"] > 0]

# Check Status of positive quantity rows with missing Amount
print("\nStatus of positive Qty rows with missing Amount:")
print(positive_qty_missing_amount["Status"].value_counts())


# -------------------------
# Fulfilment Investigation
# -------------------------

# Check Fulfilment values
print("\n" + raw_df["Fulfilment"].value_counts(dropna=False).to_string())

# Check fulfilled-by values
print("\n" + raw_df["fulfilled-by"].value_counts(dropna=False).to_string())

# Missing values in "fulfilled-by" are expected:
# Amazon orders have NaN, while Merchant orders use "Easy Ship"
print("\nCrosstab of Fulfilment and Fulfilled By:")
print(pd.crosstab(
    raw_df["Fulfilment"],
    raw_df["fulfilled-by"],
    dropna=False
))


# -------------------------
# Promotion Investigation
# -------------------------

print("\nMissing promotion IDs:")
print(raw_df["promotion-ids"].isnull().sum())

print("\nNon-missing promotion IDs:")
print(raw_df["promotion-ids"].notnull().sum())


# -------------------------
# Column Value Inspection
# -------------------------

# Check Status values
print("\n" + raw_df["Status"].value_counts(dropna=False).to_string())

# Check Category values
print("\n" + raw_df["Category"].value_counts(dropna=False).to_string())

# Check Qty distribution
print("\n" + raw_df["Qty"].value_counts().sort_index().to_string())

# Check B2B values
print("\n" + raw_df["B2B"].value_counts(dropna=False).to_string())

# Check Date data type
print("\n" + str(raw_df["Date"].dtype))

# Check sample Date values
print("\n" + raw_df["Date"].head().to_string(index=False))

# Summary statistics for numeric columns
print("\nNumeric Summary:")
print(raw_df.describe())


# Check if shipping location fields are missing together
shipping_columns = [
    "ship-city",
    "ship-state",
    "ship-postal-code",
    "ship-country"
]

print(
    raw_df[shipping_columns]
    .isnull()
    .all(axis=1)
    .sum()
)