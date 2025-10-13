import streamlit as st
import random
import time

# --- Title and Description ---
st.title("🏥 Multi-Patient Live Monitoring Dashboard")
st.write("Simulating live sensor data for multiple patients: Heart Rate, Temperature, Oxygen Level")

# --- List of Patients ---
patients = ["Arun", "Meena", "John", "Priya", "Ravi"]

# --- Generator Function: Simulate Live Sensor Data per Patient ---
def patient_sensor_stream(patients):
    while True:
        data = []
        for p in patients:
            reading = {
                "name": p,
                "heart_rate": random.randint(60, 100),              # bpm
                "temperature": round(random.uniform(97.0, 100.0), 1), # °F
                "oxygen_level": random.randint(90, 100)            # %
            }
            data.append(reading)
        yield data
        time.sleep(1)  # simulate 1-second delay between updates

# --- Create Placeholders for Each Patient ---
patient_placeholders = {}
for p in patients:
    patient_placeholders[p] = {
        "container": st.container(),
        "hr_bar": None,
        "temp_bar": None,
        "ox_bar": None,
        "hr_text": None,
        "temp_text": None,
        "ox_text": None
    }

# --- Initialize Patient Sections ---
for p in patients:
    with patient_placeholders[p]["container"]:
        st.subheader(f"👩‍⚕️ Patient: {p}")
        patient_placeholders[p]["hr_bar"] = st.progress(0)
        patient_placeholders[p]["temp_bar"] = st.progress(0)
        patient_placeholders[p]["ox_bar"] = st.progress(0)
        patient_placeholders[p]["hr_text"] = st.empty()
        patient_placeholders[p]["temp_text"] = st.empty()
        patient_placeholders[p]["ox_text"] = st.empty()

# --- Run Live Data Stream ---
for readings in patient_sensor_stream(patients):
    for reading in readings:
        p = reading["name"]
        hr = reading["heart_rate"]
        temp = reading["temperature"]
        ox = reading["oxygen_level"]

        # --- Update Progress Bars ---
        patient_placeholders[p]["hr_bar"].progress(min(hr, 100))
        temp_percentage = int((temp - 97) / 3 * 100)  # map 97–100°F → 0–100%
        patient_placeholders[p]["temp_bar"].progress(min(temp_percentage, 100))
        patient_placeholders[p]["ox_bar"].progress(ox)

        # --- Update Text Values ---
        patient_placeholders[p]["hr_text"].text(f"❤️ Heart Rate: {hr} bpm")
        patient_placeholders[p]["temp_text"].text(f"🌡️ Temperature: {temp} °F")
        patient_placeholders[p]["ox_text"].text(f"💨 Oxygen Level: {ox}%")
