from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

uri = "mongodb+srv://nawalUser:Nawal1234@cluster0.f4cjpdf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client["gyroDB"]
collection = db["gyroData"]

docs = list(collection.find({}))
df = pd.DataFrame(docs)
df = df[["x", "y", "z", "timestamp"]]
df.dropna(inplace=True)

df["x"] = pd.to_numeric(df["x"], errors="coerce")
df["y"] = pd.to_numeric(df["y"], errors="coerce")
df["z"] = pd.to_numeric(df["z"], errors="coerce")
df.dropna(inplace=True)

df.to_csv("gyroData_clean.csv", index=False)
print("Data exported and cleaned. Saved to gyroData_clean.csv")

plt.style.use("ggplot")

plt.figure()
plt.plot(df["timestamp"], df["x"], 'r-', label="Gyro X")
plt.xlabel("Time")
plt.ylabel("Rotation (dps)")
plt.title("Gyroscope X")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("gyro_x.png")
plt.close()

plt.figure()
plt.plot(df["timestamp"], df["y"], 'g-', label="Gyro Y")
plt.xlabel("Time")
plt.ylabel("Rotation (dps)")
plt.title("Gyroscope Y")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("gyro_y.png")
plt.close()

plt.figure()
plt.plot(df["timestamp"], df["z"], 'b-', label="Gyro Z")
plt.xlabel("Time")
plt.ylabel("Rotation (dps)")
plt.title("Gyroscope Z")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("gyro_z.png")
plt.close()

plt.figure()
plt.plot(df["timestamp"], df["x"], 'r-', label="Gyro X")
plt.plot(df["timestamp"], df["y"], 'g-', label="Gyro Y")
plt.plot(df["timestamp"], df["z"], 'b-', label="Gyro Z")
plt.xlabel("Time")
plt.ylabel("Rotation (dps)")
plt.title("Gyroscope X, Y, Z Combined")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("gyro_xyz.png")
plt.close()

print("Graphs saved as gyro_x.png, gyro_y.png, gyro_z.png, gyro_xyz.png")
