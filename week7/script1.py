import serial
import csv
from datetime import datetime


ser = serial.Serial('/dev/tty.usbmodem14201', 9600)


with open("dht22_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Temperature", "Humidity"])

    while True:
        line = ser.readline().decode("utf-8").strip()
        if "," in line:
            parts = line.split(",")
            if len(parts) == 2:
                temp, hum = parts
                writer.writerow([datetime.now(), temp.strip(), hum.strip()])
                print(f"{datetime.now()}, {temp.strip()}, {hum.strip()}")
            else:
                print("Skipping invalid line:", line)
