import serial
import time
import csv

# Open COM5 at 9600 baud (must match your Arduino code)
ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)  # wait for the connection

# Create a CSV file to save the data
with open("gyro_data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "X", "Y", "Z"])  # headers

    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            data = line.split(",")  # expecting: x,y,z
            if len(data) == 3:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                writer.writerow([timestamp, data[0], data[1], data[2]])
                print(timestamp, data)
