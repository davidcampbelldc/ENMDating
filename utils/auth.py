import streamlit as st
from utils.supabase_client import supabase
import json

def init_auth():
    # Check if we have a session in local storage via Streamlit's session state
    if 'supabase_auth' not in st.session_state:
        try:
            # Try to get the session from Supabase's built-in persistence
            session = supabase.auth.get_session()
            if session:
                st.session_state.supabase_auth = session
                st.session_state.user = session.user
        except Exception as e:
            print(f"Error getting session: {e}")
            st.session_state.supabase_auth = None
            st.session_state.user = None

def login(email: str, password: str):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        st.session_state.supabase_auth = res
        st.session_state.user = res.user
        return True
    except Exception as e:
        st.error(f"Error logging in: {str(e)}")
        return False

def signup(email: str, password: str):
    try:
        res = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return True
    except Exception as e:
        st.error(f"Error signing up: {str(e)}")
        return False

def logout():
    try:
        supabase.auth.sign_out()
        st.session_state.supabase_auth = None
        st.session_state.user = None
    except Exception as e:
        st.error(f"Error logging out: {str(e)}")

def require_auth():
    init_auth()  # Try to restore session
    
    # If no authenticated user, redirect to login
    if not st.session_state.get('user'):
        st.warning("Please log in to access this page")
        st.stop()