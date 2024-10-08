import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set the page layout to wide for better UI/UX
st.set_page_config(layout="wide", page_title="Stress Monitor", page_icon="🧘‍♀️")

# Sidebar Navigation
menu = st.sidebar.radio("Navigation", ["Main", "Data", "Info"])

# Functions to simulate sensor readings (for demo)
def get_sensor_data():
    heart_rate = np.random.randint(60, 100)
    skin_conductance = np.random.uniform(0.1, 1.5)
    body_temp = np.random.uniform(36.5, 37.5)
    return heart_rate, skin_conductance, body_temp

# --- Main Screen ---
if menu == "Main":
    st.title("Welcome to the Stress Monitoring Application")
    
    st.subheader("How are you feeling today?")
    
    # Emoji slider for user to input their current feeling
    mood = st.slider(
        "Mood", min_value=0, max_value=10, value=5,
        format="😖  😟  😐  🙂  😃"
    )

    # Displaying sensor readings with icons
    st.subheader("Your current physiological readings:")
    heart_rate, skin_conductance, body_temp = get_sensor_data()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Heart Rate ❤️", value=f"{heart_rate} bpm")
    with col2:
        st.metric(label="Skin Conductance 💧", value=f"{skin_conductance:.2f} µS")
    with col3:
        st.metric(label="Body Temperature 🌡️", value=f"{body_temp:.2f} °C")
    
    # Stress percentage radial bar (placeholder calculation)
    stress_prediction = np.clip(mood + np.random.randint(0, 5), 0, 100)
    st.subheader(f"Predicted Stress Level: {stress_prediction}%")
    st.progress(stress_prediction / 100)

    # Link to stress management info
    st.button("Need help managing stress?", key="info_link", on_click=lambda: st.sidebar.radio("Navigation", ["Info"]))

# --- Data Screen ---
elif menu == "Data":
    st.title("Stress Data Analysis")

    # Simulate weekly data (bar chart)
    st.subheader("Weekly Stress Levels")
    weekly_stress = np.random.randint(0, 100, size=7)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    df_weekly = pd.DataFrame({"Day": days, "Stress Level": weekly_stress})
    fig_weekly = px.bar(df_weekly, x="Day", y="Stress Level", title="Weekly Stress
