
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go
import asyncio

st.set_page_config(layout="wide")

# Cache the random data generation for sensor readings and stress levels
@st.cache_data
def generate_sensor_data():
    dates = pd.date_range('2023-08-15', periods=7)
    sensor_data = pd.DataFrame({
        'Date': dates,
        'Heart Rate': np.random.randint(60, 160, size=7),
        'Skin Conductance': np.random.randint(50, 100, size=7),
        'Body Temp': np.random.randint(95, 100, size=7)
    })
    sensor_data.set_index('Date', inplace=True)
    return sensor_data

@st.cache_data
def generate_daily_stress_data():
  days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
  stress_levels = np.random.randint(40, 90, size=7)
  return pd.DataFrame({'Day': days, 'Average Stress Level': stress_levels})

@st.cache_data
def get_current_stress_level():
    return np.random.randint(0, 10)

@st.cache_data
def get_daily_progress():
    return np.random.randint(60, 100)

@st.cache_data
def generate_current_data():
    times = [-60,-50,-40,-30,-20,-10,0]
    current_data = pd.DataFrame({
        'Time': times,
        'Heart Rate': np.random.randint(60, 160, size=7),
        'Skin Conductance': np.random.randint(50, 100, size=7),
        'Body Temp': np.random.randint(95, 100, size=7)
    })
    return current_data

async def update_current_data(old_data,placeholder):
    current_data = old_data
    times = [-60,-50,-40,-30,-20,-10,0]
    while True: 
        current_data = current_data.shift(periods=-1, axis=0, fill_value=0)
        current_data["Time"] = times
        current_data.loc[6,'Heart Rate'] = current_data.at[5,'Heart Rate'] + np.random.randint(-10, 10)
        current_data.loc[6,'Skin Conductance'] = current_data.at[5,'Skin Conductance'] + np.random.randint(-10, 10)
        current_data.loc[6,'Body Temp'] = current_data.at[5,'Body Temp'] + np.random.randint(-10, 10)
        with placeholder.container():
            # Plot the Line Chart with custom colors
            line_chart2 = alt.Chart(current_data.reset_index()).transform_fold(
                ['Heart Rate', 'Skin Conductance', 'Body Temp'],
                as_=['Sensor', 'Value']
            ).mark_line().encode(
                x='Time:Q',
                y='Value:Q',
                color=alt.Color('Sensor:N', scale=alt.Scale(range=['#FDD76F', '#D6D0FD', '#202125']))
            ).properties(
                width=500,  # reduce the chart width
                height=300
            )
            st.altair_chart(line_chart2)
        await asyncio.sleep(1)

# Set up user information
name = "User"
st.title(f"Hi, {name}!")

# Adjusted column layout with better spacing (reduce chart width)
col1,  col2= st.columns([1, 1])

# Left column: Line Chart and Bar Chart
with col1:
    # Fetch the cached sensor data
    sensor_data = generate_sensor_data()
    # Plot the Line Chart with custom colors
    st.subheader("Sensor Readings Over the Week")
    #Constant Sensor Readings Chart
    current_data = generate_current_data()
    # creating a single-element container.
    #st.subheader("Current Sensor Readings")
    placeholder = st.empty()
    asyncio.run(update_current_data(current_data,placeholder))
    
    # line_chart = alt.Chart(sensor_data.reset_index()).transform_fold(
    #     ['Heart Rate', 'Skin Conductance', 'Body Temp'],
    #     as_=['Sensor', 'Value']
    # ).mark_line().encode(
    #     x='Date:T',
    #     y='Value:Q',
    #     color=alt.Color('Sensor:N', scale=alt.Scale(range=['#FDD76F', '#D6D0FD', '#202125']))
    # ).properties(
    #     width=500,  # reduce the chart width
    #     height=300
    # )
    # st.altair_chart(line_chart)

    # Fetch the cached average stress data
    daily_stress = generate_daily_stress_data()
    
    # Plot the Bar Chart with custom colors
    st.subheader("Average Stress Level Each Day")
    bar_chart = alt.Chart(daily_stress).mark_bar(color='#D6D0FD').encode(
        x=alt.X('Day:N'),
        y=alt.Y('Average Stress Level:Q'),
    ).properties(
        width=500,  # reduce the chart width
        height=300
    )
    st.altair_chart(bar_chart)


# Right column: Current Stress Level, Mood Input, and Recommendations
with col2:
    # Fetch the cached current stress level
    current_stress_level = get_current_stress_level()
    st.subheader("Current Stress Level")

    # Create radial bar for stress level with transparent background and smaller size
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_stress_level,
        gauge={
            'axis': {'range': [0, 10]},
            'bar': {'color': '#D6D0FD'},
            'bgcolor': '#EDEDED',
            # 'borderwidth': 2,
            'bordercolor': "rgba(0,0,0,0)"
            # 'steps': [
            #     {'range': [0, 4], 'color': "#EFECFE"},
            #     {'range': [4, 7], 'color': "#F8F8FC"},
            #     {'range': [7, 10], 'color': "#202125"}
            # ]
        },
        domain={'x': [0, 0.8], 'y': [0, 1]}
    ))

    # Adjust background transparency and size
    fig.update_layout(
        width=250,  # Smaller size
        height=250,
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0),  # Remove margins
    )

    # Display the radial gauge
    st.plotly_chart(fig, use_container_width=False)

    # Asking the User How They Feel with a slider instead of radio buttons
    st.subheader("How are you feeling right now?")
    feeling = st.select_slider(
        "Choose your current mood",
        options=['😊 Happy', '🙂 Okay', '😐 Neutral', '😟 Stressed', '😢 Sad'],
        value='😐 Neutral'
    )

    # Recommendations to reduce stress
    st.subheader("Recommendations to reduce stress:")
    st.write("""
    - Practice mindfulness and breathing exercises
    - Take a short walk to relax
    - Listen to calming music or meditate
    - Ensure you are getting enough sleep and proper nutrition
    - Stay connected with friends and loved ones
    """)

# Bottom section for Daily Progress
# st.subheader("Daily Progress")
# daily_progress = get_daily_progress()
# st.progress(daily_progress / 100)

# Add custom CSS for rounded edges and padding
st.markdown("""
    <style>
        div[data-testid="stPlotlyChart"] {
            background-color: rgba(255, 255, 255, 0.1); /* Slightly transparent white */
            padding: 10px;
            border-radius: 15px; /* Rounded corners */
        }
    </style>
    <style>
    .css-1n76uvr {
        margin-right: 20px; /* Adjust this value to control spacing */
    }
    </style>
    """, unsafe_allow_html=True)



# Fetch the cached daily progress
# st.subheader("Daily Progress")
# daily_progress = get_daily_progress()
# st.text(f'Progress: {daily_progress}')
# st.progress(daily_progress / 100)
