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
    mood = st.select_slider(
        "Choose your current mood",
        options=['😊 Happy', '🙂 Okay', '😐 Neutral', '😟 Stressed', '😢 Sad'],
        value='😐 Neutral'
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

# --- Info Screen ---
elif menu == "Info":
    st.title("How to Manage Stress")

    st.subheader("Some practical ways to reduce stress:")
    
    # Providing stress management strategies with interactive buttons
    st.write("""
    - **Breathing Exercises**: Try deep breathing to calm your mind.
    - **Physical Activity**: Regular exercise can reduce stress.
    - **Mindfulness**: Practice meditation or yoga.
    """)
    
    # Interactive buttons for more resources
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Breathing Techniques", on_click=lambda: st.write("[Breathing Techniques](https://www.webmd.com/balance/stress-management/stress-relief-breathing-techniques)"))
    with col2:
        st.button("Mindfulness Tips", on_click=lambda: st.write("[Mindfulness Tips](https://www.mindful.org/how-to-practice-mindfulness/)"))
    with col3:
        st.button("Physical Activity Ideas", on_click=lambda: st.write("[Physical Activity](https://www.healthline.com/health/exercise-fitness/best-exercises-to-reduce-stress)"))
    
    st.subheader("For more resources, visit:")
    st.write("[Mental Health Resources](https://www.mentalhealth.org.uk/)")

