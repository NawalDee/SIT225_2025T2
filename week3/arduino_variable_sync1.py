import sys
import traceback
import random
from arduino_iot_cloud import ArduinoCloudClient
import asyncio
import datetime

DEVICE_ID = "25372bbe-75c6-4975-b8b3-7722e8f0f5c3"
SECRET_KEY = "pjnLhk#TGocuyL4ugktlZFTVS"


def on_temperature_changed(client, value):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_line = f"{timestamp}, {value}\n"

    with open("temperature_data.csv", "a") as file:
        file.write(csv_line)
        file.flush()

    print(f"New temperature: {value} | Saved: {csv_line.strip()}")


def main():
    print("main() function")

    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
    )

    client.register(
        "temperature", value=None,
        on_write=on_temperature_changed
    )

    client.start()


if __name__ == "__main__":
    try:
        main()
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_type, file=print)
