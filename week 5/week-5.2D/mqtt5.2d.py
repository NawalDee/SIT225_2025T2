import matplotlib
matplotlib.use("Qt5Agg")

import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import ssl
from pymongo import MongoClient
from datetime import datetime

broker = "e13ebf470e3c4a198cdd8d9b62d911b7.s1.eu.hivemq.cloud"
port = 8883
topic = "nawal/gyro"
username = "nawal"
password = "Test1234@"

MONGO_URI = "mongodb+srv://nawalUser:Nawal1234@cluster0.f4cjpdf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["gyroDB"]
collection = db["gyroData"]


x_data, y_data, z_data = [], [], []


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(" Connected to broker")
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")
    else:
        print(" Connection failed with code", rc)

def on_message(client, userdata, msg):
    raw = msg.payload.decode().strip()
    print(" Raw message:", raw)

    try:

        parts = raw.split(",")
        x, y, z = float(parts[0]), float(parts[1]), float(parts[2])


        x_data.append(x)
        y_data.append(y)
        z_data.append(z)


        if len(x_data) > 100:
            x_data.pop(0)
            y_data.pop(0)
            z_data.pop(0)


        doc = {
            "x": x,
            "y": y,
            "z": z,
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(doc)
        print(" Saved to MongoDB:", doc)

    except Exception as e:
        print(" Could not parse:", raw, e)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                     client_id="PythonClient01",
                     protocol=mqtt.MQTTv311)

client.username_pw_set(username, password)
client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)


plt.style.use('ggplot')
fig, ax = plt.subplots()
line_x, = ax.plot([], [], 'r-', label="Gyro X")
line_y, = ax.plot([], [], 'g-', label="Gyro Y")
line_z, = ax.plot([], [], 'b-', label="Gyro Z")
ax.set_xlabel("Samples")
ax.set_ylabel("Rotation (dps)")
ax.legend()

def update(frame):
    if x_data:
        ax.set_xlim(0, len(x_data))
        min_val = min(min(x_data), min(y_data), min(z_data))
        max_val = max(max(x_data), max(y_data), max(z_data))
        ax.set_ylim(min_val - 5, max_val + 5)

        line_x.set_data(range(len(x_data)), x_data)
        line_y.set_data(range(len(y_data)), y_data)
        line_z.set_data(range(len(z_data)), z_data)

    return line_x, line_y, line_z

ani = FuncAnimation(fig, update, interval=500)
client.loop_start()
plt.show()
