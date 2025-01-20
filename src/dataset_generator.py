import random
import pandas as pd
from datetime import datetime, timedelta

# Set seed for reproducibility
random.seed(42)

# Define constants
num_customers = 500
num_products = 50
num_records = 5000

# Sample data for customers, products, and categories
customer_ids = [f"C{str(i).zfill(3)}" for i in range(1, num_customers + 1)]
product_ids = [f"P{str(i).zfill(3)}" for i in range(1, num_products + 1)]
product_categories = [
    "Electronics", "Furniture", "Clothing", "Books", "Grocery", 
    "Beauty", "Kitchen", "Sports", "Appliances"
]

# Generate synthetic purchase amounts (randomly within some realistic range)
purchase_amounts = {
    "Electronics": (100, 1000),
    "Furniture": (50, 500),
    "Clothing": (10, 200),
    "Books": (5, 50),
    "Grocery": (1, 100),
    "Beauty": (10, 100),
    "Kitchen": (20, 300),
    "Sports": (20, 500),
    "Appliances": (50, 2000)
}

# Generate random purchase dates over a period of 30 days
start_date = datetime(2024, 12, 1)
end_date = datetime(2025, 1, 1)

# Function to generate a random purchase date
def random_purchase_date():
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# Create a list to store the records
records = []

# Generate 5000 purchase records
for _ in range(num_records):
    customer_id = random.choice(customer_ids)
    product_id = random.choice(product_ids)
    product_category = random.choice(product_categories)
    purchase_date = random_purchase_date().strftime('%Y-%m-%d')
    
    # Get a random purchase amount for the product category
    min_amount, max_amount = purchase_amounts[product_category]
    purchase_amount = round(random.uniform(min_amount, max_amount), 2)
    
    # Add the record to the list
    records.append([customer_id, product_id, product_category, purchase_amount, purchase_date])

# Create a DataFrame from the records
df = pd.DataFrame(records, columns=["Customer ID", "Product ID", "Product Category", "Purchase Amount", "Purchase Date"])

fileName = "purchase_data.csv"

# Save the dataset to a CSV file
df.to_csv(fileName, index=False)

print(f"Synthetic dataset generated and saved as '{fileName}'")