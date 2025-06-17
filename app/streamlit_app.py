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
import json
import settings
import requests
import traceback

def gen_viya_inputs(feature_dict):
    ret_string = None
    feature_list = []
    try:
        for k,v in feature_dict.items():
            if type(v) == str:
                feature_list.append(f'{{"name": "{k}_", "value" : "{v}"}}')
            else:
                feature_list.append(f'{{"name": "{k}_", "value" : {v}}}')
                
        feature_str = str.join(',',feature_list)
        
        ret_string ='{"inputs" : [' + feature_str + ']}'
    except Exception as e:
        msg = f'Error in gen_viya_inputs function: \n{e} \n {traceback.extract_tb(e.__traceback__)}'
        print(msg)
        
    return ret_string

def post(url1, contentType, accept, accessToken, body):
    req = None
    try:
        sess = requests.Session()
        
        headers = {"Accept": accept,
        "Authorization": "bearer " + accessToken,
        "Content-Type": contentType }
        
        # Convert the request body to a JSON object.
        reqBody = json.loads(body)
        
        # Post the request.
        req = sess.post(url1, json=reqBody, headers=headers, verify=False)
        
        #clean up
        sess.close()
    except Exception as e:
        msg = f'Error in post function: \n{e} \n {traceback.extract_tb(e.__traceback__)}'
        print(msg)
    
    return req

def call_id_api(baseUrl, accessToken, feature_dict,moduleID):
    r_j = None
    
    try:
        #create the request in format viya wants
        requestBody = gen_viya_inputs(feature_dict)
    
        # Define the content and accept types for the request header.
        contentType = "application/json"
        acceptType = "application/json"
        
        # Define the request URL.
        masModuleUrl = "/microanalyticScore/modules/" + moduleID
        requestUrl = baseUrl + masModuleUrl + "/steps/execute"
        
        # Execute the decision.
        masExecutionResponse = post(requestUrl, contentType,
         acceptType, accessToken, requestBody)
        
        r_j = json.loads(masExecutionResponse.content)
    except Exception as e:
        msg = f'Error in call_id_api function: \n{e} \n {traceback.extract_tb(e.__traceback__)}'
        print(msg)
    
    return r_j

#optional - input username
username='seford'

if 'st.secrets.token' not in locals():
    if 'WORKSPACE' in os.environ:
        WORKSPACE = os.environ['WORKSPACE']
    else:
        WORKSPACE = 'C:/certs'
        
    if os.path.exists(WORKSPACE + '/creds.json'):
        with open('C:/certs/creds.json') as f:
            creds = json.load(f)
            
        st.secrets.token = creds['verde']['token']
    
        st.secrets.host = creds['verde']['server_url']
        
else:
    token = st.secrets.token
    host = st.secrets.host
    os.environ['REQUESTS_CA_BUNDLE'] = './rainbowtrustedcert24.pem'

token = st.secrets.token
host = st.secrets.host

protocol='https'

#base URL for Viya
baseUrl = protocol + '://' + host + '/'

#the module ID. This is the name of the decision flow that was saved to MAS
moduleID_prefix = 'Propensity'


#the ID of the entire decision flow
decisionID1 = '8daf7f69-5e3e-4eb9-a0a5-0423fcf64fb2'


image0 = Image.open(settings.img_loc + '/1800flowers_logo.png')
st.image(image0,width=250)
#start building the web application using the streamlit components
#UPDATE_LOC = 'Viya Workbench'
#UPDATE_LOC = 'Viya Enterprise'
#UPDATE_LOC = 'VS Code Desktop'
#UPDATE_LOC = 'Spyder Desktop'
UPDATE_LOC = 'SAS Enterprise Guide'
st.write(f'This app was last updated in {UPDATE_LOC}')

st.title('Propensity to Purchase')

st.write("This web app predicts the likelihood for a customer to make a purchase")

def on_change():
    st.session_state.disabled = not st.session_state.disabled
    print(st.session_state.disabled)
    
def get_revisions(baseUrl,decisionId,accessToken):
    r_j = None
    try:
        #create the header
        headers = {
            'Accept': "application/json, application/vnd.sas.collection+json, application/vnd.sas.error+json",
            "Authorization": "bearer " + accessToken
            }
        
        #set up the URL
        requestUrl = baseUrl + '/decisions/flows/' + decisionId + '/revisions'
        
        #make the request
        r = requests.get(requestUrl, headers = headers)
        
        #return the result as a dictionary
        r_j = r.json()
    except Exception as e:
        msg = f'Error in get_decision_content function: \n{e} \n {traceback.extract_tb(e.__traceback__)}'
        print(msg)
        
    
    return r_j
    
    
if "disabled" not in st.session_state:
    st.session_state.disabled = True
    #response = get_revisions(baseUrl,decisionID1,token)
    revisions = ['1.0','2.0','3.0']
    #for i_ in response['items']:
        #revisions.append(str(i_['majorRevision']) + '.' + str(i_['minorRevision']))
    st.session_state.revisions = revisions
        
selected_orch_tool = st.selectbox(label='Select an Orchestration Tool',options=['GitHub','SAS Viya'],index=0,on_change=on_change)
selected_flow_version = st.selectbox(label='Select a version',options=st.session_state.revisions,index=len(st.session_state.revisions)-1,disabled=st.session_state.disabled)
use_py_model = st.checkbox(label='Use Python Model',disabled=st.session_state.disabled)

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

    Purchase_Chance = ''
    output_dict = {}
    
    #call viya
    
    if selected_orch_tool == 'GitHub':
        EM_CLASSIFICATION,EM_PROBABILITY,ERROR = scoreModel(RecencyScore, FrequencyScore, MonetaryScore)
    else:
        
        
        moduleID1 = moduleID_prefix + selected_flow_version.replace('.','_')
        
        if float(selected_flow_version) > 2:
            
            if use_py_model:
                model_to_run = 1
            else:
                model_to_run = -1
            
            #capture the variable values in a dictionary
            features = {'RecencyScore': RecencyScore,
                    'FrequencySCore': FrequencyScore,
                    'MonetaryScore': MonetaryScore,
                    'model_to_run':model_to_run
                    }
        else:

            #capture the variable values in a dictionary
            features = {'RecencyScore': RecencyScore,
                    'FrequencySCore': FrequencyScore,
                    'MonetaryScore': MonetaryScore
                    }

        #create data frame to display values in a table
        features_df  = pd.DataFrame([features])
    
        
        #call viya
        response = call_id_api(baseUrl, token, features, moduleID1)
    
        #get the response
        output_dict = viya_utils.unpack_viya_outputs(response)
        
        EM_CLASSIFICATION = output_dict['EM_CLASSIFICATION'].strip()
        EM_PROBABILITY = output_dict['EM_PROBABILITY']
        Purchase_Chance = output_dict['Purchase_Chance']
    
    print(EM_CLASSIFICATION == '0')
    if EM_CLASSIFICATION == '1' or EM_CLASSIFICATION == 1:
        str_output = f':blue[{Purchase_Chance}. Customer predicted to purchase with probability of {round(100*EM_PROBABILITY,2)}%]'
    else:
        str_output = f':red[{Purchase_Chance}. Customer predicted to NOT purchase with probability of {round(100*EM_PROBABILITY,2)}%]'
        if 'recommendation' in output_dict and output_dict['recommendation'] != '':
            str_output += output_dict['recommendation']
        
    st.write(str_output)


image_footer = Image.open(settings.img_loc + '/SAS_logo2.png')
st.image(image_footer,caption='Powered by SAS',width=100)
#TODO - add footer
