
import streamlit as st
from components.database import users_db, authenticate_user, get_user, save_resume

def signup():
    st.subheader("🔐 Sign Up")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):
        if email in users_db:
            st.error("❌ Email already exists.")
        elif password != confirm_password:
            st.error("❌ Passwords do not match.")
        elif not (name and email and password):
            st.error("❌ Please fill all fields.")
        else:
            users_db[email] = {
                "name": name,
                "password": password,
                "resumes": []
            }
            st.success("✅ Account created successfully! Please log in.")
            st.session_state["mode"] = "login"

def login():
    st.subheader("🔐 Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        user = authenticate_user(email, password)
        if user:
            st.success(f"✅ Welcome, {user['name']}!")
            st.session_state["authenticated"] = True
            st.session_state["user_email"] = email
            st.session_state["user_name"] = user["name"]
        else:
            st.error("❌ Invalid credentials.")
