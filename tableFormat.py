import pandas as pd

orders_path = "orders.csv"
products_path = "product-supplier.csv"

orders = pd.read_csv(orders_path)
products = pd.read_csv(products_path)

unique_custs = orders.dropna(subset=["Customer ID"]).drop_duplicates(subset=["Customer ID"])
customers = pd.DataFrame({
    "Customer ID": unique_custs["Customer ID"].astype(int),
    "Customer Status": unique_custs["Customer Status"]
})

orders.drop(columns=["Cost Price Per Unit","Customer Status"], inplace=True)

customers.to_csv("Write/Customers.csv",index=False)
products.to_csv("Write/Products.csv",index=False)
orders.to_csv("Write/Orders.csv",index=False)




# List all the customers with Gold Status
# SELECT customer_name FROM Customer WHERE Customer Stutus = GOLD

# Number of GOLD SILVER Platinum Customers
# SELECT COUNT(Customer_ID)

# Orders with greater lesser quantity

# 