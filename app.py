import streamlit as st
from utils.auth import init_auth, login, logout, signup
from utils.supabase_client import supabase

# Page config
st.set_page_config(
    page_title="ENM Dating",
    page_icon="💕",
    layout="wide"
)

# Initialize the auth state
init_auth()

# If user is already logged in, show main app content
if st.session_state.get('user'):
    # Create a sidebar for navigation and logout
    with st.sidebar:
        st.write(f"Welcome, {st.session_state.user.email}")
        if st.button("Logout"):
            logout()
            st.rerun()
        
        st.divider()
        
        # Add navigation links
        st.page_link("pages/profile.py", label="Profile", icon="👤")
        st.page_link("pages/matches.py", label="Matches", icon="❤️")
        st.page_link("pages/messages.py", label="Messages", icon="💬")
        st.page_link("pages/settings.py", label="Settings", icon="⚙️")
    
    # Main content area
    st.title("ENM Dating")
    st.write("Welcome to ENM Dating! Use the sidebar to navigate through the app.")
    
else:
    # Create tabs for Login and Sign Up
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    # Login tab
    with tab1:
        st.header("Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if login(email, password):
                    st.success("Logged in successfully!")
                    st.rerun()
    
    # Sign Up tab
    with tab2:
        st.header("Sign Up")
        with st.form("signup_form"):
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            signup_submit = st.form_submit_button("Sign Up")
            
            if signup_submit:
                if new_password != confirm_password:
                    st.error("Passwords do not match!")
                else:
                    if signup(new_email, new_password):
                        st.success("Account created successfully! Please log in.") 