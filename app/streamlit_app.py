# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 11:15:32 2024

@author: seford
"""

#import packages required to run the application

import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import plotly.express as px
from viyapy import viya_utils
from scoreModel import scoreModel
import os

#optional - input username
username='seford'

if 'WORKSPACE' in os.environ:
    if os.path.exists(os.environ['WORKSPACE'] + '/cred.json'):
        with open('C:/certs/creds.json') as f:
            creds = json.load(f)
            
        token = creds['verde']['token']

        host=creds['verde']['server_url']

protocol='https'

#base URL for Viya
# baseUrl = protocol + '://' + host + '/'

#the ID of the entire decision flow
decisionID1 = ''

image0 = Image.open('./img/Hallmark_logo.svg.PNG')
st.image(image0,width=500)
#start building the web application using the streamlit components
st.title('Propensity to Purchase')

st.write("This web app predicts the likelihood for a customer to make a purchase")

st.header('Dynamic Model Input')

#user editable features. These variables will store the values of the 
#web components
RecencyScore = st.slider(label = 'RecencyScore', min_value = 0,
                          max_value = 5 ,
                          value = 1,
                          step = 1)

FrequencyScore = st.slider(label = 'FrequencySCore', min_value = 0,
                          max_value = 5 ,
                          value = 1,
                          step = 1)

MonetaryScore = st.slider(label = 'MonetaryScore', min_value = 0,
                          max_value = 5 ,
                          value = 1,
                          step = 1)
  

# st.table(features_df)  

#when user clicks the predict button
if st.button('Predict'):
    
    #call viya
    EM_CLASSIFICATION,EM_PROBABILITY,ERROR = scoreModel(10, 10, 10)
    
    

image_footer = Image.open('./img/SAS_logo2.png')
st.image(image_footer,caption='Powered by SAS',width=100)
#TODO - add footer