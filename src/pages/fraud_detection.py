import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


def write():
	if st.session_state['navigation_current'] != "Fraud Detection":
		st.session_state['navigation_current'] = "Fraud Detection"
		st.session_state['navigation_changed'] = True
	else:
		st.session_state['navigation_changed'] = False


	#Title
	st.title("Fraud Detection on Credit Card data")
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
		return pd.read_csv("https://github.com/milara-ds/streamlit-portfolio-app/blob/main/data/class_mean_variables.csv")

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

	#4. Plot "Modeling"*********************************************************************************
	st.markdown("## **Machine Learning Models**")

	st.markdown("This is one where the fun is. The Data Scientist has to find the model that provide the best results. For that \
	            many experiments are run to test different hypothesis until the best model is found. The plot below shows the results \
	            of 4 experiments and 1 baseline (Dummy classifier). The horizontal axis presents the proportion of instances of a test \
	            set (transactions that the model has never seen), and the vertical axis presents the cost each model generates \
	            after processing the test set.")

	st.markdown("**[Interactive]** Click on the top-left labels to enable and disable each experiment. Try disabling the Dummy classifier.")

	st.markdown("Let's imagine you have a budget of € 4,000 to pay for the analysis of transactions and to reimburse fraudulent transactions. Which \
		        model would you like to use for this task? ")

	st.markdown("**NOTE: it takes a few seconds to refresh the Cost curve after the sliders are updated**")

	def error_cost(y_pred,y_test,costs):
	    """
	    Returns the costs of the error
	    
	    Parameters:
	    -----------
	    y_pred: classes estimated by the classifier
	    y_test: actual classes
	    costs: costs of the errors
	    """
	    if y_pred == 1 and y_test == 1:
	        return costs['avg_analysis_cost']
	    if y_pred == 1 and y_test==0:
	        return costs['avg_analysis_cost']
	    elif y_pred== 0 and y_test==1:
	        return costs['avg_fraud_cost'] 
	    else:
	        return 0
	    
	def compute_cost_df(y_proba,y_test,best_thres,costs):
	    """
	    Generates a df with the cummulative cost of the errors
	    
	    Parameters:
	    ------------
	    y_proba: array with the probabilities of X_test given by an estimator
	    y_test: array with the actual values of y
	    best_thres: int best threshold to define a binary outcome
	    costs: dict with the costs of the errors
	    """
	    #Build the df for the cost curve
	    df_cost_curve = pd.DataFrame({'y_proba':y_proba, 
	                                  'y_pred': np.where(y_proba > best_thres,1,0),
	                                  'y_test':y_test})

	    #Sort df by probability
	    df_cost_curve = df_cost_curve.sort_values(by='y_proba', ascending = False).reset_index().drop('index', axis =1)

	    #Compute the cost of each error
	    df_cost_curve['cost'] = df_cost_curve.apply(lambda x: error_cost(x.y_pred, x.y_test,costs), axis=1)

	    #Compute the cummulative sum of the costs
	    df_cost_curve['cum_cost'] = df_cost_curve['cost'].cumsum(axis=0)
	    
	    return df_cost_curve

	costs = {
	    'avg_analysis_cost':avg_monitoring_cost ,
	    'avg_fraud_cost':avg_fraud_cost ,
	    'test_ratio':0.25
			}

	

	@st.cache
	def read_model_results():
		return pd.read_csv("https://github.com/milara-ds/streamlit-portfolio-app/blob/main/data/model_results_fd.csv") 

	#Read results of the models 
	df_results = read_model_results() 
	y_test = df_results['y_test']

	#Dummy model 
	dummy_proba = df_results['dummy_proba']
	df_dummy_cost_curve = compute_cost_df(dummy_proba,y_test,0.5,costs)

	#Simple Logistic Regression
	logreg_proba = df_results['logreg_proba']
	df_logreg_cost_curve = compute_cost_df(logreg_proba,y_test,0.5,costs)

	#Simple XGBoost
	xgboost_proba = df_results['xgboost_proba']
	df_xgboost_cost_curve = compute_cost_df(xgboost_proba,y_test,0.5,costs)

	#SMOTE RFE HYP THRS Logistic Regression
	logreg_sm_rfe_hyp_proba = df_results['logreg_sm_rfe_hyp_proba']
	df_logreg_thrs_cost_curve = compute_cost_df(logreg_sm_rfe_hyp_proba,y_test,0.375,costs)

	#SMOTE RFE HYP THRS XGBoost
	xgboost_sm_rfe_hyp_proba = df_results['xgboost_sm_rfe_hyp_proba']
	df_xgboost_thrs_cost_curve = compute_cost_df(xgboost_sm_rfe_hyp_proba,y_test,0.525,costs)

	#values for x axis
	instances=np.arange(0, 1, (1/len(y_test)))

	fig = go.Figure(layout=go.Layout(height=600, width=800))

	fig.add_trace(go.Scatter(x=instances, 
		y=df_dummy_cost_curve['cum_cost'],
		name = 'Dummy classifier'))

	fig.add_trace(go.Scatter(x=instances, 
		y=df_logreg_cost_curve['cum_cost'],
		name = 'Logistic Regression (simple)'))

	fig.add_trace(go.Scatter(x=instances, 
		y=df_logreg_thrs_cost_curve['cum_cost'],
		name = 'Logistic Regression (tunned)'))

	fig.add_trace(go.Scatter(x=instances, 
		y=df_xgboost_cost_curve['cum_cost'],
		name ='XGBoost (simple)' ))

	fig.add_trace(go.Scatter(x=instances, 
		y=df_xgboost_thrs_cost_curve['cum_cost'],
		name = 'XGBoost (tunned)'))


	fig.update_layout(
	    yaxis_title="Cost €",
	    xaxis_title="Instances proportion",
	    title_text= "Cost curve",
	    title_x=0.5,
	    showlegend=True,
	    legend=dict(
		    yanchor="top",
		    y=0.99,
		    xanchor="left",
		    x=0.01)
	    )

	fig.add_hline(y=y_test.sum()*avg_monitoring_cost,
				  line_dash="dot",
	              annotation_text="Perfect classificator", 
	              annotation_position="top right")

	st.plotly_chart(fig, use_container_width=True)


	#5. Plot "Feature Importances"**********************************************************
	st.markdown("## **Feature Importance**")

	st.markdown("Finally, it is important to understand how the models do what they do. One method for this is to get the \
				importance of each feature the model assigns. The plot below shows the ranking of the features of the XGBoost (tunned) model.")

	@st.cache
	def read_feature_importance():
		return pd.read_csv("https://github.com/milara-ds/streamlit-portfolio-app/blob/main/data/xgb_feat_importance_fd.csv") 

	#Read the data of best model
	df_feat = read_feature_importance()

	y = df_feat.columns
	x = df_feat.iloc[0]

	colors = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 
			  'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 
			  'brown', 'burlywood', 'cadetblue', 'deeppink']

	# Use textposition='auto' for direct text
	fig = go.Figure(data=[go.Bar(
	            x=x, 
	            y=y,
	            text=x,
	            textposition='auto',
	            marker_color = colors,
	            orientation='h',
	        )])

	fig.update_layout(
	    yaxis_title="Features",
	    xaxis_title="Score",
	    title_text= "Ranking of features",
	    title_x=0.5,
	    )


	st.plotly_chart(fig, use_container_width=True)


	st.markdown("## **Conclusion**")
	st.markdown("This quick interactive overview of the job of a Data Scientist presented some of the most important tasks when solving a \
		         problem of Fraud Detection. Nevertheless, these tasks are similar to any problem with data. Indeed, there are more \
		         tasks such as cleaning the data and checking that the models are able to make good predictions instead of learning a set of\
		         possible results. For the complete analysis please Jupyter notebook in \
		         my [github](https://github.com/milara-ds/fraud-detection/blob/main/Fraud%20Detection_v1.ipynb).")