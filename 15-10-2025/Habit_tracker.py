import json
import datetime
import matplotlib.pyplot as plt

class Habit:
    """Represents a single habit and its completion history."""
    def __init__(self, name):
        self.name = name
        # history is a dictionary: {'YYYY-MM-DD': True, ...}
        self.history = {}

    def mark_completed(self, date=None):
        """Marks the habit as completed for a given date or today."""
        # Format today's date if none is provided
        date = date or datetime.datetime.now().strftime('%Y-%m-%d')
        self.history[date] = True

    def __repr__(self):
        """String representation of the Habit object."""
        return f"{self.name}: {len(self.history)} completions"

class HabitTracker:
    """Manages a collection of Habit objects."""
    def __init__(self):
        self.habits = {}  # Dictionary to store Habit objects: {name: Habit_object}

    def add_habit(self, name):
        """Adds a new habit to the tracker."""
        if name not in self.habits:
            self.habits[name] = Habit(name)
            print(f"Habit '{name}' added.")
        else:
            print("Habit already exists.")

    def delete_habit(self, name):
        """Deletes a habit from the tracker."""
        if name in self.habits:
            del self.habits[name]
            print(f"Habit '{name}' deleted.")
        else:
            print("Habit does not exist.")

    def mark_completed(self, name, date=None):
        """Marks a specific habit as completed."""
        if name in self.habits:
            self.habits[name].mark_completed(date)
            print(f"Habit '{name}' marked as completed for {date if date else 'today'}.")
        else:
            print("Habit does not exist.")

    def view_habits(self):
        """Prints all tracked habits and their completion counts."""
        if not self.habits:
            print("No habits tracked yet.")
            return
        print("\n--- Current Habits ---")
        for habit in self.habits.values():
            print(habit)
        print("----------------------")

    def save_to_file(self, filename='habits.json'):
        """Saves all habit data to a JSON file."""
        # Create a serializable dictionary of all habit histories
        data = {name: habit.history for name, habit in self.habits.items()}
        try:
            with open(filename, 'w') as f:
                # Use indent for readability in the JSON file
                json.dump(data, f, indent=4)
            print(f"Habits saved to '{filename}'.")
        except Exception as e:
            print(f"Error saving file: {e}")


    def load_from_file(self, filename='habits.json'):
        """Loads habit data from a JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)

            # Re-initialize habits based on the loaded names
            self.habits = {name: Habit(name) for name in data}

            # Populate the history for each habit
            for name, history in data.items():
                if name in self.habits:
                    self.habits[name].history = history

            print(f"Habits loaded from '{filename}'.")

        except FileNotFoundError:
            print(f"File '{filename}' not found. Starting with an empty habit tracker.")
        except json.JSONDecodeError:
            print(f"Error reading '{filename}'. File content is invalid JSON. Starting with an empty habit tracker.")
        except Exception as e:
            print(f"An unexpected error occurred during loading: {e}")

    def visualize_habit(self, name):
        """Generates and displays a simple plot of habit completions over time."""
        if name in self.habits:
            habit = self.habits[name]
            if not habit.history:
                print(f"No completion data available for '{name}'.")
                return

            # Get and sort the dates the habit was completed
            completed_dates_str = list(habit.history.keys())
            completed_dates_str.sort()

            # Convert date strings to datetime objects for better plotting
            min_date = datetime.datetime.strptime(completed_dates_str[0], '%Y-%m-%d')
            max_date = datetime.datetime.now()
            
            # Generate a list of all dates from the first completion to today
            date_range = []
            current_date = min_date
            while current_date <= max_date:
                date_range.append(current_date.strftime('%Y-%m-%d'))
                current_date += datetime.timedelta(days=1)

            # Create the list of completion status (1 or 0) for the entire date range
            completions = [1 if date in habit.history else 0 for date in date_range]

            # Use the datetime objects for the x-axis for proper spacing
            dates_for_plot = [datetime.datetime.strptime(d, '%Y-%m-%d') for d in date_range]

            plt.figure(figsize=(12, 6))
            # Plot the completion status as a line plot
            plt.plot(dates_for_plot, completions, marker='o', linestyle='-', color='skyblue', linewidth=1, markersize=5)
            
            plt.title(f'Habit Completion History: {name}', fontsize=16)
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Completed (1=Yes, 0=No)', fontsize=12)
            
            # Set y-ticks clearly
            plt.yticks([0, 1], ['No', 'Yes'])

            # Improve x-axis date formatting
            plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%b %d'))
            plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.DayLocator(interval=max(1, len(date_range) // 10))) # Show ~10 ticks
            
            plt.xticks(rotation=45, ha='right')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout() # Adjust plot to prevent labels from being cut off
            plt.show()
        else:
            print("Habit does not exist.")

def main():
    """Main function to run the command-line interface."""
    tracker = HabitTracker()
    tracker.load_from_file()

    while True:
        print("\n--- Habit Tracker Menu ---")
        print("1. Add Habit")
        print("2. Delete Habit")
        print("3. Mark Habit as Completed")
        print("4. View All Habits")
        print("5. Save Habits to File")
        print("6. Load Habits from File")
        print("7. Visualize Habit")
        print("8. Exit")
        print("--------------------------")

        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter habit name: ")
            tracker.add_habit(name)
        
        elif choice == '2':
            name = input("Enter habit name to delete: ")
            tracker.delete_habit(name)
        
        elif choice == '3':
            name = input("Enter habit name: ")
            date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
            tracker.mark_completed(name, date if date else None)
        
        elif choice == '4':
            tracker.view_habits()
        
        elif choice == '5':
            tracker.save_to_file()
        
        elif choice == '6':
            tracker.load_from_file()
        
        elif choice == '7':
            name = input("Enter habit name to visualize: ")
            tracker.visualize_habit(name)
        
        elif choice == '8':
            print("Exiting Habit Tracker. Goodbye! 👋")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()