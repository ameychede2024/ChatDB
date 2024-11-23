import csv
import mysql.connector
from datetime import datetime

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

def create_coffee_sales_table(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS CoffeeSales (
        transaction_id INT,
        transaction_date DATE,
        transaction_time TIME,
        transaction_qty INT,
        store_id INT,
        store_location VARCHAR(100),
        product_id INT,
        unit_price DECIMAL(10,2),
        product_category VARCHAR(100),
        product_type VARCHAR(100),
        product_detail VARCHAR(100)
    )
    """
    cursor.execute(create_table_query)

def insert_csv_to_mysql(csv_file_path, connection, cursor):
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        
        insert_query = """
        INSERT INTO CoffeeSales 
        (transaction_id, transaction_date, transaction_time, transaction_qty, 
        store_id, store_location, product_id, unit_price, 
        product_category, product_type, product_detail) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for row in csv_reader:
            # Skip empty rows
            if not any(row.values()):
                continue
            
            try:
                # Convert date and time if not empty
                transaction_date = datetime.strptime(row['transaction_date'], '%m/%d/%Y').date() if row['transaction_date'] else None
                transaction_time = datetime.strptime(row['transaction_time'], '%H:%M:%S').time() if row['transaction_time'] else None
                
                # Convert empty strings to None
                processed_row = [
                    int(row['transaction_id']) if row['transaction_id'] else None,
                    transaction_date,
                    transaction_time,
                    int(row['transaction_qty']) if row['transaction_qty'] else None,
                    int(row['store_id']) if row['store_id'] else None,
                    row['store_location'],
                    int(row['product_id']) if row['product_id'] else None,
                    float(row['unit_price']) if row['unit_price'] else None,
                    row['product_category'],
                    row['product_type'],
                    row['product_detail']
                ]
                
                cursor.execute(insert_query, processed_row)
            except Exception as e:
                print(f"Error inserting row: {e}")
        
        connection.commit()
        print(f"Successfully inserted data from {csv_file_path}")

def main(csv_file_path):
    connection, cursor = connect_to_mysql()
    if connection and cursor:
        try:
            create_coffee_sales_table(cursor)
            insert_csv_to_mysql(csv_file_path, connection, cursor)
        finally:
            cursor.close()
            connection.close()

# Usage
if __name__ == "__main__":
    main('coffee_shop_sales.csv')