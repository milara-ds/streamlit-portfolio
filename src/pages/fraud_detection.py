import streamlit as st


def write():
    if st.session_state['navigation_current'] == None:
        st.session_state['navigation_current'] = "Fraud Detection"
        st.session_state['navigation_changed'] = False
    elif (st.session_state['navigation_current'] != "Fraud Detection"):
        st.session_state['navigation_current'] = "Fraud Detection"
        st.session_state['navigation_changed'] = True
    elif (st.session_state['navigation_current'] == "Fraud Detection"):
        st.session_state['navigation_changed'] = False
        
    st.title("Fraud Detection")
    st.write("---")

    st.write("Working on the page...")

    st.write("In the meantime, please visit the complete analysis [here](https://github.com/milara-ds/targeted-marketing/blob/main/Uplift_v1.ipynb).")