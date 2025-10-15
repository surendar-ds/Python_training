import json
import os

DATA_FILE = "bank_data.json"

# ---------- Save data to JSON ----------
def save_data(data):
    """Saves the provided data dictionary to a JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\nData saved to {DATA_FILE} successfully!")

# ---------- Load existing data (if available) ----------
def load_data():
    """Loads data from the JSON file if it exists."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Warning: JSON file was empty or corrupted. Starting fresh.")
                return {}
    else:
        return {}

# ---------- Create account ----------
def create_account(data):
    """Creates a new bank account and adds it to the data."""
    name = input("Enter account holder name: ").strip()
    if name in data:
        print(f"Account for '{name}' already exists!")
        return data

    pin = input("Enter 4-digit PIN: ").strip()
    balance = float(input("Enter initial balance: "))

    data[name] = {"account_holder": name, "pin": pin, "balance": balance}
    print(f"\nAccount for {name} added successfully!")
    return data

# ---------- Read / Display accounts ----------
def display_accounts(data):
    """Displays all existing bank accounts."""
    if not data:
        print("\nNo accounts found.")
        return

    print("\n--- All Bank Accounts ---")
    for account in data.values():
        print(f"Name: {account['account_holder']}, PIN: {account['pin']}, Balance: ${account['balance']:.2f}")

# ---------- Update account ----------
def update_account(data):
    """Updates an existing account's PIN or balance."""
    name = input("Enter the account holder name to update: ").strip()
    if name not in data:
        print(f"Account for '{name}' does not exist!")
        return data

    print("\nWhat would you like to update?")
    print("1. PIN")
    print("2. Balance")
    choice = input("Enter your choice (1/2): ").strip()

    if choice == '1':
        new_pin = input("Enter new 4-digit PIN: ").strip()
        data[name]['pin'] = new_pin
        print(f"\nPIN updated for {name}")
    elif choice == '2':
        new_balance = float(input("Enter new balance: "))
        data[name]['balance'] = new_balance
        print(f"\nBalance updated for {name}")
    else:
        print("Invalid choice.")
    return data

# ---------- Delete account ----------
def delete_account(data):
    """Deletes a specified bank account."""
    name = input("Enter the account holder name to delete: ").strip()
    if name in data:
        confirm = input(f"Are you sure you want to delete account '{name}'? (y/n): ").lower()
        if confirm == 'y':
            del data[name]
            print(f"\nAccount '{name}' deleted successfully!")
        else:
            print("Delete cancelled.")
    else:
        print(f"Account for '{name}' does not exist!")
    return data

# ---------- Main program ----------
def main():
    """Main function to run the bank account manager application."""
    print("Welcome to the Bank Account Manager")
    data = load_data()

    while True:
        print("\n--- Menu ---")
        print("1. Create Account")
        print("2. Display All Accounts")
        print("3. Update Account")
        print("4. Delete Account")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            data = create_account(data)
        elif choice == '2':
            display_accounts(data)
        elif choice == '3':
            data = update_account(data)
        elif choice == '4':
            data = delete_account(data)
        elif choice == '5':
            save_data(data)
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1-5.")

if __name__ == "__main__":
    main()