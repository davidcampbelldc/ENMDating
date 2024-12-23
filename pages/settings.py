import streamlit as st
from utils.auth import require_auth

# Require authentication for this page
require_auth()

def show_settings():
    st.title("Settings")
    st.write("Your settings will appear here.")

if __name__ == "__main__":
    show_settings() 