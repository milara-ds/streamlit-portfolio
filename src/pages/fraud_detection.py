import streamlit as st
import plotly.graph_objects as go

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
    
    st.markdown("Fraud Detection is a powerful application of Machine Learning models. Where the first objective is to create a tool that identifies\
	             when a transaction is fraudulent or not, and the second objective is to make that tool have a better performance than the current\
				 tool (*assume it is not with Machine Learning*) ")

    st.markdown("The following charts aim to show a quick and interactive overview of the job of a **Data Scientist** does to solve this type of problem. \
		        The data used in this project contains anonymized credit card transactions labeled as fradulent or genuine. The transactions were made \
		        in September 2013 by European cardholders. The data was retrieved from two day transactions, where only **492** were fraud out of **284,807**.")

	#1. Plot "Diference between NoneFrauds and Frauds"**************************************
	#Plot
    x = ['Genuine', 'Frauds']
    y = [284315,492] 
    colors = ['royalblue','crimson']

    fig = go.Figure(data=[go.Bar(
				x=x, 
				y=y,
				text=y,
				textposition='auto',
				marker_color = colors,
			)])

    fig.update_layout( yaxis_title="Number of transactions",
						title_text= "Genuine vs Fraud Transactions",
						title_x=0.5)

    st.plotly_chart(fig, use_container_width=True)