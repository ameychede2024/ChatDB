import pandas as pd

customers = pd.read_csv("Write/Customers.csv")
orders = pd.read_csv("Write/Orders.csv")
products = pd.read_csv("Write/Products.csv")

ids = customers["Customer ID"]
uids = pd.unique(ids)
print(len(ids))
print(len(uids))

ids = products["Product ID"]
uids = pd.unique(ids)
print(len(ids))
print(len(uids))