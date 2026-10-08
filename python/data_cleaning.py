import pandas as pd

# -------------------------
# Load Dataset
# -------------------------

# Load the raw dataset
raw_df = pd.read_csv("../data/raw/Amazon Sale Report.csv")

# Create a copy for cleaning
clean_df = raw_df.copy()


# -------------------------
# Remove Unnecessary Columns
# -------------------------

# Remove unnecessary columns
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
# Fix Data Types
# -------------------------

# Convert Date to datetime
clean_df["date"] = pd.to_datetime(
    clean_df["date"],
    format="%m-%d-%y",
    errors="coerce"
)

# Check if any conversion errors resulted in missing date values
print(clean_df["date"].isnull().sum())

# Convert postal code to string
clean_df["ship_postal_code"] = (
    clean_df["ship_postal_code"]
    .astype("Int64")
    .astype("string")
)

# Verify column names and data types
print(clean_df.columns.tolist())
print(clean_df.dtypes)


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