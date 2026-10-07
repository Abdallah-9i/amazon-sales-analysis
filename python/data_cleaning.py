import pandas as pd

#Load the raw dataset
raw_df = pd.read_csv("../data/raw/Amazon Sale Report.csv")

# Create a copy for cleaning
clean_df = raw_df.copy()

# Remove unnecessary columns
clean_df = clean_df.drop(columns=["index", "Unnamed: 22"])

# Standardize column names
clean_df.columns = (
    clean_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# Convert Date to datetime
clean_df["date"] = pd.to_datetime(
    clean_df["date"],
    format="%m-%d-%y",
    errors="coerce"
)


#cheack if there any error led to a missing date value
print(clean_df["date"].isnull().sum())

# Convert postal code to string
clean_df["ship_postal_code"] = (
    clean_df["ship_postal_code"]
    .astype("Int64")
    .astype("string")
)

print(clean_df.columns.tolist())
print(clean_df.dtypes)