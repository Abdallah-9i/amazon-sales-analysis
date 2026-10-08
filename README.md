# amazon-sales-analysis

## Project overview
This project is an end-to-end data analytics project focused on analysis Amazon sales data.

## Project Goal
The goal of this project is to analyze Amazon sales data to identify sales patterns, product performance, and potential business opportunities.

## Business Problem

The purpose of this analysis is to understand Amazon sales performance
and identify patterns that can support business decisions.

## Business Questions

- Which product categories perform the best?
- Which products perform the best and worst?
- How does product performance change over time?
- Is there a relationship between product price and sales performance?
- Is there a relationship between product ratings and sales performance?
- What patterns or opportunities can be identified from the data?

## Tools

To clean, analyze and visualize the data this project will use the follwong tools:
- Python
- SQL
- Power BI
- Excel
- Git & Github

## Data Inspection

The raw dataset was inspected using Python and Pandas before cleaning.

The inspection included:

- Checking dataset dimensions and column names
- Reviewing data types
- Identifying missing values
- Checking for duplicate records after excluding technical columns
- Investigating missing `Amount` and `currency` values
- Investigating the relationship between `Fulfilment` and `fulfilled-by`
- Reviewing missing shipping location data
- Investigating missing `Courier Status` values
- Reviewing promotion ID availability
- Investigating zero-amount transactions
- Reviewing distributions of key columns such as `Status`, `Category`, `Qty`, and `B2B`
- Inspecting unusually high quantity and amount values
- Generating summary statistics for numeric columns

### Key Findings

- The dataset contains 128,975 rows and 24 columns.
- Six duplicate records were identified after excluding the technical `index` and `Unnamed: 22` columns.
- `Amount` and `currency` have 7,795 missing values each and share the same missing-value pattern.
- Missing `fulfilled-by` values are structurally related to Amazon-fulfilled orders.
- Shipping location fields are missing together in 33 records.
- Most missing `Courier Status` values are associated with cancelled orders.
- Zero-amount transactions could not be fully explained by promotions or zero quantity and were therefore retained.
- Unusually high quantity and amount values were inspected and appeared plausible, so they were not removed.
- The `Date` column was stored as text and required conversion to datetime.

## Data Cleaning

The dataset was cleaned using Python and Pandas to improve data quality and prepare it for analysis.

The cleaning process included:

- Removing unnecessary technical columns such as `index` and `Unnamed: 22`
- Standardizing column names using lowercase and snake_case formatting
- Converting the `Date` column to datetime format
- Converting `ship_postal_code` to string format
- Replacing expected missing `fulfilled_by` values with `Not Applicable`
- Replacing missing promotion IDs with `No Promotion ID`
- Replacing missing shipping location values with `Unknown`
- Handling missing `Courier Status` values based on order status
- Keeping missing `amount` and `currency` values as null because their true values were unknown
- Removing fully duplicated records
- Performing final validation on shape, missing values, data types, and duplicates

### Cleaning Results

- The cleaned dataset contains 128,969 rows and 22 columns.
- Six duplicate records were removed.
- Remaining missing values are limited to `amount` and `currency`.
- Column names were standardized.
- Date and postal code data types were corrected.
- No duplicate rows remain after cleaning.
