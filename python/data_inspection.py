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