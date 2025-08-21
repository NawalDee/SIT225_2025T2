import matplotlib
# Use Qt5Agg backend (doesn't need Tkinter)
matplotlib.use('Qt5Agg')

import serial
import time
import matplotlib.pyplot as plt
from collections import deque

# === Serial setup ===
ser = serial.Serial('COM5', 9600)  # Adjust COM port if needed
time.sleep(2)

# Store only the latest 100 points to avoid memory overload
timestamps = deque(maxlen=100)
x_vals = deque(maxlen=100)
y_vals = deque(maxlen=100)
z_vals = deque(maxlen=100)

# === Create separate figures ===
plt.ion()
fig1, ax1 = plt.subplots()
fig2, ax2 = plt.subplots()
fig3, ax3 = plt.subplots()
fig4, ax4 = plt.subplots()

print("Reading from Arduino and plotting live...")

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            try:
                x, y, z = line.split(",")
                x, y, z = float(x), float(y), float(z)

                t = time.time()
                timestamps.append(t)
                x_vals.append(x)
                y_vals.append(y)
                z_vals.append(z)

                # === Plot X ===
                ax1.clear()
                ax1.plot(timestamps, x_vals, label="X-axis", color='r')
                ax1.set_title("Gyro X (deg/s)")
                ax1.set_xlabel("Time")
                ax1.set_ylabel("X")
                ax1.legend()

                # === Plot Y ===
                ax2.clear()
                ax2.plot(timestamps, y_vals, label="Y-axis", color='g')
                ax2.set_title("Gyro Y (deg/s)")
                ax2.set_xlabel("Time")
                ax2.set_ylabel("Y")
                ax2.legend()

                # === Plot Z ===
                ax3.clear()
                ax3.plot(timestamps, z_vals, label="Z-axis", color='b')
                ax3.set_title("Gyro Z (deg/s)")
                ax3.set_xlabel("Time")
                ax3.set_ylabel("Z")
                ax3.legend()

                # === Combined XYZ ===
                ax4.clear()
                ax4.plot(timestamps, x_vals, label="X", color='r')
                ax4.plot(timestamps, y_vals, label="Y", color='g')
                ax4.plot(timestamps, z_vals, label="Z", color='b')
                ax4.set_title("Gyro XYZ (deg/s)")
                ax4.set_xlabel("Time")
                ax4.set_ylabel("Values")
                ax4.legend()

                plt.pause(0.01)
            except Exception as e:
                print("Invalid line:", line, "| Error:", e)

except KeyboardInterrupt:
    print("Stopped by user.")
    ser.close()
