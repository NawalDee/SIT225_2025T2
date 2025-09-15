import time
import threading
import pandas as pd
import plotly.express as px
from datetime import datetime
from dash import Dash, dcc, html
from dash.dependencies import Output, Input
from arduino_iot_cloud import ArduinoCloudClient
from my_secrets import DEVICE_ID, SECRET_KEY

# Buffers
buffer_x, buffer_y, buffer_z = [], [], []
batch_size = 200

client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

def on_x_change(client, value):
    buffer_x.append(value)
    print("X:", value)

def on_y_change(client, value):
    buffer_y.append(value)
    print("Y:", value)

def on_z_change(client, value):
    buffer_z.append(value)
    print("Z:", value)

# Register variables
client.register("accel_x", value=None, on_write=on_x_change)
client.register("accel_y", value=None, on_write=on_y_change)
client.register("accel_z", value=None, on_write=on_z_change)

# Dash app
app = Dash(__name__)
app.layout = html.Div([
    html.H1("Live Smartphone Accelerometer Data"),
    dcc.Graph(id="live-graph"),
    dcc.Interval(id="interval", interval=1000, n_intervals=0)
])

latest_fig = px.line()

def data_collector():
    global latest_fig
    while True:
        # Always plot rolling data
        min_len = min(len(buffer_x), len(buffer_y), len(buffer_z))
        if min_len > 0:
            df = pd.DataFrame({
                "x": buffer_x[-min_len:],
                "y": buffer_y[-min_len:],
                "z": buffer_z[-min_len:]
            })
            latest_fig = px.line(df, y=["x", "y", "z"], title="Accelerometer Readings")

        # Save batch to CSV + PNG
        if min_len >= batch_size:
            df_batch = pd.DataFrame({
                "x": buffer_x[:batch_size],
                "y": buffer_y[:batch_size],
                "z": buffer_z[:batch_size]
            })
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            df_batch.to_csv(f"data_{timestamp}.csv", index=False)
            latest_fig.write_image(f"graph_{timestamp}.png")
            print(f"Saved batch: data_{timestamp}.csv, graph_{timestamp}.png")

            # Remove used samples
            del buffer_x[:batch_size]
            del buffer_y[:batch_size]
            del buffer_z[:batch_size]

        time.sleep(1)

@app.callback(Output("live-graph", "figure"), Input("interval", "n_intervals"))
def update_graph(n):
    return latest_fig

def start_arduino_client():
    client.start()
    while True:
        client.loop()
        time.sleep(0.5)

if __name__ == "__main__":
    threading.Thread(target=start_arduino_client, daemon=True).start()
    threading.Thread(target=data_collector, daemon=True).start()
    app.run(debug=True)
