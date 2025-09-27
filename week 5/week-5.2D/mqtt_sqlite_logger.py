import paho.mqtt.client as mqtt
import ssl
import sqlite3
from datetime import datetime

broker = "e13ebf470e3c4a198cdd8d9b62d911b7.s1.eu.hivemq.cloud"
port = 8883
topic = "nawal/gyro"
username = "nawal"
password = "Test1234@"

conn = sqlite3.connect("gyroData2.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS gyroData2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    x REAL,
    y REAL,
    z REAL,
    timestamp TEXT
)
""")
conn.commit()

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(topic)
    else:
        print("Connection failed with code", rc)

def on_message(client, userdata, msg):
    raw = msg.payload.decode().strip()
    print("Raw message:", raw)
    try:
        parts = raw.split(",")
        x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
        ts = datetime.utcnow().isoformat()
        cursor.execute(
            "INSERT INTO gyroData2 (x, y, z, timestamp) VALUES (?, ?, ?, ?)",
            (x, y, z, ts)
        )
        conn.commit()
        print(f"Saved to SQLite: {x}, {y}, {z}, {ts}")
    except Exception as e:
        print("Could not parse:", raw, e)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                     client_id="PythonClient02",
                     protocol=mqtt.MQTTv311)
client.username_pw_set(username, password)
client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)

print("Starting MQTT loop, saving to SQLite...")
client.loop_forever()
