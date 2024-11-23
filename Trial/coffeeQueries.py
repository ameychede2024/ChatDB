import random
import pandas as pd
import sqlite3
import mysql.connector

# Load spaCy model
# nlp = spacy.load("en_core_web_sm")

# Load CSV data and create SQLite database
# file_path = "/content/Retails.csv"
# data = pd.read_csv(file_path, encoding='ISO-8859-1')
# conn = sqlite3.connect(":memory:")
# data.to_sql("OnlineRetail", conn, if_exists="replace", index=False)


def connect_to_mysql(host='localhost', user='shardul', password='password', database='CHATDB'):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection, connection.cursor()
    except mysql.connector.Error as err:
        print(f"MySQL Connection Error: {err}")
        return None, None
    
# Pattern detection
def detect_pattern(user_input):
    user_input = user_input.lower()

    if "total sales" in user_input and "product" in user_input:
        return "total_sales_by_product"
    elif "purchases" in user_input and "quantity greater" in user_input:
        return "purchases_where_quantity_greater"
    elif "total quantity" in user_input and "country" in user_input:
        return "total_quantity_by_country"
    elif "average price" in user_input and "product" in user_input:
        return "average_price_by_product"
    elif "unique customers" in user_input and "country" in user_input:
        return "unique_customers_by_country"
    elif "top" in user_input and "products" in user_input:
        return "top_products_by_sales"
    elif "total quantity" in user_input and "date" in user_input:
        return "total_quantity_on_date"
    elif "purchases" in user_input and "customer" in user_input:
        return "purchases_by_customer"
    elif "example" in user_input and "group by" in user_input:
        return "example_grp_by"
    else:
        return "example"

# Query generation
def generate_query(pattern, params):

    if pattern == "example":
        rnd = random.randint(0, 9)
        if "groupby" in user_input:
            print("No group by queries.")  
        else:
            sql_queries = [
                "SELECT * FROM CoffeeSales WHERE store_location = 'Lower Manhattan';",
                "SELECT * FROM CoffeeSales WHERE product_category = 'Coffee';",
                "SELECT * FROM CoffeeSales WHERE transaction_date = '1/1/2023';",
                "SELECT * FROM CoffeeSales WHERE transaction_qty > 2;",
                "SELECT * FROM CoffeeSales WHERE unit_price > 3.00;",
                "SELECT * FROM CoffeeSales WHERE product_type = 'Organic brewed coffee';",
                "SELECT * FROM CoffeeSales WHERE product_id = 79;",
                "SELECT * FROM CoffeeSales WHERE transaction_time LIKE '8:%';",
                "SELECT * FROM CoffeeSales WHERE product_detail LIKE '%Green Tea%';",
                "SELECT * FROM CoffeeSales WHERE unit_price BETWEEN 2.00 AND 4.00;"
            ]
            return {"SQL": sql_queries[rnd], "MongoDB": None}
    elif pattern == "total_sales_by_product":
        sql_query = "SELECT Description, SUM(Quantity * UnitPrice) AS TotalSales FROM OnlineRetail GROUP BY Description;"
        mongo_query = {
            "$group": { "_id": "$Description", "totalSales": { "$sum": { "$multiply": ["$Quantity", "$UnitPrice"] } } }
        }
        return {"SQL": sql_query, "MongoDB": mongo_query}

    elif pattern == "purchases_where_quantity_greater":
        quantity = params.get("quantity", 1)
        sql_query = f"SELECT * FROM OnlineRetail WHERE Quantity > {quantity};"
        mongo_query = { "$match": { "Quantity": { "$gt": quantity } } }
        return {"SQL": sql_query, "MongoDB": mongo_query}

    elif pattern == "total_quantity_by_country":
        sql_query = "SELECT Country, SUM(Quantity) AS TotalQuantity FROM OnlineRetail GROUP BY Country;"
        mongo_query = {
            "$group": { "_id": "$Country", "totalQuantity": { "$sum": "$Quantity" } }
        }
        return {"SQL": sql_query, "MongoDB": mongo_query}

    elif pattern == "average_price_by_product":
        sql_query = "SELECT Description, AVG(UnitPrice) AS AveragePrice FROM OnlineRetail GROUP BY Description;"
        mongo_query = {
            "$group": { "_id": "$Description", "averagePrice": { "$avg": "$UnitPrice" } }
        }
        return {"SQL": sql_query, "MongoDB": mongo_query}

    elif pattern == "unique_customers_by_country":
        sql_query = "SELECT Country, COUNT(DISTINCT CustomerID) AS UniqueCustomers FROM OnlineRetail GROUP BY Country;"
        mongo_query = {
            "$group": { "_id": "$Country", "uniqueCustomers": { "$addToSet": "$CustomerID" } }
        }
        return {"SQL": sql_query, "MongoDB": mongo_query}

    elif pattern == "top_products_by_sales":
        limit = params.get("limit", 5)  # Default to top 5 products
        sql_query = f"SELECT Description, SUM(Quantity * UnitPrice) AS TotalSales FROM OnlineRetail GROUP BY Description ORDER BY TotalSales DESC LIMIT {limit};"
        mongo_query = [
            { "$group": { "_id": "$Description", "totalSales": { "$sum": { "$multiply": ["$Quantity", "$UnitPrice"] } } } },
            { "$sort": { "totalSales": -1 } },
            { "$limit": limit }
        ]
        return {"SQL": sql_query, "MongoDB": mongo_query}

    elif pattern == "total_quantity_on_date":
        date = params.get("date", "2010-12-01")
        sql_query = f"SELECT SUM(Quantity) AS TotalQuantity FROM OnlineRetail WHERE DATE(InvoiceDate) = '{date}';"
        mongo_query = [
            { "$match": { "InvoiceDate": date } },
            { "$group": { "_id": None, "totalQuantity": { "$sum": "$Quantity" } } }
        ]
        return {"SQL": sql_query, "MongoDB": mongo_query}

    elif pattern == "purchases_by_customer":
        customer_id = params.get("customer_id", 17850)
        sql_query = f"SELECT * FROM OnlineRetail WHERE CustomerID = {customer_id};"
        mongo_query = { "$match": { "CustomerID": customer_id } }
        return {"SQL": sql_query, "MongoDB": mongo_query}

    return None

def run_sql_query(sql_query,cursor):
    cursor.execute(sql_query)
    results = cursor.fetchall()
    return results

# Main processing function
def process_user_input(user_input):
    # Detect pattern
    pattern = detect_pattern(user_input)
    if not pattern:
        return "No matching pattern found."

    # Extract parameters
    params = {}
    if "quantity greater" in user_input:
        quantity = int(user_input.split("greater than")[-1].strip())
        params["quantity"] = quantity
    elif "top" in user_input:
        limit = int(user_input.split("top")[-1].split()[0].strip())
        params["limit"] = limit
    elif "date" in user_input:
        date = user_input.split("date")[-1].strip()
        params["date"] = date
    elif "customer" in user_input:
        customer_id = int(user_input.split("customer")[-1].strip())
        params["customer_id"] = customer_id

    # Generate and execute query
    generated_query = generate_query(pattern, params)
    if generated_query and "SQL" in generated_query:
        sql_query = generated_query["SQL"]

        connection, cursor = connect_to_mysql()
        if connection and cursor:
            try:
                result = run_sql_query(sql_query,cursor);
            finally:
                cursor.close()
                connection.close()
        return sql_query, result
    
    return generated_query

# Test the system with an example input
user_input = "Example Query"
sql_query, result = process_user_input(user_input)

# Display the result
print("Generated SQL Query:\n", sql_query)
print("\nQuery Result:")
print(result)