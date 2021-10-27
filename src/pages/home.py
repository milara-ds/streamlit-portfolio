import streamlit as st


def write():
    if st.session_state['navigation_current'] == None:
        st.session_state['navigation_current'] = "Home"
        st.session_state['navigation_changed'] = False
    elif (st.session_state['navigation_current'] != "Home"):
        st.session_state['navigation_current'] = "Home"
        st.session_state['navigation_changed'] = True
    elif (st.session_state['navigation_current'] == "Home"):
        st.session_state['navigation_changed'] = False

    st.title("Home")
    st.write("---")

    st.write("Hello, my name is Miguel Lara. 😊")

    st.write("I am an enthusiast Data Scientist with master’s in Computer Science with specialization in Data Science\
        and a bachelor’s in engineering. I have experience in projects such as Targeted Marketing, Fraud Detection,\
         and Predicting students’ performance.")

    st.write(" My areas of expertise are on data cleansing, modeling, hyperparameter tunning, model evaluation, \
        pattern recognition, statistical analysis, and profit focus for the business case. I love working with Python \
            to find insights and generate actionable information from data. Moreover, I use other handy tools such as SQL, R and Tableau." )

    st.write("I believe any problem can be solved using the following combination: understanding to the fundamentals and using Occam’s Razor.")