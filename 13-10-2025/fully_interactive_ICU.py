import streamlit as st
import random
import time

st.set_page_config(page_title="ICU Live Monitoring Dashboard", layout="wide")

st.title("ICU Live Monitoring Dashboard")
st.write("Monitoring multiple patients in real-time with alerts for abnormal vitals")

# --- Patients list ---
patients = ["Arun", "Meena", "John", "Priya", "Ravi"]

# --- Normal ranges for vitals ---
NORMAL_RANGES = {
    "heart_rate": (60, 100),  # bpm
    "temperature": (97.0, 99.5),  # °F
    "oxygen_level": (95, 100)  # %
}

# --- Generator to simulate live sensor data ---
def patient_sensor_stream(patients):
    """Yields a list of readings for all patients every second."""
    while True:
        data = []
        for p in patients:
            reading = {
                "name": p,
                "heart_rate": random.randint(50, 110),
                "temperature": round(random.uniform(96.0, 101.0), 1),
                "oxygen_level": random.randint(88, 100)
            }
            data.append(reading)
        yield data
        time.sleep(1)

# --- Create placeholders for each patient ---
patient_placeholders = {}

# Use columns for a more compact layout
cols = st.columns(len(patients))

for i, p in enumerate(patients):
    with cols[i]:
        st.subheader(f"Patient: {p}")
        # Custom CSS for progress bar colors
        st.markdown("""
        <style>
            .stProgress > div > div > div > div {
                transition: width 0.5s ease-in-out;
            }
            .normal-bar .stProgress > div > div > div > div {
                background-color: #28a745; /* Green */
            }
            .abnormal-bar .stProgress > div > div > div > div {
                background-color: #dc3545; /* Red */
            }
        </style>
        """, unsafe_allow_html=True)

        hr_container = st.empty()
        temp_container = st.empty()
        ox_container = st.empty()
        alert_container = st.empty()

        patient_placeholders[p] = {
            "hr_container": hr_container,
            "temp_container": temp_container,
            "ox_container": ox_container,
            "alert": alert_container,
        }

# --- Helper function: clamp between 0–100 ---
def clamp(value):
    """Clamps a value to be within the 0-100 range."""
    return max(0, min(100, int(value)))

# --- Run live updates ---
for readings in patient_sensor_stream(patients):
    for reading in readings:
        p = reading["name"]
        hr = reading["heart_rate"]
        temp = reading["temperature"]
        ox = reading["oxygen_level"]

        # --- Check vitals against normal ranges ---
        hr_normal = NORMAL_RANGES["heart_rate"][0] <= hr <= NORMAL_RANGES["heart_rate"][1]
        temp_normal = NORMAL_RANGES["temperature"][0] <= temp <= NORMAL_RANGES["temperature"][1]
        ox_normal = ox >= NORMAL_RANGES["oxygen_level"][0]

        # --- Normalize bar values to 0–100 range for display ---
        # Heart rate: Center around 80bpm as 50%
        hr_bar_value = clamp((hr - 40) * (100 / (120 - 40)))
        # Temperature: Scale 96-101°F to 0-100
        temp_bar_value = clamp((temp - 96) * (100 / (101 - 96)))
        # Oxygen: Scale 90-100% to 0-100
        ox_bar_value = clamp((ox - 90) * 10)

        # --- Update progress bars with color coding ---
        hr_bar_class = "normal-bar" if hr_normal else "abnormal-bar"
        patient_placeholders[p]["hr_container"].markdown(
            f'<div class="{hr_bar_class}"><div data-testid="stProgress"></div></div>',
            unsafe_allow_html=True
        )
        # The progress bar itself is updated inside the container
        with patient_placeholders[p]["hr_container"].container():
            st.progress(hr_bar_value, text=f"Heart Rate: {hr} bpm")

        temp_bar_class = "normal-bar" if temp_normal else "abnormal-bar"
        patient_placeholders[p]["temp_container"].markdown(
            f'<div class="{temp_bar_class}"><div data-testid="stProgress"></div></div>',
            unsafe_allow_html=True
        )
        with patient_placeholders[p]["temp_container"].container():
            st.progress(temp_bar_value, text=f"Temperature: {temp} °F")

        ox_bar_class = "normal-bar" if ox_normal else "abnormal-bar"
        patient_placeholders[p]["ox_container"].markdown(
            f'<div class="{ox_bar_class}"><div data-testid="stProgress"></div></div>',
            unsafe_allow_html=True
        )
        with patient_placeholders[p]["ox_container"].container():
            st.progress(ox_bar_value, text=f"Oxygen Level: {ox}%")


        # --- Alerts ---
        alerts = []
        if not hr_normal:
            alerts.append(f"Heart Rate abnormal: {hr} bpm")
        if not temp_normal:
            alerts.append(f"Temperature abnormal: {temp} °F")
        if not ox_normal:
            alerts.append(f"Oxygen Level low: {ox}%")

        if alerts:
            patient_placeholders[p]["alert"].warning("\n\n".join(alerts))
        else:
            patient_placeholders[p]["alert"].success("Vitals Normal")

    # This sleep is now inside the generator, so we can remove it from here
    # to make the UI update feel slightly faster after the data is yielded.
