import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Load CSV
df = pd.read_csv("dht22_data.csv")

# Convert to numeric
df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")
df["Humidity"] = pd.to_numeric(df["Humidity"], errors="coerce")
df = df.dropna(subset=["Temperature", "Humidity"])

# Train model
X = df["Temperature"].values.reshape(-1, 1)
y = df["Humidity"].values
model = LinearRegression()
model.fit(X, y)

print("Regression slope:", model.coef_[0])
print("Regression intercept:", model.intercept_)

# Create test values between min and max temperature
x_range = np.linspace(X.min(), X.max(), 100)
y_range = model.predict(x_range.reshape(-1, 1))

# Plot scatter + regression line
fig = px.scatter(df, x="Temperature", y="Humidity", opacity=0.7, title="Temperature vs Humidity with Regression Line")
fig.add_traces(go.Scatter(x=x_range, y=y_range, name="Regression Line", line=dict(color="red")))
fig.show()


# Filter scenario 1: temperatures between 10–35 °C
filtered_df = df[(df["Temperature"] >= 10) & (df["Temperature"] <= 35)]

Xf = filtered_df["Temperature"].values.reshape(-1, 1)
yf = filtered_df["Humidity"].values

model_f = LinearRegression()
model_f.fit(Xf, yf)

print("Filtered slope:", model_f.coef_[0])
print("Filtered intercept:", model_f.intercept_)

