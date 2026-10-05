import pandas as pd

#Load the raw dataset
raw_df = pd.read_csv("../data/raw/Amazon Sale Report.csv")

# Create a copy for cleaning
clean_df = raw_df.copy()