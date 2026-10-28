import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

raw_path = BASE / "data" / "raw" / "Amazon Sale Report.csv"
out_path = BASE / "data" / "cleaned" / "amazon_sales_cleaned.csv"

# -------------------------
# Load Dataset
# -------------------------

# Load the raw dataset
raw_df = pd.read_csv(
    raw_path,
    low_memory=False
)

# Create a copy for cleaning
clean_df = raw_df.copy()


# -------------------------
# Remove Unnecessary Columns
# -------------------------

clean_df = clean_df.drop(columns=["index", "Unnamed: 22"])


# -------------------------
# Standardize Column Names
# -------------------------

# Standardize column names
clean_df.columns = (
    clean_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)


# -------------------------
# Remove Duplicate Rows
# -------------------------

# Remove fully duplicated records
clean_df = clean_df.drop_duplicates()


# -------------------------
# Fix Data Types
# -------------------------

# Convert Date to datetime
clean_df["date"] = pd.to_datetime(
    clean_df["date"],
    format="%m-%d-%y",
    errors="coerce"
)

# Convert postal code to string
clean_df["ship_postal_code"] = (
    clean_df["ship_postal_code"]
    .astype("Int64")
    .astype("string")
)

# -------------------------
# Handle Missing Values
# -------------------------

# Replace expected missing fulfilled_by values
clean_df["fulfilled_by"] = clean_df["fulfilled_by"].fillna("Not Applicable")

# Replace missing promotion IDs with a descriptive value
clean_df["promotion_ids"] = clean_df["promotion_ids"].fillna("No Promotion ID")

# Replace missing shipping location values
shipping_columns = [
    "ship_city",
    "ship_state",
    "ship_postal_code",
    "ship_country"
]

clean_df[shipping_columns] = clean_df[shipping_columns].fillna("Unknown")

# Set missing Courier Status for cancelled orders
clean_df.loc[
    (clean_df["status"] == "Cancelled") &
    (clean_df["courier_status"].isnull()),
    "courier_status"
] = "Not Applicable"

# Set remaining missing Courier Status values
clean_df["courier_status"] = clean_df["courier_status"].fillna("Unknown")

# Keep missing amount and currency values as NaN because their true values are unknown.
# They should not be replaced with zero because zero is already a valid recorded value in the dataset.


# -------------------------
# Standardize Text Values
# -------------------------

# Standardize city and state values
for col in ["ship_city", "ship_state"]:
    clean_df[col] = (
        clean_df[col]
        .str.strip()
        .str.upper()
    )

# Keep Hyderabad state values as recorded because the correct state
# cannot be confirmed from the available data.

# Standardize known state naming variants
state_mapping = {
    "NEW DELHI": "DELHI",
    "AR": "ARUNACHAL PRADESH",
    "NL": "NAGALAND",
    "PB": "PUNJAB",
    "RJ": "RAJASTHAN",
    "ORISSA": "ODISHA",
    "PONDICHERRY": "PUDUCHERRY",
    "RAJSHTHAN": "RAJASTHAN",
    "RAJSTHAN": "RAJASTHAN",
    "PUNJAB/MOHALI/ZIRAKPUR": "PUNJAB"
}

clean_df["ship_state"] = clean_df["ship_state"].replace(state_mapping)

# Standardize category values
clean_df["category"] = (
    clean_df["category"]
    .str.strip()
    .str.title()
)


# -------------------------
# Create Derived Columns
# -------------------------

# Create a combined city-state field for geographic analysis
clean_df["city_state"] = (
    clean_df["ship_city"] + ", " + clean_df["ship_state"]
)


# -------------------------
# Final Validation
# -------------------------

# Check final dataset shape
print("\nFinal Shape:")
print(clean_df.shape)

# Check remaining missing values
print("\nRemaining Missing Values:")
missing_values = clean_df.isnull().sum()
print(missing_values[missing_values > 0])

# Check for duplicate rows
print("\nDuplicates:")
print(clean_df.duplicated().sum())

# Check final data types
print("\nFinal Data Types:")
print(clean_df.dtypes)

# Preview cleaned data
print("\nCleaned Data Preview:")
print(clean_df.head())

assert clean_df.shape == (128969, 23)
assert clean_df.duplicated().sum() == 0
assert clean_df["date"].notna().all()
assert clean_df["order_id"].nunique() == 120378
assert set(clean_df.columns[clean_df.isnull().any()]) == {"amount", "currency"}

# -------------------------
# Save Cleaned Dataset
# -------------------------

clean_df.to_csv(
    out_path,
    index=False
)

print("\nCleaned dataset saved successfully.")