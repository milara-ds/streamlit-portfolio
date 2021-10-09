import streamlit as st

def write():
	if st.session_state['navigation_current'] != "Fraud Detection":
		st.session_state['navigation_current'] = "Fraud Detection"
		st.session_state['navigation_changed'] = True
	else:
		st.session_state['navigation_changed'] = False


st.title("Fraud Detection")
st.write("---")

st.write("Working on the page...")