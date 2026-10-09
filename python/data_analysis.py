import pandas as pd

# Load cleaned dataset
df = pd.read_csv(
    "../data/cleaned/amazon_sales_cleaned.csv",
    parse_dates=["date"]
)