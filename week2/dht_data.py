import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
data = pd.read_csv("dht_data.csv")

# Create a time index (assuming 2 seconds between readings)
data["Time(s)"] = [i * 2 for i in range(len(data))]

# Plot Temperature
plt.figure()
plt.plot(data["Time(s)"], data["Temperature(°C)"], marker='o')
plt.title("Temperature vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Temperature (°C)")
plt.grid(True)
plt.savefig("temperature_plot.png")  # <-- saves PNG

# Plot Humidity
plt.figure()
plt.plot(data["Time(s)"], data["Humidity(%)"], marker='o', color='green')
plt.title("Humidity vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Humidity (%)")
plt.grid(True)
plt.savefig("humidity_plot.png")  # <-- saves PNG

plt.show()
