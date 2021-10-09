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


st.title("Fraud Detection")
st.write("---")

st.write("Working on the page...")