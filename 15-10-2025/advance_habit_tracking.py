import json
import datetime
import matplotlib.pyplot as plt
import streamlit as st

# Use st.cache_data to cache data from the file, avoiding re-loading on every interaction.
# This makes the app much faster.
@st.cache_data
def load_habits(filename='habits.json'):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_habits(data, filename='habits.json'):
    with open(filename, 'w') as f:
        json.dump(data, f)

# --- App UI and Logic ---
def main():
    st.set_page_config(page_title="Daily Habit Tracking", layout="wide")
    st.title("📊 Daily Habit Tracking")
    st.markdown("Track your habits and visualize your progress!")
    st.markdown("---Speciliazed by komal group of companies---")
    # Initialize session state to persist data across reruns
    if 'habits' not in st.session_state:
        st.session_state.habits = load_habits()
        
    # Sidebar for actions
    with st.sidebar:
        st.header("Actions")
        action = st.radio("Choose an action:", ["Add Habit", "Mark Completed", "Visualize Habit"])

    if action == "Add Habit":
        st.subheader("Add a New Habit")
        new_habit_name = st.text_input("Enter new habit name:")
        if st.button("Add"):
            if new_habit_name and new_habit_name not in st.session_state.habits:
                st.session_state.habits[new_habit_name] = {}
                st.success(f"Habit '{new_habit_name}' added.")
            else:
                st.warning("Habit already exists or name is empty.")

    elif action == "Mark Completed":
        st.subheader("Mark a Habit as Completed")
        if st.session_state.habits:
            habit_name_to_mark = st.selectbox("Select a habit:", list(st.session_state.habits.keys()))
            date_to_mark = st.date_input("Select date:", datetime.date.today())
            
            if st.button("Mark Completed"):
                date_str = date_to_mark.strftime('%Y-%m-%d')
                if date_str not in st.session_state.habits[habit_name_to_mark]:
                    st.session_state.habits[habit_name_to_mark][date_str] = True
                    st.success(f"'{habit_name_to_mark}' marked as completed on {date_str}.")
                else:
                    st.info(f"'{habit_name_to_mark}' was already completed on {date_str}.")
        else:
            st.info("No habits to mark. Add a habit first.")
            
    elif action == "Visualize Habit":
        st.subheader("Visualize Habit Completion")
        if st.session_state.habits:
            habit_name_to_visualize = st.selectbox("Select a habit to visualize:", list(st.session_state.habits.keys()))
            
            if st.button("Generate Plot"):
                if st.session_state.habits[habit_name_to_visualize]:
                    dates_completed = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in st.session_state.habits[habit_name_to_visualize].keys()]
                    
                    if dates_completed:
                        # Create a full date range from the first to the last date
                        min_date = min(dates_completed).date()
                        max_date = datetime.date.today()
                        date_range = [min_date + datetime.timedelta(days=x) for x in range((max_date - min_date).days + 1)]
                        
                        # Prepare data for plotting
                        #completion_status = [1 if d.date() in [d.date() for d in dates_completed] else 0 for d in date_range]
                        # The corrected line where the error occurred
                        completion_status = [1 if d in [d_completed.date() for d_completed in dates_completed] else 0 for d in date_range]

                        fig, ax = plt.subplots(figsize=(10, 5))
                        ax.plot(date_range, completion_status, marker='o', linestyle='-', color='skyblue', label='Completed')
                        
                        ax.set_title(f'Completion Trend for {habit_name_to_visualize}', fontsize=16)
                        ax.set_xlabel('Date', fontsize=12)
                        ax.set_ylabel('Completed (Yes/No)', fontsize=12)
                        
                        # Improve X-axis formatting
                        plt.xticks(rotation=45)
                        plt.tight_layout()
                        plt.yticks([0, 1], ['No', 'Yes'])
                        
                        st.pyplot(fig) # Use st.pyplot() to display the Matplotlib figure
                    else:
                        st.info("This habit has no completions to visualize yet.")
                else:
                    st.info("This habit has no completions to visualize yet.")
        else:
            st.info("No habits to visualize. Add a habit first.")
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Save/Load")
    if st.sidebar.button("Save Habits"):
        save_habits(st.session_state.habits)
        st.sidebar.success("Habits saved!")

if __name__ == "__main__":
    main()