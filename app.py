"""
import streamlit as st

import src.pages.home
import src.pages.fraud_detection
import src.pages.targeted_marketing

PAGES = {
    "Home": src.pages.home,
    "Fraud Detection": src.pages.fraud_detection,
    "Targeted Marketing": src.pages.targeted_marketing
}


def main():
    st.sidebar.write("# Navigation")

    selection = st.sidebar.radio("Go to:", list(PAGES.keys()))
    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.write()

    st.sidebar.write("---")
    st.sidebar.write("# About")
    st.sidebar.info("Author: Miguel Lara\n\n [LinkedIn](https://www.linkedin.com/in/miguellaradatascientist)")
    

if __name__ == "__main__":
    st.set_page_config(
        page_title="Milara's Portfolio",
        page_icon=(":computer:"),
        layout="centered",
        initial_sidebar_state="auto",
    )

    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    if 'navigation_changed' not in st.session_state and 'navigation_current' not in st.session_state:
        st.session_state['navigation_changed'] = False
        st.session_state['navigation_current'] = None

    #main()
    st.write("Hola Mundo")
"""
import streamlit as st

st.write("Hola Mundo")