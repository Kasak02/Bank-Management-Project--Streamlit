# Bank Management System — Streamlit

A simple Bank Management demo built with **Python** and **Streamlit**.  
This is a beginner-friendly project that demonstrates CRUD operations (Create, Read, Update, Delete) for bank accounts stored in a local JSON file.

## Features
- Create a new account (name, age, address, mobile, PIN)
- Deposit money (amount limits enforced)
- Withdraw money (with balance check)
- View account details in a neat table
- Update account information
- Delete an account
- All data stored locally in `data.json` (for demo only)

## Tech Stack
- Python 3.8+
- Streamlit
- JSON for simple persistence

## Files
- `bank.py` — backend module for account management
- `streamlit_app.py` (or `app.py`) — Streamlit frontend
- `data.json` — local storage (auto-created)
- `.gitignore` — recommended to avoid committing `data.json`


