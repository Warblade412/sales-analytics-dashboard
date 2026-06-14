# Sales Analytics Dashboard

A resume-ready data analytics project built with Python, Pandas, Streamlit, and Plotly. The dashboard analyzes a realistic 12,000-row sales dataset and turns raw transaction data into interactive business insights.

## Project Overview

This project simulates sales data for an e-commerce/business environment and provides a clean dashboard for exploring revenue, profit, monthly growth, product performance, and regional trends. It is designed to be easy to explain in interviews while still showing practical data cleaning, analysis, and dashboard development skills.

## Tech Stack

- Python
- Pandas
- Streamlit
- Plotly
- Matplotlib

## Features

- Loads sales data from `data.csv`
- Cleans and preprocesses the dataset
- Handles missing values
- Converts date fields to datetime format
- Removes duplicate records
- Filters by date range, product category, region, and customer type
- Displays key metrics including total revenue, average order revenue, total profit, profit margin, and monthly growth
- Visualizes monthly revenue trends with a line chart
- Shows category revenue distribution with a pie chart
- Compares top product categories and regional performance with bar charts
- Displays a top-products table for deeper business analysis

## How to Run Locally

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Optional: regenerate the dataset:

```bash
python generate_data.py
```

4. Start the Streamlit app:

```bash
streamlit run app.py
```

5. Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Dataset Columns

- `Date`: Sales transaction date
- `Product_Category`: Product category sold
- `Product`: Specific product name
- `Region`: Sales region
- `Customer_Type`: Customer segment
- `Units_Sold`: Number of units sold
- `Unit_Price`: Unit sale price
- `Revenue`: Total transaction revenue
- `Profit`: Estimated transaction profit

