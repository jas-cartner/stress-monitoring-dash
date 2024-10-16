import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from paho.mqtt import client as pahoClient
from time import sleep

# Set the page layout to wide for better UI/UX
st.set_page_config(layout="wide", page_title="Stress Monitor", page_icon="🧘‍♀️")

st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        margin: 5px 0;
        padding: 10px;
        background-color: #A0A0A0; /* Button color */
        color: white;
        border: none;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigation with Radio Buttons
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Main", "Data", "Info", "MQTT"])

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
    stress_prediction = np.clip(np.random.randint(0, 5), 0, 100)
    st.subheader(f"Predicted Stress Level: {stress_prediction}%")
    st.progress(stress_prediction / 100)

    # Link to stress management info
    st.button("Need help managing stress?", key="info_link")

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
        st.link_button("Breathing Techniques","https://www.webmd.com/balance/stress-management/stress-relief-breathing-techniques")
    with col2:
        st.link_button("Mindfulness Tips","https://www.mindful.org/how-to-practice-mindfulness/")
    with col3:
        st.link_button("Physical Activity Ideas", "(https://www.healthline.com/health/exercise-fitness/best-exercises-to-reduce-stress")
    
    st.subheader("For more resources, visit:")
    st.write("[Mental Health Resources](https://www.mentalhealth.org.uk/)")

elif menu == "MQTT":
    st.title("MQTT Testing")

    # requirement to have mosquitto running as the MQTT broker - if not already running in background
    # "".\mosquiitto.exe -v" in the file location "C:\Program Files\mosquitto"

    broker = 'raspberrypi.local'
    port = 1883
    topic = "python/mqtt"
    # Generate a Client ID with the subscribe prefix.
    client_id = f'subscribe-10'
    username = 'estresso'
    password = 'UTS'

    MQTT_message = "test"
    con_message = "test"

    client = pahoClient.Client(client_id=client_id,callback_api_version=pahoClient.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)

    st.subheader("Connection message")
    if client.connect(broker, port) != 0:
        con_message = "Failed to connect"
    else:
        con_message = "Connected"
    st.text(con_message)

    st.subheader("MQTT message")
    MQTT_textbox = st.empty()
    st.subheader("Current readings from the rPi:")
    MQTT_display = st.empty()
    if con_message == "Connected":
        def on_message(client, userdata, msg):
            global MQTT_message
            MQTT_message = msg.payload.decode()

        client.subscribe(topic)
        client.on_message = on_message
        
        heart_rate = 0
        skin_conductance = 0
        body_temp = 0

        while(True):
            client.loop()
            MQTT_textbox.text(MQTT_message)
            MQTTarr = MQTT_message.split(",")
            if(len(MQTTarr) == 3):
                heart_rate = int(MQTTarr[0])
                skin_conductance = float(MQTTarr[1])
                body_temp = float(MQTTarr[2])

            col1, col2, col3 = MQTT_display.columns(3)
            with col1:
                st.metric(label="Heart Rate ❤️", value=f"{heart_rate} bpm")
            with col2:
                st.metric(label="Skin Conductance 💧", value=f"{skin_conductance:.2f} µS")
            with col3:
                st.metric(label="Body Temperature 🌡️", value=f"{body_temp:.2f} °C")

            sleep(1)

