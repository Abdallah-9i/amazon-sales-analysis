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


## Exploratory Data Analysis

Exploratory data analysis was performed using Python and Pandas on the cleaned dataset.

The full dataset was used for order-status analysis, while non-cancelled records were used as the main population for business analysis. The `Amount` field is referred to as **Recorded Amount** because the dataset includes cancelled, returned, pending, and other non-final order statuses.

### Key Findings

- The cleaned dataset contains **128,969 records** and **120,378 unique orders**.
- `Shipped` is the most common status at **60.33%**, while `Cancelled` accounts for **14.21%**.
- Non-cancelled records account for approximately **71.67M** in Recorded Amount.
- **Set** is the leading category by Recorded Amount at approximately **35.73M**, despite having a similar number of orders to `kurta`.
- From April to May, unique orders decreased by **13.79%** and Recorded Amount decreased by **8.70%**, while average Recorded Amount per order increased from **670.41** to **709.96**.
- **94.04%** of non-cancelled orders are single-unit orders.
- B2B represents only **0.71%** of non-cancelled orders, but has a higher average Recorded Amount per order (**768.41**) than non-B2B orders (**694.01**).
- Amazon fulfilment accounts for **70.93%** of non-cancelled unique orders, while Merchant accounts for **29.07%**. Their average Recorded Amount per order is relatively similar.
- **Maharashtra** is the leading state with **18,002** non-cancelled unique orders, while **Bengaluru** is the leading city with **9,785**.
- Orders with a recorded Promotion ID represent **70.93%** of non-cancelled orders and have a higher average Recorded Amount per order.
- Quantity and Recorded Amount show a **moderate positive correlation of 0.57**.
- High-value outliers were reviewed using the IQR method and retained because they did not appear to be obvious data errors.

### Notes

- `Recorded Amount` should not be interpreted as confirmed revenue or net sales.
- `No Promotion ID Recorded` does not necessarily mean no promotion was applied.
- Correlation indicates association, not causation.
