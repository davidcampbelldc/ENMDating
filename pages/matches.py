import streamlit as st
from utils.auth import require_auth

# Require authentication for this page
require_auth()

def show_matches():
    st.title("Matches")
    st.write("Your matches will appear here.")

if __name__ == "__main__":
    show_matches() 