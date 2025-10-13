import streamlit as st
import random
import time

st.title("Hospital Sensor Live Monitoring")
st.write("Simulating live sensor data: heart rate , temperature, and oxygen level.")

# Initialize placeholders for sensor data
def sensor_data_stream():
    while True: 
        
        yield {
            "heart_rate": random.randint(60, 100),  # Simulated heart rate
            "temprature": round(random.uniform(36.5, 37.5), 1),  # Simulated temperature
            "oxygen_level": random.randint(95, 100)  # Simulated oxygen level
            }
        time.sleep(1)  # Simulate a delay for live data

#----streamlit UI placeholders----
heart_rate_bar = st.progress(0)
temprature_bar = st.progress(0)
oxygen_level_bar = st.progress(0)
heart_rate_text = st.empty()
temprature_text = st.empty()
oxygen_level_text = st.empty()
#-------------------------------
# Simulate live data updates
for data in sensor_data_stream():
    heart_rate = data["heart_rate"]
    temprature = data["temprature"]
    oxygen_level = data["oxygen_level"]

    # Update progress bars and text
    heart_rate_bar.progress(heart_rate / 100)
    temprature_bar.progress((temprature - 36.5) / (37.5 - 36.5))
    oxygen_level_bar.progress(oxygen_level / 100)

    heart_rate_text.text(f"Heart Rate: {heart_rate} bpm")
    temprature_text.text(f"Temperature: {temprature} °C")
    oxygen_level_text.text(f"Oxygen Level: {oxygen_level}%")

    time.sleep(1)  # Simulate a delay for live data

# Note: In a real application, you would replace the random data generation with actual sensor data fetching logic.

        

