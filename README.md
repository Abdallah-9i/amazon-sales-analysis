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
- Reviewing non-null currency values
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
- All non-null currency values were confirmed to be INR (Indian Rupees).
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
- Performing final validation on dataset shape, missing values, data types, and duplicates

### Cleaning Results

- The cleaned dataset contains **128,969 rows and 22 columns**.
- Six duplicate records were removed.
- Remaining missing values are limited to `amount` and `currency`.
- Column names were standardized.
- Date and postal code data types were corrected.
- No duplicate rows remain after cleaning.

## Exploratory Data Analysis

Exploratory data analysis was performed using Python and Pandas on the cleaned dataset.

The full dataset was used for order-status analysis, while non-cancelled records were used as the main population for business analysis. Non-cancelled records include all statuses except `Cancelled`, including returned, pending, failed, and other non-final statuses. The `Amount` field is therefore referred to as **Recorded Amount** rather than confirmed revenue or net sales. All non-null currency values were confirmed to be **INR (Indian Rupees)**, so monetary values are reported in ₹.

### Key Findings

- The cleaned dataset contains **128,969 records** and **120,378 unique orders**.
- `Shipped` is the most common order status at **60.50%** of unique orders, while `Cancelled` accounts for **14.28%**.
- Non-cancelled records account for approximately **₹71.67M** in Recorded Amount.
- **Set** is the leading category by Recorded Amount at approximately **₹35.73M**, despite having a similar number of unique orders to `kurta`. Its average Recorded Amount per order is also substantially higher.
- On a daily basis, unique orders decreased by **16.57%** from April to May and by another **4.36%** from May to June. Recorded Amount per day decreased by **11.65%** and **4.54%**, respectively.
- Despite the decline in daily order volume, average Recorded Amount per order increased from **₹670.41** in April to **₹709.96** in May and remained similar at **₹708.63** in June. This suggests that the decline was driven mainly by lower order volume rather than lower order value.
- **94.04%** of non-cancelled orders are single-unit orders.
- B2B represents only **0.71%** of non-cancelled orders, but has a higher average Recorded Amount per order (**₹768.41**) than non-B2B orders (**₹694.01**).
- Amazon fulfilment accounts for **70.93%** of non-cancelled unique orders, while Merchant accounts for **29.07%**.
- Merchant orders have a higher cancellation rate (**17.54%**) than Amazon-fulfilled orders (**12.86%**).
- **Maharashtra** is the leading state with **18,002** non-cancelled unique orders, while **Bengaluru** is the leading city with **9,785**.
- Orders with a recorded Promotion ID represent **70.93%** of non-cancelled orders and have a higher average Recorded Amount per order. However, Promotion ID usage is strongly associated with fulfilment method, so the difference should not be interpreted as a direct promotion effect.
- Quantity and Recorded Amount show a **moderate positive correlation of 0.57**.
- High-value outliers were reviewed using the IQR method. Many high-value orders also contained multiple units, and the amount-per-unit distribution did not provide evidence that these orders were obvious data errors, so the outliers were retained.

### Notes

- `Recorded Amount` should not be interpreted as confirmed revenue or net sales.
- The non-cancelled population includes returned, pending, failed, and other non-final order statuses.
- `No Promotion ID Recorded` does not necessarily mean that no promotion was applied.
- Promotion ID usage is strongly associated with fulfilment method, so observed differences should not be interpreted as causal.
- Correlation indicates association, not causation.
- March contains only one day of data, while June contains 29 days; monthly comparisons therefore use daily averages for months with at least 28 days of coverage.
- The final day in the dataset (**29 June**) shows an unusually low order count and may represent a partial data extract, so end-of-period daily trends should be interpreted with caution.

## SQL Analysis

SQL analysis was performed using PostgreSQL on the cleaned dataset to extend the Python EDA and apply database querying techniques such as CTEs, joins, conditional logic, ranking, and window functions.

Non-cancelled orders were used as the main population for the SQL analysis. The `Amount` field continues to be referred to as **Recorded Amount** rather than confirmed revenue or net sales. Monetary values are reported in **INR (Indian Rupees)**.

### Key Findings

- `Set` was the leading category by Recorded Amount across most geographic labels. The strongest state-category combination was **Maharashtra + Set**, with **6,736 unique orders** and approximately **₹5.76M** in Recorded Amount.
- Among non-cancelled orders, **99.81%** of Merchant-fulfilled orders had a recorded Promotion ID, compared with **59.09%** of Amazon-fulfilled orders. This strong association means Promotion ID differences should not be interpreted as a direct promotion effect.
- Using quartile thresholds calculated during the Python EDA (`Q1 = ₹459`, `Q3 = ₹824`), orders with known Recorded Amount were segmented into Low, Medium, and High Value groups.
- High Value orders represented approximately **25%** of orders with known Recorded Amount but contributed about **41.8%** of Recorded Amount, with an average order value of **₹1,165.30**.
- `Set` contributed **49.85%** of non-cancelled Recorded Amount, while `kurta` contributed **27.10%**. Together, they accounted for approximately **76.95%**.
- The top three categories — `Set`, `kurta`, and `Western Dress` — accounted for approximately **91.20%** of non-cancelled Recorded Amount.
- Maharashtra was the leading state by Recorded Amount for **6 of the 9 product categories**. `Blouse` was led by Karnataka, `Saree` by Tamil Nadu, and `Dupatta` by Telangana.
- The running total of non-cancelled Recorded Amount reached **₹71.67M**, matching the result calculated during the Python analysis and providing an additional validation check.

### Notes

- SQL analysis primarily uses **non-cancelled orders** unless otherwise stated.
- `Recorded Amount` should not be interpreted as confirmed revenue or net sales.
- `No Promotion ID Recorded` does not necessarily mean no promotion was applied.
- Promotion ID usage is strongly associated with fulfilment method, so observed differences should not be interpreted as causal.
- Order value segmentation thresholds were derived from quartiles calculated during the Python EDA rather than selected arbitrarily.
- March and June are partial months in the dataset, so raw monthly totals should not be interpreted as directly comparable full-month performance.
- Geographic labels were normalized for capitalization and whitespace in SQL, but some spelling and abbreviation variants may still remain.
