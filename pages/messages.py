import streamlit as st
from utils.auth import require_auth

# Require authentication for this page
require_auth()

def show_messages():
    st.title("Messages")
    st.write("Your messages will appear here.")

if __name__ == "__main__":
    show_messages() 