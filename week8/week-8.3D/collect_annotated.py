import time
import threading
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
from arduino_iot_cloud import ArduinoCloudClient
from my_secrets import DEVICE_ID, SECRET_KEY
import cv2
from datetime import datetime

# Buffers (rolling)
buffer_x, buffer_y, buffer_z = [], [], []
window_size = 500
sequence_number = 1

client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

def on_x_change(client, value):
    buffer_x.append(value)
    if len(buffer_x) > window_size:
        buffer_x.pop(0)
    print("X:", value)

def on_y_change(client, value):
    buffer_y.append(value)
    if len(buffer_y) > window_size:
        buffer_y.pop(0)
    print("Y:", value)

def on_z_change(client, value):
    buffer_z.append(value)
    if len(buffer_z) > window_size:
        buffer_z.pop(0)
    print("Z:", value)

# Register variables
client.register("accel_x", value=None, on_write=on_x_change)
client.register("accel_y", value=None, on_write=on_y_change)
client.register("accel_z", value=None, on_write=on_z_change)

# Dash app
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Live Smartphone Accelerometer Data with Activity Images"),
    dcc.Graph(id="live-graph"),
    dcc.Interval(id="interval", interval=500, n_intervals=0)  # update twice per second
])

@app.callback(Output("live-graph", "figure"), Input("interval", "n_intervals"))
def update_graph(n):
    min_len = min(len(buffer_x), len(buffer_y), len(buffer_z))
    if min_len == 0:
        return px.line(title="Waiting for data...")

    df = pd.DataFrame({
        "x": buffer_x[-min_len:],
        "y": buffer_y[-min_len:],
        "z": buffer_z[-min_len:]
    })
    fig = px.line(df, y=["x", "y", "z"], title="Accelerometer Readings (Smooth Live)")
    return fig

def start_arduino_client():
    client.start()
    while True:
        client.loop()
        time.sleep(0.1)

def capture_batches():
    global sequence_number
    cap = cv2.VideoCapture(0)
    while True:
        time.sleep(10)
        min_len = min(len(buffer_x), len(buffer_y), len(buffer_z))
        if min_len == 0:
            continue

        #  filenames
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        base_name = f"{sequence_number}_{timestamp}"

        # Save CSV
        df = pd.DataFrame({
            "x": buffer_x[-min_len:],
            "y": buffer_y[-min_len:],
            "z": buffer_z[-min_len:]
        })
        df.to_csv(f"{base_name}.csv", index=False)
        print(f"Saved {base_name}.csv")

        # Capture webcam image
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(f"{base_name}.jpg", frame)
            print(f"Saved {base_name}.jpg")

        sequence_number += 1

if __name__ == "__main__":
    threading.Thread(target=start_arduino_client, daemon=True).start()
    threading.Thread(target=capture_batches, daemon=True).start()
    app.run(debug=True)
