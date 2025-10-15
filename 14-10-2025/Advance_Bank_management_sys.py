import streamlit as st
import pandas as pd
import json
import os
import hashlib

# --- CONFIGURATION ---
DATA_FILE = "bank_data_secure.json"

# --- SECURITY ---
def hash_pin(pin: str) -> str:
    """Hashes a PIN using SHA-256."""
    return hashlib.sha256(pin.encode()).hexdigest()

def verify_pin(stored_hash: str, provided_pin: str) -> bool:
    """Verifies a provided PIN against a stored hash."""
    return stored_hash == hash_pin(provided_pin)

# --- DATA PERSISTENCE ---
def load_data() -> dict:
    """Loads account data from the JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_data(data: dict):
    """Saves account data to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# --- INITIALIZE SESSION STATE ---
if 'accounts' not in st.session_state:
    st.session_state.accounts = load_data()

# --- UI PAGES ---
def view_accounts():
    """Displays all accounts in a table, excluding PIN hashes."""
    st.header("👤 All Bank Accounts")
    if not st.session_state.accounts:
        st.info("No accounts found. Please create one from the sidebar.")
        return

    # Convert data to a DataFrame for better display
    accounts_data = st.session_state.accounts.values()
    df = pd.DataFrame(accounts_data)
    
    # Exclude the hashed pin from the default view for security
    df_display = df[['account_holder', 'balance']]
    df_display = df_display.rename(columns={'account_holder': 'Account Holder', 'balance': 'Balance ($)'})
    
    st.dataframe(df_display, use_container_width=True)

def create_account():
    """Page for creating a new bank account."""
    st.header("➕ Create a New Account")
    with st.form("create_form"):
        name = st.text_input("Account Holder Name").strip()
        pin = st.text_input("4-Digit PIN", type="password", max_chars=4)
        balance = st.number_input("Initial Balance", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("Create Account")

        if submitted:
            if not name or not pin or len(pin) != 4 or not pin.isdigit():
                st.error("Please fill all fields correctly (PIN must be 4 digits).")
            elif name in st.session_state.accounts:
                st.error(f"Account for '{name}' already exists!")
            else:
                hashed_pin = hash_pin(pin)
                st.session_state.accounts[name] = {
                    "account_holder": name, 
                    "pin_hash": hashed_pin, 
                    "balance": balance
                }
                save_data(st.session_state.accounts)
                st.success(f"Account for '{name}' created successfully!")

def update_account():
    """Page for updating an existing account (transactions or PIN change)."""
    st.header("🔄 Update an Account")
    if not st.session_state.accounts:
        st.info("No accounts to update.")
        return

    account_to_update = st.selectbox("Select Account", options=list(st.session_state.accounts.keys()))
    
    if account_to_update:
        st.subheader(f"Managing Account: {account_to_update}")
        
        # --- Transactions: Deposit/Withdraw ---
        st.markdown("#### Transactions")
        with st.form("transaction_form"):
            transaction_type = st.radio("Type", ["Deposit", "Withdraw"])
            amount = st.number_input("Amount", min_value=0.01, format="%.2f")
            pin = st.text_input("Enter PIN to confirm", type="password", max_chars=4)
            transact_submitted = st.form_submit_button("Perform Transaction")

            if transact_submitted:
                account_data = st.session_state.accounts[account_to_update]
                if verify_pin(account_data['pin_hash'], pin):
                    if transaction_type == "Deposit":
                        account_data['balance'] += amount
                        st.success(f"Deposited ${amount:.2f}. New balance: ${account_data['balance']:.2f}")
                    elif transaction_type == "Withdraw":
                        if account_data['balance'] >= amount:
                            account_data['balance'] -= amount
                            st.success(f"Withdrew ${amount:.2f}. New balance: ${account_data['balance']:.2f}")
                        else:
                            st.error("Insufficient funds.")
                    save_data(st.session_state.accounts)
                else:
                    st.error("Invalid PIN.")

        # --- PIN Update ---
        st.markdown("---")
        st.markdown("#### Change PIN")
        with st.form("pin_update_form"):
            current_pin = st.text_input("Current PIN", type="password", max_chars=4)
            new_pin = st.text_input("New 4-Digit PIN", type="password", max_chars=4)
            pin_submitted = st.form_submit_button("Update PIN")

            if pin_submitted:
                account_data = st.session_state.accounts[account_to_update]
                if verify_pin(account_data['pin_hash'], current_pin):
                    if len(new_pin) == 4 and new_pin.isdigit():
                        account_data['pin_hash'] = hash_pin(new_pin)
                        save_data(st.session_state.accounts)
                        st.success("PIN updated successfully!")
                    else:
                        st.error("New PIN must be 4 digits.")
                else:
                    st.error("Invalid current PIN.")


def delete_account():
    """Page for deleting an account."""
    st.header("❌ Delete an Account")
    if not st.session_state.accounts:
        st.info("No accounts to delete.")
        return
        
    account_to_delete = st.selectbox("Select Account to Delete", options=list(st.session_state.accounts.keys()))
    
    if account_to_delete:
        st.warning(f"**Warning:** You are about to permanently delete the account for **{account_to_delete}**.")
        pin = st.text_input("Enter PIN to confirm deletion", type="password", max_chars=4)
        
        if st.button("Confirm Deletion"):
            if pin:
                account_data = st.session_state.accounts[account_to_delete]
                if verify_pin(account_data['pin_hash'], pin):
                    del st.session_state.accounts[account_to_delete]
                    save_data(st.session_state.accounts)
                    st.success(f"Account '{account_to_delete}' has been deleted.")
                    # Use st.experimental_rerun() to refresh the page state after deletion
                    st.experimental_rerun()
                else:
                    st.error("Invalid PIN.")
            else:
                st.error("Please enter the PIN to confirm.")

# --- MAIN APP LAYOUT ---
st.set_page_config(page_title="Pro Bank Manager", page_icon="🏦", layout="centered")

st.title("🏦 Chithapphu Mercantile Bank ")
st.write("       A Part of Komal Group of Company       ")

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")
menu = {
    "View All Accounts": view_accounts,
    "Create Account": create_account,
    "Update Account": update_account,
    "Delete Account": delete_account
}
choice = st.sidebar.radio("Go to", list(menu.keys()))

# --- Display the selected page ---
menu[choice]()