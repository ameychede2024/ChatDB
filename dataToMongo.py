from pymongo import MongoClient
import pandas as pd

# MongoDB Atlas connection details
MONGO_URI = "mongodb+srv://sdharmad:wwXtTxn9MRCyFFgp@clusterchatdb.ntqf3.mongodb.net/?retryWrites=true&w=majority&appName=ClusterChatDB"
DATABASE_NAME = "hr_analytics"
COLLECTION_NAME = "analytics_data"

# Load the CSV file
file_path = "HR_Analytics.csv" 
data = pd.read_csv(file_path)

# Convert the data to a list of dictionaries for MongoDB
records = data.to_dict(orient="records")

# Connect to MongoDB Atlas
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Insert data into MongoDB
try:
    result = collection.insert_many(records)
    print(f"Inserted {len(result.inserted_ids)} records into MongoDB Atlas.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    client.close()
