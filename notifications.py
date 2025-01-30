import streamlit as st

def show_toast(message: str):
    """Affiche une notification en toast."""
    st.toast(message)

def show_spinner(message: str):
    """Utilise un spinner pour indiquer un chargement."""
    return st.spinner(message)
