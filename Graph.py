import pandas as pd
import plotly.express as px

millibar_offset = -1000
time_offset = -12.863

# ---- File paths ----
file1 = "Brain_ballast_v2.0test1"
file2 = "BrainBallast.csv"

# ---- Load data ----
df1 = pd.read_csv(file1, delimiter="\t")
df2 = pd.read_csv(file2, header=None)
df2.columns = ["Pressure_mbar", "Temperature_C", "Col3", "Col4", "Col5", "Milliseconds"]

# ---- Adjust baseline ----
df2["Adj_Pressure_mbar"] = df2["Pressure_mbar"] + millibar_offset
df2["Adj_Pressure_psi"] = df2["Adj_Pressure_mbar"] * 0.0145038

# ---- Time alignment ----
df1["Time_ms"] = (df1["Time (sec)"] * 1000).astype(int)
df1["Aligned_Time_ms"] = df1["Time_ms"] - df1["Time_ms"].iloc[0]
df2["Aligned_Time_ms"] = df2["Milliseconds"] - df2["Milliseconds"].iloc[0]
df2["Aligned_Time_ms"] = df2["Aligned_Time_ms"] + int(time_offset * 1000)

# ---- Prepare for Plotly ----
plot_data = pd.DataFrame({
    "Time (s)": pd.concat([
        df1["Aligned_Time_ms"]/1000,
        df1["Aligned_Time_ms"]/1000,
        df2["Aligned_Time_ms"]/1000
    ]),
    "Pressure (psi)": pd.concat([
        df1["Top Pore Pressure (psi)"],
        df1["Bottom Pore Pressure (psi)"],
        df2["Adj_Pressure_psi"]
    ]),
    "Source": (["Top Pore Pressure"] * len(df1)
              + ["Bottom Pore Pressure"] * len(df1)
              + ["Pressure Brain Ballast"] * len(df2))
})

# ---- Interactive Plot ----
fig = px.line(plot_data, x="Time (s)", y="Pressure (psi)", color="Source",
              title="Interactive Pressure Comparison")
fig.write_html("my_plot.html")
fig.show()
