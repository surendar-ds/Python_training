import streamlit as st
import json
import os

# --- Configuration & Data Persistence ---
DATA_FILE = "bank_data.json"

def load_data():
    """Loads account data from a JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                st.error("Error decoding JSON file. Starting with an empty dataset.")
                return {}
    return {}

def save_data(data):
    """Saves account data to a JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- BankAccount Class ---
class BankAccount:
    """Represents a bank account with basic ATM functionalities."""
    def __init__(self, account_holder, pin, balance=0):
        self.account_holder = account_holder
        self.__pin = pin  # Private attribute for the PIN
        self.__balance = balance  # Private attribute for the balance

    def verify_pin(self, pin):
        """Checks if the provided PIN matches the account's PIN."""
        return self.__pin == pin

    def deposit(self, amount):
        """Adds a positive amount to the account balance."""
        if amount > 0:
            self.__balance += amount
            return f"Deposited ₹{amount}. New balance: ₹{self.__balance}"
        return "Invalid deposit amount."

    def withdraw(self, amount):
        """Withdraws a positive amount if funds are sufficient."""
        if amount <= 0:
            return "Invalid withdrawal amount."
        elif amount > self.__balance:
            return "Insufficient funds."
        else:
            self.__balance -= amount
            return f"Withdrew ₹{amount}. Remaining balance: ₹{self.__balance}"

    def get_balance(self):
        """Returns the current account balance."""
        return self.__balance

    def to_dict(self):
        """Converts the account object to a dictionary for JSON serialization."""
        return {
            "account_holder": self.account_holder,
            "pin": self._BankAccount__pin,  # Accessing the private PIN
            "balance": self._BankAccount__balance  # Accessing the private balance
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a BankAccount object from a dictionary."""
        return cls(data["account_holder"], data["pin"], data["balance"])

# --- Streamlit UI Components ---

# Set up the main page configuration
st.set_page_config(page_title="ATM System", page_icon="🏦")
st.title("ATM System")

# Load persistent account data
accounts_data = load_data()

# Initialize session state variables if they don't exist
if "account" not in st.session_state:
    st.session_state.account = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# --- Navigation Menu ---
menu = st.sidebar.radio("Menu", ["Create Account", "Login", "ATM Operations"])

# --- Main App Logic ---

# Create Account Page
if menu == "Create Account":
    st.header("Step 1: Create a New Account")
    name = st.text_input("Enter account holder name:")
    pin = st.text_input("Set a 4-digit PIN", type="password", max_chars=4)
    initial_balance = st.number_input("Initial Deposit", min_value=0, step=100)
    
    if st.button("Create Account"):
        if not name.strip():
            st.warning("Please enter a valid name.")
        elif not pin.isdigit() or len(pin) != 4:
            st.warning("The PIN must be a 4-digit number.")
        elif name in accounts_data:
            st.error("An account with this name already exists. Please choose a different name.")
        else:
            new_account = BankAccount(name.strip(), pin, initial_balance)
            accounts_data[name] = new_account.to_dict()
            save_data(accounts_data)
            st.success(f"Account created successfully for {name} with a balance of ₹{initial_balance}.")
            st.info("Go to the 'Login' page from the sidebar to access ATM services.")

# Login Page
elif menu == "Login":
    st.header("Step 2: Log In to Your Account")
    if not accounts_data:
        st.warning("No accounts found. Please create one first.")
    else:
        name = st.text_input("Enter account holder name:")
        entered_pin = st.text_input("Enter your 4-digit PIN", type="password", max_chars=4)
        
        if st.button("Login"):
            if name not in accounts_data:
                st.error("Account not found. Please check your name.")
            else:
                account_info = accounts_data[name]
                account = BankAccount.from_dict(account_info)
                if account.verify_pin(entered_pin):
                    st.session_state.account = account
                    st.session_state.logged_in = True
                    st.session_state.user_name = name
                    st.success(f"Welcome, {account.account_holder}! You have successfully logged in.")
                    st.info("Go to the 'ATM Operations' page to perform transactions.")
                else:
                    st.error("Incorrect PIN. Please try again.")

# ATM Operations Page
elif menu == "ATM Operations":
    st.header("ATM Operations")
    if not st.session_state.logged_in or st.session_state.account is None:
        st.warning("Please log in first from the 'Login' page.")
    else:
        account = st.session_state.account
        name = st.session_state.user_name
        
        st.subheader(f"Account: {name}")
        action = st.radio("Choose an action", ["Check Balance", "Deposit", "Withdraw"])

        if action == "Check Balance":
            st.success(f"Your current balance is ₹{account.get_balance()}.")

        elif action == "Deposit":
            amount = st.number_input("Enter deposit amount", min_value=0, step=100, key="deposit_input")
            if st.button("Deposit", key="deposit_button"):
                message = account.deposit(amount)
                st.info(message)
                accounts_data[name] = account.to_dict()
                save_data(accounts_data)

        elif action == "Withdraw":
            amount = st.number_input("Enter withdrawal amount", min_value=0, step=100, key="withdraw_input")
            if st.button("Withdraw", key="withdraw_button"):
                message = account.withdraw(amount)
                st.info(message)
                accounts_data[name] = account.to_dict()
                save_data(accounts_data)
        
        st.write("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.account = None
            st.session_state.user_name = ""
            st.success("You have been logged out successfully.")