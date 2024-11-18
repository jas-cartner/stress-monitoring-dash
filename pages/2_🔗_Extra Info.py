import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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
