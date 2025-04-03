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
from score_rf import score_rf_model


def set_values_for_player():
    player_select_val = st.session_state['player_select']
    if player_select_val != '':
        vals = df.loc[df.Name == player_select_val]
        
        pos_idx = positions.index(vals['Position'].item())
        div_idx = divisions.index(vals['Div'].item())
        st.session_state['Position'] = positions[pos_idx]
        st.session_state['Div'] = divisions[div_idx]
        
        st.session_state['CrAtBat'] = int(vals['CrAtBat'].item())
        st.session_state['CrBB'] = int(vals['CrBB'].item())
        st.session_state['CrHits'] = int(vals['CrHits'].item())
        st.session_state['CrHome'] = int(vals['CrHome'].item())
        st.session_state['CrRbi'] = int(vals['CrRbi'].item())
        st.session_state['CrRuns'] = int(vals['CrRuns'].item())
        st.session_state['nAssts'] = int(vals['nAssts'].item())
        st.session_state['nAtBat'] = int(vals['nAtBat'].item())
        st.session_state['nBB'] = int(vals['nBB'].item())
        st.session_state['nError'] = int(vals['nError'].item())
        st.session_state['nHits'] = int(vals['nHits'].item())
        st.session_state['nHome'] = int(vals['nHome'].item())
        st.session_state['nOuts'] = int(vals['nOuts'].item())
        st.session_state['nRBI'] = int(vals['nRBI'].item())
        st.session_state['nRuns'] = int(vals['nRuns'].item())
        st.session_state['YrMajor'] = int(vals['YrMajor'].item())
        st.session_state['CrAtBat'] = int(vals['CrAtBat'].item())
        


#load the base data set
df = pd.read_csv('https://shai-alit.github.io/sas-CA-examples/Data/baseball.csv')

#drop rows with missing data
df = df.dropna()

df_stat = df.describe()


#compute mean by division
div_mean = df.groupby('Div').mean(numeric_only=True)

#compute mean by position
position_mean = df.groupby('Position').mean(numeric_only=True)

#compute mean by division and position
avg_by_div_pos = df.groupby(['Div','Position']).mean(numeric_only=True)



positions = list(set(df.Position))
positions.sort()
divisions = list(set(df.Div))
divisions.sort()
players = ['']
players.extend(list(df.Name))
players.sort()

#optional - input username
username='seford'

# with open('C:/certs/creds.json') as f:
#     creds = json.load(f)
    
# token = creds['verde']['token']

# host=creds['verde']['server_url']

protocol='https'

#base URL for Viya
# baseUrl = protocol + '://' + host + '/'

#the module ID. This is the name of the decision flow that was saved to MAS
moduleID1 = "Baseball Salary 21_1"

#the ID of the entire decision flow
decisionID1 = 'c9e22367-af5e-4385-b58a-69fa945f21e9'


# st.set_page_config(layout="wide")

#start building the web application using the streamlit components
st.title('1986 MLB Salary Prediction')

image0 = Image.open('./img/baseball_img.PNG')
st.image(image0)

st.write("This web app predicts an MLB player's 1987 salary given their stats up through the 1986 season.")
st.write("Model:  **Python Random Forest**")

st.sidebar.write('**Model Inputs**')

player_select = st.sidebar.selectbox(label='Player',options=players,index=0,key='player_select',on_change=set_values_for_player)

Div = st.sidebar.selectbox(label='Division',options=divisions,index=0,key='Div')

Position = st.sidebar.selectbox(label='Position',options=positions,index=0,key='Position')

CrAtBat = st.sidebar.slider('Career at Bats',key='CrAtBat',min_value=int(df_stat['CrAtBat']['min']),
                    max_value=int(df_stat['CrAtBat']['max']),
                    value=int(df_stat['CrAtBat']['mean']),step=1)

CrBB = st.sidebar.slider('Career Walks',key='CrBB',min_value=int(df_stat['CrBB']['min']),
                    max_value=int(df_stat['CrBB']['max']),
                    value=int(df_stat['CrBB']['mean']),step=1)

CrHits = st.sidebar.slider('Career Hits',key='CrHits',min_value=int(df_stat['CrHits']['min']),
                    max_value=int(df_stat['CrHits']['max']),
                    value=int(df_stat['CrHits']['mean']),step=1)

CrHome = st.sidebar.slider('Career Home Runs',key='CrHome',min_value=int(df_stat['CrHome']['min']),
                    max_value=int(df_stat['CrHome']['max']),
                    value=int(df_stat['CrHome']['mean']),step=1)

CrRbi = st.sidebar.slider('Career RBIs',key='CrRbi',min_value=int(df_stat['CrRbi']['min']),
                    max_value=int(df_stat['CrRbi']['max']),
                    value=int(df_stat['CrRbi']['mean']),step=1)

CrRuns = st.sidebar.slider('Career Runs',key='CrRuns',min_value=int(df_stat['CrRuns']['min']),
                    max_value=int(df_stat['CrRuns']['max']),
                    value=int(df_stat['CrRuns']['mean']),step=1)

