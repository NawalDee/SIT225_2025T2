import pandas as pd
import matplotlib.pyplot as plt


data = pd.read_csv("elderly_monitor_log.csv")
data["timestamp"] = pd.to_datetime(data["timestamp"])


print(" Average Temperature:", data["temperature"].mean())
print(" Average Humidity:", data["humidity"].mean())
print(" Total Alerts:", data["alert"].sum())
print(" Motion Detections (PIR=1):", (data["pir"] == 1).sum())


plt.figure(figsize=(10,5))
plt.plot(data["timestamp"], data["temperature"], label="Temperature (°C)")
plt.plot(data["timestamp"], data["humidity"], label="Humidity (%)")
plt.xlabel("Time")
plt.ylabel("Value")
plt.title("Temperature & Humidity Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10,5))
plt.plot(data["timestamp"], data["distance"], label="Distance (cm)", color="orange")
plt.xlabel("Time")
plt.ylabel("Distance (cm)")
plt.title("Ultrasonic Distance Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


plt.figure(figsize=(10,5))
plt.plot(data["timestamp"], data["alert"], label="Alerts", color="red")
plt.xlabel("Time")
plt.ylabel("Alert (0=Safe, 1=Triggered)")
plt.title("Alert Events Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
