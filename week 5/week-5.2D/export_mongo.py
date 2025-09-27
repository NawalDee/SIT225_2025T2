from pymongo import MongoClient
import pandas as pd


uri = "mongodb+srv://nawalUser:Nawal1234@cluster0.f4cjpdf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

db = client["gyroDB"]
collection = db["gyroData"]


cursor = collection.find({})
data = list(cursor)


df = pd.DataFrame(data)

# SaveCSV
df.to_csv("gyro_data.csv", index=False)
print(" Data exported to gyro_data.csv")
