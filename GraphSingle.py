import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

millibar_offset = -1000 + 37
time_offset = 0

file = "data.txt"

df = pd.read_csv(file, header=None)
df.columns = ["Pressure_mbar", "Temperature_C", "Col3", "Col4", "Col5", "Milliseconds"]

df["Adj_Pressure_mbar"] = df["Pressure_mbar"] + millibar_offset
df["Adj_Pressure_psi"] = df["Adj_Pressure_mbar"] * 0.0145038

df["Aligned_Time_ms"] = df["Milliseconds"] - df["Milliseconds"].iloc[0]
df["Aligned_Time_ms"] = df["Aligned_Time_ms"] + int(time_offset * 1000)
df["Time_s"] = df["Aligned_Time_ms"] / 1000

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(x=df["Time_s"], y=df["Adj_Pressure_psi"],
               mode='lines', name='Pressure (psi)',
               line=dict(color='blue')),
    secondary_y=False
)

fig.add_trace(
    go.Scatter(x=df["Time_s"], y=df["Adj_Pressure_mbar"],
               mode='lines', name='Pressure (mbar)',
               line=dict(color='red')),
    secondary_y=True
)

# Update axes labels
fig.update_xaxes(title_text="Time (s)")
fig.update_yaxes(title_text="Pressure (psi)", secondary_y=False)
fig.update_yaxes(title_text="Pressure (mbar)", secondary_y=True)

# Update layout
fig.update_layout(
    title_text=f"Pressure over Time (Time offset: {time_offset}s, mbar offset: {millibar_offset})",
    hovermode='x unified'
)

fig.write_html("my_plot.html")
fig.show()