import streamlit as st

st.set_page_config(page_title="LabCare", page_icon="🧪", layout="wide")

# Auto-login as SuperAdmin and redirect to Financial
st.session_state["logged_in"] = True
st.session_state["user"] = {
    "role": "SuperAdmin", "display": "Admin", "page": "Financial"
}
st.switch_page("pages/Financial.py")