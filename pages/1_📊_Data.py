import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from paho.mqtt import client as pahoClient
from time import sleep


st.title("Stress Data Analysis")

# Simulate weekly data (bar chart)
st.subheader("Weekly Stress Levels")
weekly_stress = np.random.randint(0, 100, size=7)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
df_weekly = pd.DataFrame({"Day": days, "Stress Level": weekly_stress})
fig_weekly = px.bar(df_weekly, x="Day", y="Stress Level", title="Weekly Stress Overview")
st.plotly_chart(fig_weekly)

# Simulate real-time sensor data (static chart per page refresh)
st.subheader("Real-Time Sensor Data")
sensor_data = pd.DataFrame({
    "Heart Rate": np.random.randint(60, 100, size=50),
    "Skin Conductance": np.random.uniform(0.1, 1.5, size=50),
    "Body Temp": np.random.uniform(36.5, 37.5, size=50)
})
st.line_chart(sensor_data)