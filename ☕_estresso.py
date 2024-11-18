# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# from paho.mqtt import client as pahoClient
# from time import sleep
# st.title("Welcome to the Stress Monitoring Application!")
    


# # requirement to have mosquitto running as the MQTT broker - if not already running in background
# # "".\mosquiitto.exe -v" in the file location "C:\Program Files\mosquitto"

# broker = 'raspberrypi.local'
# port = 1883
# topic = "python/mqtt"
# # Generate a Client ID with the subscribe prefix.
# client_id = f'subscribe-10'
# username = 'estresso'
# password = 'UTS'

# MQTT_message = "test"
# con_message = "test"

# client = pahoClient.Client(client_id=client_id,callback_api_version=pahoClient.CallbackAPIVersion.VERSION2)
# client.username_pw_set(username, password)

# st.subheader("Connection message")
# if client.connect(broker, port) != 0:
#     con_message = "Failed to connect"
# else:
#     con_message = "Connected"
# st.text(con_message)


# MQTT_textbox = st.empty()

# st.subheader("How are you feeling today?")
# mood = st.select_slider(
#         "Choose your current mood",
#         options=['😊 Happy', '🙂 Okay', '😐 Neutral', '😟 Stressed', '😢 Sad'],
#         value='😐 Neutral'
#     )

# MQTT_display = st.empty()
# if con_message == "Connected":
#     def on_message(client, userdata, msg):
#         global MQTT_message
#         MQTT_message = msg.payload.decode()

#     client.subscribe(topic)
#     client.on_message = on_message
    
#     heart_rate = 0
#     skin_conductance = 0
#     body_temp = 0

#     while(True):
#         client.loop()
#         MQTT_textbox.text(MQTT_message)
#         MQTTarr = MQTT_message.split(",")
#         if(len(MQTTarr) == 3):
#             heart_rate = int(MQTTarr[0])
#             skin_conductance = float(MQTTarr[1])
#             body_temp = float(MQTTarr[2])


#         st.subheader("Your current physiological readings:")
#         col1, col2, col3 = MQTT_display.columns(3)
#         with col1:
#             st.metric(label="Heart Rate ❤️", value=f"{heart_rate} bpm")
#         with col2:
#             st.metric(label="Skin Conductance 💧", value=f"{skin_conductance:.2f} %")
#         with col3:
#             st.metric(label="Body Temperature 🌡️", value=f"{body_temp:.2f} °C")

#         stress_prediction = np.clip(np.random.randint(0, 100), 0, 100) #Need to pull from the RPi!!!
#         st.subheader(f"Predicted Stress Level: {stress_prediction}%")
#         st.progress(stress_prediction / 100)

#         # Link to stress management info
#         st.button("Need help managing stress?", key="info_link")
#         sleep(1)

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
