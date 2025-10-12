import streamlit as st

# ATM class with methods
class ATM:
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance

    def check_balance(self):
        return f"Your current balance is: ${self.balance}"

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return f"Deposit successful. New balance is: ${self.balance}"
        else:
            return "Invalid deposit amount. Please enter a positive number."

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return f"Withdrawal successful. New balance is: ${self.balance}"
        elif amount > self.balance:
            return "Insufficient funds. Withdrawal denied."
        else:
            return "Invalid withdrawal amount. Please enter a positive number."

# Use Streamlit's session state to store the ATM object
# This ensures the balance persists across user interactions
if 'atm' not in st.session_state:
    st.session_state.atm = ATM()

# --- Streamlit UI ---
st.title("Streamlit ATM Simulator")

# Display the current balance
st.header(st.session_state.atm.check_balance())

# Create tabs for different actions
tab1, tab2, tab3 = st.tabs(["Check Balance", "Deposit", "Withdraw"])

with tab1:
    st.markdown("### View your current balance.")
    if st.button("Refresh Balance"):
        st.experimental_rerun()  # Rerun the script to display the latest balance

with tab2:
    st.markdown("### Deposit Funds")
    deposit_amount = st.number_input("Enter amount to deposit:", min_value=0.01, format="%.2f")
    if st.button("Deposit"):
        message = st.session_state.atm.deposit(deposit_amount)
        st.success(message)
        st.experimental_rerun()

with tab3:
    st.markdown("### Withdraw Funds")
    withdraw_amount = st.number_input("Enter amount to withdraw:", min_value=0.01, format="%.2f")
    if st.button("Withdraw"):
        message = st.session_state.atm.withdraw(withdraw_amount)
        if "Insufficient funds" in message:
            st.error(message)
        else:
            st.success(message)
        st.experimental_rerun()
        