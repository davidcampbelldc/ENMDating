import streamlit as st
from utils.supabase_client import supabase
import time

def login(email: str, password: str):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state.user = response.user
        st.session_state.authenticated = True
        return True
    except Exception as e:
        st.error(f"Error logging in: {str(e)}")
        return False

def signup(email: str, password: str):
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        if response.user:
            st.success("Successfully signed up!")
            st.info("You can now log in using your credentials.")
            # Don't try to modify session state here
            return True
    except Exception as e:
        st.error(f"Error signing up: {str(e)}")
        return False

def logout():
    supabase.auth.sign_out()
    st.session_state.authenticated = False
    st.session_state.user = None

def auth_page():
    # Initialize active tab in session state if not exists
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Login"
    
    # Create tabs and set active tab
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        st.header("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if login(email, password):
                st.rerun()

    with tab2:
        st.header("Sign Up")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        password_confirm = st.text_input("Confirm Password", type="password", key="signup_password_confirm")
        if st.button("Sign Up"):
            if password != password_confirm:
                st.error("Passwords do not match!")
            else:
                if signup(email, password):
                    # Show success message and instructions
                    st.success("Account created successfully!")
                    st.info("Please use the Login tab to sign in with your credentials.")
                    time.sleep(2)  # Give user time to read the message
  