nAssts = st.sidebar.slider('1986 - Num Assists',key='nAssts',min_value=int(df_stat['nAssts']['min']),
                    max_value=int(df_stat['nAssts']['max']),
                    value=int(df_stat['nAssts']['mean']),step=1)

nAtBat = st.sidebar.slider('1986 - Num At Bat',key='nAtBat',min_value=int(df_stat['nAtBat']['min']),
                    max_value=int(df_stat['nAtBat']['max']),
                    value=int(df_stat['nAtBat']['mean']),step=1)

nBB = st.sidebar.slider('1986 - Num Walks',key='nBB',min_value=int(df_stat['nBB']['min']),
                    max_value=int(df_stat['nBB']['max']),
                    value=int(df_stat['nBB']['mean']),step=1)

nError = st.sidebar.slider('1986 - Num Errors',key='nError',min_value=int(df_stat['nError']['min']),
                    max_value=int(df_stat['nError']['max']),
                    value=int(df_stat['nError']['mean']),step=1)

nHits = st.sidebar.slider('1986 - Num Hits',key='nHits',min_value=int(df_stat['nHits']['min']),
                    max_value=int(df_stat['nHits']['max']),
                    value=int(df_stat['nHits']['mean']),step=1)

nHome = st.sidebar.slider('1986 - Num Home Runs',key='nHome',min_value=int(df_stat['nHome']['min']),
                    max_value=int(df_stat['nHome']['max']),
                    value=int(df_stat['nHome']['mean']),step=1)

nOuts = st.sidebar.slider('1986 - Num Put Outs',key='nOuts',min_value=int(df_stat['nOuts']['min']),
                    max_value=int(df_stat['nOuts']['max']),
                    value=int(df_stat['nOuts']['mean']),step=1)

nRBI = st.sidebar.slider('1986 - Num RBIs',key='nRBI',min_value=int(df_stat['nRBI']['min']),
                    max_value=int(df_stat['nRBI']['max']),
                    value=int(df_stat['nRBI']['mean']),step=1)


nRuns = st.sidebar.slider('1986 - Num Runs',key='nRuns',min_value=int(df_stat['nRuns']['min']),
                    max_value=int(df_stat['nRuns']['max']),
                    value=int(df_stat['nRuns']['mean']),step=1)


YrMajor = st.sidebar.slider('Years in Majors',key='YrMajor',min_value=int(df_stat['YrMajor']['min']),
                    max_value=int(df_stat['YrMajor']['max']),
                    value=int(df_stat['YrMajor']['mean']),step=1)


    
features = {
'CrAtBat':CrAtBat,
'CrBB':CrBB,
'CrHits':CrHits,
'CrHome':CrHome,
'CrRbi':CrRbi,
'CrRuns':CrRuns,
'nAssts':nAssts,
'nAtBat':nAtBat,
'nBB' :nBB,
'nError':nError,
'nHits':nHits,
'nHome':nHome,
'nOuts':nOuts,
'nRBI':nRBI,
'nRuns':nRuns,
'YrMajor':YrMajor}
 
#create data frame to display values in a table
features_df  = pd.DataFrame([features])
  

# st.table(features_df)  

#when user clicks the predict button
if st.button('Predict'):
    
    #call viya
    P_logSalary = score_rf_model(nAtBat, nHits, nHome, nRuns, nRBI, nBB, YrMajor,
           CrAtBat, CrHits, CrHome, CrRuns, CrRbi, CrBB, nOuts,
           nAssts, nError)
    
    
    
    #get the mean salary for the given position
    mean_salary_by_position = position_mean.loc[Position]['Salary']

    #get the mean salary for the given division
    mean_salary_by_division = div_mean.loc[Div]['Salary']

    #get the mean salary for the given division and position
    mean_salary_by_div_pos = avg_by_div_pos.loc[Div,Position]['Salary']
    
    st.subheader('Prediction Results')
    
    pred_salary_dollars = 1000*np.exp(P_logSalary)
    st.write(f'Suggested Salary: ${pred_salary_dollars:,.0f}')
    
       
    df_graph = pd.DataFrame(columns = ['Idx','Label','Salary'], 
                            data = [[0,'Mean by Div,Pos',int(1000*mean_salary_by_div_pos)],
                                     [1,'Mean by Position',int(1000*mean_salary_by_position)],
                                     [2,'Mean by Division',int(1000*mean_salary_by_division)]])
    
    fig = px.bar(df_graph, x='Label', y='Salary',text="Label")
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(xaxis_title=None)
    fig.add_hline(y=pred_salary_dollars,annotation_text='Suggested Salary',line_color='red')
    # fig.add_shape(
    # type='line',
    # x0=0,
    # x1=1,
    # y0=pred_salary_dollars,
    # y1=pred_salary_dollars,
    # xref='paper',
    # yref='y',
    # line=dict(color='red', width=2))
    st.plotly_chart(fig, use_container_width=True)
    
    
    # if len(model_list) > 0:
    #     model_list.index.name = 'Model Count'
    #     st.write("Current Model Information")
    #     st.dataframe(model_list)




image_footer = Image.open('./img/SAS_logo2.png')
st.image(image_footer,caption='Powered by SAS',width=100)
#TODO - add footer