import streamlit as st
from bank import Bank
import pandas as pd


st.set_page_config(page_title="Simple Bank", layout="centered")

st.title(" Simple Bank App")

menu = st.sidebar.selectbox("Choose action", [
    "Create Account",
    "Deposit",
    "Withdraw",
    "View Details",
    "Update Details",
    "Delete Account",
])

if menu == "Create Account":
    st.header("Create Account")
    with st.form("create_form"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=0, max_value=120, value=18)
        address = st.text_area("Address")
        mobile = st.text_input("Mobile Number")
        father = st.text_input("Father's / Husband's Name")
        pin = st.text_input("4-digit PIN", type="password")
        submitted = st.form_submit_button("Create")
    if submitted:
        try:
            account = Bank.create_account(name, int(age), address, mobile, father, pin)
            st.success("Account created successfully!")
            st.write("Account Number:", account["Account Number"])
            st.write("Keep your PIN and Account Number safe.")
        except Exception as e:
            st.error(str(e))

elif menu == "Deposit":
    st.header("Deposit Money")
    with st.form("deposit_form"):
        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        amount = st.number_input("Amount", min_value=1.0, max_value=10000.0, step=1.0)
        submitted = st.form_submit_button("Deposit")
    if submitted:
        try:
            new_balance = Bank.deposit(acc.strip(), pin.strip(), float(amount))
            st.success(f"Deposited \u20B9{amount:.2f} successfully.")
            st.info(f"New Balance: \u20B9{new_balance:.2f}")
        except Exception as e:
            st.error(str(e))

elif menu == "Withdraw":
    st.header("Withdraw Money")
    with st.form("withdraw_form"):
        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        amount = st.number_input("Amount", min_value=1.0, max_value=10000.0, step=1.0)
        submitted = st.form_submit_button("Withdraw")
    if submitted:
        try:
            new_balance = Bank.withdraw(acc.strip(), pin.strip(), float(amount))
            st.success(f"Withdrawn \u20B9{amount:.2f} successfully.")
            st.info(f"New Balance: \u20B9{new_balance:.2f}")
        except Exception as e:
            st.error(str(e))

elif menu == "View Details":
    st.header("View Account Details")
    
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    
    if st.button("View"):
        try:
            details = Bank.get_details(acc.strip(), pin.strip())
            
            # Convert to tabular 2-column format
            df = pd.DataFrame(
                list(details.items()),  # convert dict → list of (key, value)
                columns=["Field", "Value"]
            )
            
            st.success("Account Details:")
            st.table(df)  # simple static table
            
        except Exception as e:
            st.error(str(e))



elif menu == "Update Details":
    st.header("Update Account Details")
    with st.form("update_form"):
        acc = st.text_input("Account Number")
        pin = st.text_input("Current PIN", type="password")
        name = st.text_input("New Name (leave blank to keep)")
        address = st.text_area("New Address (leave blank to keep)")
        mobile = st.text_input("New Mobile Number (leave blank to keep)")
        father = st.text_input("New Father's / Husband's Name (leave blank to keep)")
        new_pin = st.text_input("New 4-digit PIN (leave blank to keep)", type="password")
        submitted = st.form_submit_button("Update")
    if submitted:
        try:
            kwargs = {}
            if name: kwargs["name"] = name
            if address: kwargs["address"] = address
            if mobile: kwargs["mobile_number"] = mobile
            if father: kwargs["father_or_husband"] = father
            if new_pin: kwargs["new_pin"] = new_pin
            updated = Bank.update_details(acc.strip(), pin.strip(), **kwargs)
            df = pd.DataFrame(
                list(updated.items()),  # convert dict → list of (key, value)
                columns=["Field", "Value"]
            )

            st.success("Details updated successfully.")
            st.table(df)
            
        except Exception as e:
            st.error(str(e))

elif menu == "Delete Account":
    st.header("Delete Account")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Delete"):
        try:
            Bank.delete_account(acc.strip(), pin.strip())
            st.success("Account deleted successfully.")
        except Exception as e:
            st.error(str(e))
