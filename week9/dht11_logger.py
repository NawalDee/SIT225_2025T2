import serial
import csv
from datetime import datetime


PORT = "/dev/cu.usbmodem14101"
BAUD_RATE = 9600
ser = serial.Serial(PORT, BAUD_RATE)

# create CSV
with open("elderly_monitor_log.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "temperature", "humidity", "pir", "distance", "alert"])
    print("Logging started... (Ctrl+C to stop)")

    try:
        while True:
            line = ser.readline().decode("utf-8").strip()
            if "Temp:" in line and "Humidity:" in line:

                parts = line.replace("°C", "").replace("%", "").replace("cm", "").replace(",", "").split()
                if len(parts) >= 10:
                    temp = float(parts[1])
                    hum = float(parts[3])
                    pir = int(parts[5])
                    dist = float(parts[7])
                    alert = int(parts[9])
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    #  CSV
                    writer.writerow([timestamp, temp, hum, pir, dist, alert])
                    print(f"{timestamp} | Temp: {temp} °C | Hum: {hum} % | PIR: {pir} | Distance: {dist} cm | Alert: {alert}")
    except KeyboardInterrupt:
        print("Logging stopped.")
        ser.close()
