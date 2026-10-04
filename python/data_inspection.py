import pandas as pd

# Load raw dataset
raw_df = pd.read_csv("../data/raw/Amazon Sale Report.csv")

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

# Is the missing values in "Amount" column connected more to a specific "Status"?
missing_amount = raw_df[raw_df["Amount"].isnull()]
print(missing_amount["Status"].value_counts())


# Show non-cancelled orders with missing Amount
print(missing_amount[
    missing_amount["Status"] != "Cancelled"
][["Order ID", "Status", "Qty", "Category", "currency", "Amount"]].head(30))

# Check if Amount and currency are missing together
print((raw_df["Amount"].isnull() == raw_df["currency"].isnull()).value_counts())

# Count missing Amount rows with zero quantity
print("Qty = 0:")
print((missing_amount["Qty"] == 0).sum())

# Count missing Amount rows with positive quantity
print("Qty > 0:")
print((missing_amount["Qty"] > 0).sum())

# Filter missing Amount rows with positive quantity
positive_qty_missing_amount = missing_amount[missing_amount["Qty"] > 0]

# Check the status of those rows
print(positive_qty_missing_amount["Status"].value_counts())