import pandas as pd
import plotly.graph_objects as go

millibar_offset = -1000
time_skip_seconds = 1700  # Skip first 1700 seconds

# ---- Load data ----
df = pd.read_csv("data.txt", header=None)
df.columns = ["Pressure_mbar", "Temperature_C", "Col3", "Col4", "Col5", "Milliseconds"]

# ---- Adjust baseline ----
df["Adj_Pressure_mbar"] = df["Pressure_mbar"] + millibar_offset
df["Adj_Pressure_psi"] = df["Adj_Pressure_mbar"] * 0.0145038

# ---- Time alignment (convert to seconds, starting from 0) ----
df["Time_s"] = (df["Milliseconds"] - df["Milliseconds"].iloc[0]) / 1000

# ---- Skip first 1700 seconds ----
df = df[df["Time_s"] >= time_skip_seconds].reset_index(drop=True)

# ---- Reset time to start at 0 after skipping ----
df["Time_s"] = df["Time_s"] - df["Time_s"].iloc[0]

# ---- Interactive Plot with custom hover ----
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Time_s"],
    y=df["Adj_Pressure_psi"],
    mode='lines',
    name='Pressure Brain Ballast',
    customdata=df[["Adj_Pressure_mbar", "Temperature_C"]],
    hovertemplate=(
        '<b>Time:</b> %{x:.3f} s<br>' +
        '<b>Pressure:</b> %{y:.4f} psi<br>' +
        '<b>Pressure:</b> %{customdata[0]:.2f} mbar<br>' +
        '<b>Temperature:</b> %{customdata[1]:.2f} °C<br>' +
        '<extra></extra>'
    )
))

fig.update_layout(
    title="Pressure Data from Brain Ballast (Starting at 1700s)",
    xaxis_title="Time (s)",
    yaxis_title="Pressure (psi)",
    hovermode='closest'
)

fig.write_html("my_plot.html")
fig.show()