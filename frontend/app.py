import streamlit as st
import requests
import json

# Backend URL
BACKEND_URL = 'http://localhost:5000/api'

# Session state for auth
if 'token' not in st.session_state:
    st.session_state.token = None

def login_page():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f"{BACKEND_URL}/auth/login", json={"email": email, "password": password})
        if response.status_code == 200:
            st.session_state.token = response.json()['token']
            st.success("Logged in successfully")
            st.rerun()
        else:
            st.error("Invalid credentials")

def register_page():
    st.title("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        response = requests.post(f"{BACKEND_URL}/auth/register", json={"username": username, "email": email, "password": password})
        if response.status_code == 201:
            st.success("Registered successfully. Please login.")
        else:
            st.error("Registration failed")

def upload_page():
    st.title("Upload Code for Analysis")
    uploaded_file = st.file_uploader("Choose a C/C++ file", type=["c", "cpp"])
    if st.button("Upload and Analyze"):
        if uploaded_file:
            files = {"code": uploaded_file}
            headers = {"Authorization": f"Bearer {st.session_state.token}"}
            response = requests.post(f"{BACKEND_URL}/upload", files=files, headers=headers)
            if response.status_code == 200:
                st.success("Analysis complete. Check reports.")
            else:
                st.error("Upload failed")

def dashboard_page():
    st.title("Dashboard")
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    response = requests.get(f"{BACKEND_URL}/reports", headers=headers)
    if response.status_code == 200:
        reports = response.json()
        for report in reports:
            st.subheader(f"Report for {report['codeFile']}")
            st.write(f"Bugs: {len(report['bugs'])}")
            st.write(f"Repairs: {len(report['repairs'])}")
            # Simple visualization
            st.bar_chart({"Bugs": len(report['bugs']), "Repairs": len(report['repairs'])})
    else:
        st.error("Failed to load reports")

# Main app
if st.session_state.token:
    menu = ["Upload", "Dashboard", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Upload":
        upload_page()
    elif choice == "Dashboard":
        dashboard_page()
    elif choice == "Logout":
        st.session_state.token = None
        st.rerun()
else:
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Login":
        login_page()
    elif choice == "Register":
        register_page()
