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

    st.write("I am an enthusiast Data Scientist with a bachelor’s in engineering and a master’s in Computer Science \
        focused on Machine Learning and Statistics. I have experience in projects such as Targeted Marketing, Fraud Detection,\
         and Predicting students’ performance.")

    st.write(" My areas of expertise are on data cleansing, data preparation, modeling, \
         hyperparameter tunning, and model evaluation with profit focus for the business case. I love working with python. \
         Moreover, I use other handy tools such as SQL, R and Tableau." )

    st.write("I believe any problem can be solved using the following combination: understanding to the fundamentals and using Occam’s Razor.")