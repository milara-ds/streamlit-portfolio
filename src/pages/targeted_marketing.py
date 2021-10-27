import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from streamlit.elements.exception import marshall
from streamlit.legacy_caching.caching import cache
import numpy as np
from plotly.subplots import make_subplots



def write():
    if st.session_state['navigation_current'] == None:
        st.session_state['navigation_current'] = "Targeted Marketing"
        st.session_state['navigation_changed'] = False
    elif (st.session_state['navigation_current'] != "Targeted Marketing"):
        st.session_state['navigation_current'] = "Targeted Marketing"
        st.session_state['navigation_changed'] = True
    elif (st.session_state['navigation_current'] == "Targeted Marketing"):
        st.session_state['navigation_changed'] = False
        
    st.title("Targeted Marketing")
    st.markdown("*Uplift modeling for Targeted Marketing using a large dataset of a French advertising company. \
                The model almost duplicated the gains by targeting only 50% of users compared to the baseline.* **[4 min read]**")
    st.write("---")

    st.markdown("One of the main applications of Machine Learning is to improve the **Targeted Marketing**.\
                Briefly, Targeted Marketing is used to identify customers that most likely will buy a product given they received an incentive. One of the latest\
                techniques applied to this problem is called **Uplift modeling**.")

    st.markdown("This technique uses Machine Learning to  \
                boost the results of randomized trial procedures. In other words, the results of campaign tests are scaled and improved.  \
                **Specifically, the technique identifies the customers that\
                are worth spending money on Targeted Marketing.** The following project with **interactive** figures shows a grasp of how the technique works.")
    
    #---0th plot [dataset]
    st.markdown("### The data and trial procedures")
    st.markdown("First things first, we need data. The data used in this project is from a French advertising company that provides online display advertisements.\
                The data contains 13 million users from a randomized trial procedure collected in two weeks, where 84.6% of \
                 the users were targeted at least once, and the other 15.4% was prevented from being targeted.")
    st.markdown("Each instance has 12 features that were anonymized plus two treatment variables (treatment and exposure) and two \
                target variables (visits and conversion). The features are the information available of the customers.")

    @st.cache
    def read_dataframe():
	    return pd.read_csv("https://raw.githubusercontent.com/milara-ds/streamlit-portfolio-app/main/data/head_dataframe_uplift.csv") 
    
    df_head = read_dataframe()
    st.dataframe(df_head)
    st.markdown("**[Note]**This project is focused only on the results of target variable *conversion* which, for the sake of simplicity, it shows if the customer did or did not\
        purchase the product.")

    #----1st plot [Pie chart with amount of data]---------------------------------------------------------------------
    st.markdown("### Exploratory Data Analysis ")
    st.markdown("The next step is to see the data and understand if it is useful for the model. \
                The following selection box shows a pie chart with the proportion of population that received and didn't receive the treatment.\
                If you change the selection item, you will see the chart of *exposure* and *conversion*.")
    st.markdown("The *exposure* is the second treatment tried by the company and\
                the *conversion* is the target variable (whether the user bought the product or not). Note that this analysis does not consider the visit variable.")

    #Read the dataset
    data = {'treatment': [11454443,2096937] , 'exposure':[428212,13551380], 'conversion':[13938818,40774]}
    choice = st.selectbox('Select the pie chart', ('Treatment', 'Exposure','Conversion'))
    
    if choice == 'Treatment':
        #Plot
        fig = go.Figure(go.Pie(
            name = "",
            values = data['treatment'],
            labels = [ 'Treatment','No treatment'],
            texttemplate = "%{label}: %{value:,.3s} <br> (%{percent}) </br>"
            
        ))

        fig.update_layout( yaxis_title="Number of users with treatment",
                            title_text= "Treatment",
                            title_x=0.5)

        st.plotly_chart(fig, use_container_width=True)
    elif choice == 'Exposure':
        #Plot

        fig = go.Figure(go.Pie(
            name = "",
            values = data['exposure'],
            labels = ['Exposure','No exposure'],
            texttemplate = "%{label}: %{value:,.3s} <br> (%{percent}) </br>"
            
        ))

        fig.update_layout( yaxis_title="Number of users with exposure",
                            title_text= "Exposure",
                            title_x=0.5)

        st.plotly_chart(fig, use_container_width=True)
    elif choice == 'Conversion':
        #Plot
        fig = go.Figure(go.Pie(
            name = "",
            values = data['conversion'],
            labels = ['No conversion', 'Conversion'],
            texttemplate = "%{label}: %{value:,.3s} <br> (%{percent}) </br>",
            
        ))

        fig.update_layout( yaxis_title="Number of users with conversion",
                            title_text= "Conversion",
                            title_x=0.5)

        st.plotly_chart(fig, use_container_width=True)

    #----2nd plot [Checkbox on conversion]---------------------------------------------------------------------
    st.markdown("### Did the treatments work?")
    st.markdown("Then, to give meaning to the data that is shown above it is necessary to analyse if one of the treatments or both (treatment and exposure) \
                did improve the conversion rate. \
                For this, statistical tests are carried out. Do not worry I do not show any technical computations, but I do show the mean of conversion \
                given the *no treatment*, *treatment*, and *exposure*.")
    st.markdown("Check that the mean of conversion of *treatment* does not improve the mean of conversion \
                compared to the mean of conversion of *no treatment*. On the other side, the *exposure treatment* did improve.\
                Try by selecting different population.")
    
    agg_data = {'t1e1_mean': 0.053784, 't1e1_sum': 23031 ,'t1e1_count': 428212,
                't1e0_mean': 0.001194, 't1e0_sum': 13680,'t1e0_count': 11454443,
	            't0e0_mean': 0.001938, 't0e0_sum': 4063 ,'t0e0_count': 2096937} 

    agg_radio = st.radio("Select the type of population:",('No treatment', 'Treatment', 'Exposure'))


    #PRINT aggregate results
    col1, col2, col3 = st.columns(3)

    if agg_radio == 'Treatment': 
        col1.metric("Users Converted", '{:,.0f}'.format(agg_data['t1e0_sum']),  '{:,.0f}'.format(agg_data['t1e0_sum'] - agg_data['t0e0_sum']))
        col2.metric("Total Users", '{:,.0f}'.format(agg_data['t1e0_count']), '{:,.0f}'.format(agg_data['t1e0_count'] - agg_data['t0e0_count']))
        col3.metric("Mean of Conversion", round(agg_data['t1e0_mean'],4), round(agg_data['t1e0_mean'] - agg_data['t0e0_mean'],4))
    elif agg_radio == 'No treatment':
        col1.metric("Users Converted", '{:,.0f}'.format(agg_data['t0e0_sum']))
        col2.metric("Total Users", '{:,.0f}'.format(agg_data['t0e0_count']))
        col3.metric("Mean of Conversion", round(agg_data['t0e0_mean'],4) )
    elif agg_radio == 'Exposure':
        col1.metric("Users Converted", '{:,.0f}'.format(agg_data['t1e1_sum']), '{:,.0f}'.format(agg_data['t1e1_sum'] - agg_data['t0e0_sum']))
        col2.metric("Total Users", '{:,.0f}'.format(agg_data['t1e1_count']), '{:,.0f}'.format(agg_data['t1e1_count'] - agg_data['t0e0_count']))
        col3.metric("Mean of Conversion", round(agg_data['t1e1_mean'],4), round(agg_data['t1e1_mean'] - agg_data['t0e0_mean'],4))


    #----3rd plot [Show data for models?? exposure and conversion??]---------------------------------------------------------------------
    st.markdown("### Data for the models")
    st.markdown("Given the previous results, not all the data is useful for the model. The idea is to only feed the models with the campaign test \
                that worked. Thus, the data used for the following step (modeling) is the population that did and did not receive  the exposure treatment.")
    st.markdown ("The following bar plots shows the conversion of the population that is used for the model.")

    fig = make_subplots(rows=1, cols=2,subplot_titles=("Conversion given not exposure", "Conversion given exposure"))

    colors = ['royalblue','crimson']

    fig.add_trace( go.Bar(
				x=['No conversion', 'Conversion'], 
				y=[2092874,4063],
				textposition='auto',
				marker_color = colors,
                showlegend= False,
                texttemplate = " %{value:,.3s}"
			), row=1, col=1)
    
    fig.add_trace( go.Bar(
                    x=['No conversion', 'Conversion'], 
                    y=[405181,23031] ,
                    textposition='auto',
                    marker_color = colors,
                    showlegend= False,
                    texttemplate = " %{value:,.3s}"
                ), 
                row=1, col=2
    )

    fig.update_layout(height=400, width=900, yaxis_title="Population")

    st.plotly_chart(fig, use_container_width=True)

    #----- 4th plot Show the uplift modeling-----
    st.markdown("### Modeling")
    st.markdown("This is where the magic happens. The selected data is used to train and evaluate the uplift model.")
    st.markdown("The uplift model is nothing more than the difference between the probability of the user to buy the product given that she or he received \
                the treatment minus the probability of the same user given that she or he did not receive the treatment. The higher the uplift the better.")
    st.markdown("This is also known as **Causal Machine Learning**.")
    st.markdown("The following plot shows the cumulative results of two models on 680,000 test instances, where \
                the x axis represents the number of instances processed by the models and y axis the cumulative uplift. ")

    @st.cache
    def read_uplift_results():
	    return pd.read_csv("https://raw.githubusercontent.com/milara-ds/streamlit-portfolio-app/main/data/uplift_results.csv") 
    
    df_up_results = read_uplift_results()

    #values for x axis
    instances=np.arange(0, 1, (1/len(df_up_results)))

    fig = go.Figure(layout=go.Layout(height=600, width=800))

    fig.add_trace(go.Scatter(x=instances, 
		y=df_up_results['gain_twomodel'],
		name = 'Uplift model'))

    fig.add_trace(go.Scatter(x=[0,0.5,1], 
		y=[0,0.0259215,0.051843],
       name = 'Random model'))
    
    #fig.add_vline(x=0.2, line_width=3, line_dash="dash", line_color="green")
    fig.add_vline(x=0.5, line_width=1, line_dash="dash", line_color="black")

    fig.add_vrect(x0="0", x1="0.2", 
              annotation_text="Profile 1", annotation_position="top left",
              fillcolor="blue", opacity=0.07, line_width=0)

    fig.add_vrect(x0="0.2", x1="0.6", 
        annotation_text="Profile 2", annotation_position="top left",
        fillcolor="red", opacity=0.07, line_width=0)

    fig.add_vrect(x0="0.6", x1="1", 
        annotation_text="Profile 3", annotation_position="top left",
        fillcolor="mediumspringgreen", opacity=0.07, line_width=0)

    fig.update_layout(
	    yaxis_title="Uplift",
	    xaxis_title="Instances proportion",
	    title_text= "Cumulative Uplift curve",
	    title_x=0.5,
	    showlegend=True,
	    legend=dict(
		    yanchor="bottom",
		    y=0.01,
		    xanchor="right",
		    x=0.99)
	    ) 

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("The plot of above shows two lines. The blue line presents the cumulative results of the uplift model. In short, the uplift model was used to sort the \
                 population based on their probability of buying the product given that they received the treatment. The first users are the ones with the highest probability\
                 and the last ones with the lowest.")
    
    st.markdown("And the red line shows the baseline model. \
                 Which presents the cumulative uplift given that the users were randomly sorted (no Machine Learning used). \
                 Therefore, the uplift is smaller than the uplift model.")

    st.markdown("Look at the blue highlighted area, the difference between the growth of the curves is huge. Also, the red highlighted area \
                shows the part where both plots are most similar to each other. Finally, the green area shows decrease of the uplift model." )
    
    st.markdown("In other words, the blue area represents the users with the highest probability of buying the product given they received\
                the treatment, the red area represents the users that their probability of buying the product does not change whether they did or did not receive \
                the treatment. Finally, the green area represents the users that if receive the treatment can provide negative impact on the business.\
                This only applies for the uplift model.")

    st.markdown("Moreover, the uplift model almost duplicated the uplift by targeting only 50% of users compared to the baseline. See where both plots intersect \
                the dashed line.")

    st.markdown("**[Key points]**")
    st.markdown("**[Key 1]** The uplift model helps to identify the most persuadable population.")
    st.markdown("**[Key 2]** The uplift model helps to avoid spending on population that will not change their behavior whether they receive \
                or not the incentive.")
    st.markdown("**[Key 3]** The uplift model helps to avoid population that if receive the treatment can provide negative impact on the business.")

    st.markdown("Hence, Uplift modeling provides several benefits for Targeted Marketing.")

    #---5th plot ---profiles------
    st.markdown("### Bonus: How do the three profiles look like?")
    st.markdown("The next radar plot shows the comparison between the median values of the features for each group of profiles. The idea is to highlight the differences between\
        the profiles found.")
    categories = ['f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11']
   
    #Median values
    profile_1 = [-0.9108630125077848, -0.15411908702956328, -0.20216423421989535, 0.08422266441412694, -0.21303824704659052, 0.26413600066507525, -0.21480072414693854, 
                -0.2901967783002336, -1.528229994194157, 1.592912352005471, -0.2436741822118126, 0.13885617130736533]
    profile_2 = [0.953287548552067, -0.15411908702956328, -0.8047864597398902, 0.49682552606034996, -0.21303824704659052, 0.26413600066507525, 0.3546984987345564, 
                -0.2901967783002336, 0.7528650023511599, -0.48437188083960875, -0.2436741822118126, 0.13885617130736533]
    profile_3 = [-0.9126290699436324, -0.15411908702956328, 1.06541232410226, 0.49682552606034996, -0.21303824704659052, 0.26413600066507525, 0.11166610800584308, 
                -0.2901967783002336, 0.3149889266009519, -0.48437188083960875, -0.2436741822118126, 0.13885617130736533]

    #Plot 
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
            r= profile_1,
            theta=categories,
            fill='toself',
            name='Profile 1\'s area'
    ))

    fig.add_trace(go.Scatterpolar(
            r= profile_2,
            theta=categories,
            fill='toself',
            name='Profile 2\'s area'
    ))

    fig.add_trace(go.Scatterpolar(
            r= profile_3,
            theta=categories,
            fill='toself',
            name='Profile 3\'s area'
    ))


    fig.update_layout(
	    title_text= "Radar profiles' curve",
	    title_x=0.5,
	    showlegend=True,

	    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("You can try by clicking on the colors of the labels that are on the upper right corner of the plot to enable and disable the profiles. \
                The profile 1 has the highest differences for the f8 and f9 variables. And profile 2 and profile 3 for the f0 and f2 variables respectively. ")


    st.markdown("### Conclusion")
    st.markdown("In this brief explanation, it was shown how Targeted Marketing is improved with Uplift modeling. Further, the key steps from understanding \
        the data to the modeling were presented. In addition, a bonus was shown. Finally, the takeaways of this project are listed below: ")
    st.markdown("+ To use this technique, it is necessary to perform at least one successful random trail treatment on a group of a population.")
    st.markdown("+ This technique helps you to identify the population that need an incentive to buy product.")
    st.markdown("+ This technique helps you avoid spending money on population that might impact your business.")
    st.markdown("+ This technique is based on Causal Machine Learning.")


    st.write("For the complete analysis click [here](https://github.com/milara-ds/targeted-marketing/blob/main/Uplift_v1.ipynb). If you have any comments \
        or feedback, please reach me out via [LinkedIn](https://www.linkedin.com/in/miguellaradatascientist).")
 