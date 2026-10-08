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

- ## Data Inspection

The raw dataset was inspected using Python and Pandas before cleaning.

The inspection included:
- Checking dataset dimensions and column names
- Reviewing data types
- Identifying missing values
- Checking for duplicate rows
- Investigating missing `amount` and `currency` values
- Investigating the relationship between `Fulfilment` and `fulfilled-by`
- Reviewing missing shipping location data
- Investigating missing `Courier Status` values
- Reviewing distributions of key columns such as `Status`, `Category`, `Qty`, and `B2B`
- Generating summary statistics for numeric columns

- ### Key Findings

- The dataset contains 128,975 rows and 24 columns.
- No fully duplicated rows were found.
- `amount` and `currency` share the same missing-value pattern.
- Missing `fulfilled-by` values are structurally related to Amazon-fulfilled orders.
- Shipping location fields are missing together in 33 records.
- Most missing `Courier Status` values are associated with cancelled orders.
- The `Date` column was stored as text and required conversion to datetime.

