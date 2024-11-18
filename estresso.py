import streamlit as st
import numpy as np

@st.cache_data
def get_sensor_data():
    heart_rate = np.random.randint(60, 100)
    skin_conductance = np.random.uniform(1, 100)
    body_temp = np.random.uniform(36.5, 37.5)
    return heart_rate, skin_conductance, body_temp

def calculate_stress_prediction(mood):
    mood_to_stress_range = {
        '😊 Happy': (0, 20),
        '🙂 Okay': (20, 40),
        '😐 Neutral': (40, 60),
        '😟 Stressed': (70, 100),
        '😢 Sad': (60, 80)
    }
    stress_min, stress_max = mood_to_stress_range[mood]
    return np.random.randint(stress_min, stress_max)

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
    st.metric(label="Skin Conductance 💧", value=f"{skin_conductance:.2f} %")
with col3:
    st.metric(label="Body Temperature 🌡️", value=f"{body_temp:.2f} °C")

# Stress percentage radial bar (based on mood)
stress_prediction = calculate_stress_prediction(mood)
st.subheader(f"Predicted Stress Level: {stress_prediction}%")
st.progress(stress_prediction / 100)

# Link to stress management info
st.button("Need help managing stress?", key="info_link")
