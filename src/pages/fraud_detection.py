import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np

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

	#2. Plot Differences between Profiles ************************************************
    st.markdown("## **Genuine and Fraud average behavior**")

    st.markdown("One of the firsts tasks of the Data Scientist is to get to know the data which is also known as *Exploratory Data Analysis*. One example \
				of the outcome of this analysis is shown in the spyder plot below. The plot presents all the variables in the dataset as if they were\
				angles of the circle. The blue and red areas are the mean values of each variable for the two types of transactions. In other words, \
				the average behavior of the variables for genuine and fraud transactions. The variables V1 to V19 seem to have huge difference. ")

    st.markdown("**[Interactive]** Click on the labels that are on the top-right side of the plot, the areas will disappear. If the fraud's area is \
		        removed it can be seen that the genuine area has a different shape than a circle, the reason is that the range of its values are closer\
		        to zero than the values of the fraud's area.")

	#Calculate the mean values of the variables for each class
    @st.cache
    def read_class():
	    return pd.read_csv("https://raw.githubusercontent.com/milara-ds/streamlit-portfolio-app/main/data/class_mean_variables.csv")

    df_profile = read_class()
    categories = df_profile.columns

	#Plot 
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
	      r= df_profile.iloc[0].to_list(),
	      theta=categories,
	      fill='toself',
	      name='Genuine\'s area'
	))

    fig.add_trace(go.Scatterpolar(
	      r=df_profile.iloc[1].to_list(),
	      theta=categories,
	      fill='toself',
	      name='Fraud\'s area'
	))

    st.plotly_chart(fig, use_container_width=True)

	#3. Plot "Cost of Errors"***************************************************************
    st.markdown("## **Cost of making a mistake**")

    st.markdown("Another important task before start creating the models is to determine if there is a benefit or cost associated to the problem. \
		         This type of approach helps to design the models towards a solution that either generates profits or reduces costs. \
		         For the sake of simplicity of this problem, the **average cost of fraud** and the **average cost of analysis** \
		         of a transaction are defined. The average cost of fraud is the mean of the amount of the frauds in the dataset and the average \
		         cost of analysis is the cost of one person verifying the transaction.")

    st.markdown("**[Interactive]** Use the sliders to change the average cost of fraud and analysis and see how the plot below changes. ")

    st.markdown(" The plot below shows the number of false alarms (*when a person performed an analysis when it was not necessary*) in the horizontal \
		         axis and the amount of € in the vertical axis. The diagonal is the function for the marginal gain per extra fraud caught. In other words,\
		        it shows the benefits if it is worth catching a fraud after a number of false alarms. For instance, there is a loss if the model \
		        correcly finds 1 fraud transaction but generates 62 false alarms.")
	
    fixed_avcost_fraud = 122.2

    st.write(f'The **average cost of fraud** calculated from the data is € {fixed_avcost_fraud}')
    avg_fraud_cost = st.slider('Average cost of fraud € ', 100, 300, 122)

    st.write(f'The **average cost of analysis** is calculated based on the salary of an employee and the amount of time it takes to analyse a transaction')
    avg_monitoring_cost = st.slider('Average cost of analysis € ', 1, 5, 2)

    count_of_false_positives = np.arange(0, avg_fraud_cost / avg_monitoring_cost * 2)
    marginal_cost_function = count_of_false_positives * -avg_monitoring_cost + avg_fraud_cost
    intersect = int(avg_fraud_cost / avg_monitoring_cost)


	#Plot
    fig = px.line( x=count_of_false_positives, 
		y=marginal_cost_function)

    fig.add_trace(
		go.Scatter(	
			mode = 'markers',
			x = [intersect],
			y = [0],
			marker=dict(
	            color='red',
	            size=10,
	            ),
			showlegend=False,
			name = 'Intersection'
			))

    fig.update_layout(
	    yaxis_title="Amount in €",
	    xaxis_title="Number of false alarm",
	    title_text= "Marginal gain per extra fraud caught",
	    title_x=0.5
	    )

    st.plotly_chart(fig, use_container_width=True)

	st.write(f'After {intersect} false alarms, it wasn\'t worth catching the extra fraud.')