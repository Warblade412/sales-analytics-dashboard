import csv
import random
from datetime import date, timedelta


random.seed(42)

categories = {
    "Electronics": ["Laptop", "Tablet", "Smartphone", "Headphones", "Smartwatch"],
    "Clothing": ["Jacket", "Sneakers", "Jeans", "T-Shirt", "Dress"],
    "Home & Garden": ["Cookware Set", "Office Chair", "Garden Tools", "Bedding Set", "Lamp"],
    "Sports": ["Yoga Mat", "Tennis Racket", "Running Shoes", "Bike Helmet", "Dumbbell Set"],
    "Beauty": ["Skin Care Kit", "Fragrance", "Hair Dryer", "Makeup Palette", "Face Serum"],
}

regions = ["North", "South", "East", "West", "Central"]
customer_types = ["Retail", "Wholesale", "Direct"]
start_date = date(2022, 1, 1)
end_date = date(2023, 12, 31)
days_in_range = (end_date - start_date).days
n_records = 12000
rows = []

for _ in range(n_records):
    product_category = random.choice(list(categories.keys()))
    product = random.choice(categories[product_category])
    region = random.choice(regions)
    units_sold = random.randint(1, 99)
    unit_price = round(random.uniform(10, 500), 2)
    revenue = units_sold * unit_price

    # Add regional revenue differences to make the analysis more realistic.
    if region == "North":
        revenue *= 1.20
    elif region == "South":
        revenue *= 0.95
    elif region == "West":
        revenue *= 1.10

    profit = revenue * random.uniform(0.15, 0.45)

    rows.append(
        {
            "Date": start_date + timedelta(days=random.randint(0, days_in_range)),
            "Product_Category": product_category,
            "Product": product,
            "Region": region,
            "Customer_Type": random.choice(customer_types),
            "Units_Sold": units_sold,
            "Unit_Price": unit_price,
            "Revenue": round(revenue, 2),
            "Profit": round(profit, 2),
        }
    )

# Add controlled data quality issues to demonstrate dashboard preprocessing.
for index in random.sample(range(len(rows)), int(0.02 * len(rows))):
    rows[index]["Profit"] = ""
rows.extend(random.sample(rows, 50))
rows.sort(key=lambda row: row["Date"])

with open("data.csv", "w", newline="") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print(f"Dataset created successfully with {len(rows)} records")
print("First few rows:")
for row in rows[:5]:
    print(row)
