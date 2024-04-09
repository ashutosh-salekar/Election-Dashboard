import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json

st.set_page_config(page_title="Election Dashboard", page_icon="📈", layout="wide")
st.sidebar.image('EC_Logo4.png', width=250)
st.sidebar.write('*For Educational Purposes Only.')

col_head, col_flag = st.columns(2)
with col_head:
    st.header('Loksabha Election Dashboard')
with col_flag:
    st.image('India_Flag.jpg',width=300)

st.markdown('')
st.markdown('')

col1, col2, col3 = st.columns(3)

with col1:
    selected_year = st.selectbox('Select Year', [2019, 2014])

with col2:
    sheet = 'State_Wise_Seat_Won.csv'
    state_data = pd.read_csv(str(Path('Data',str(selected_year),sheet)), usecols=['STATE NAME', 'PARTY TYPE', 'PARTY NAME', 'SEATS WON'])
    
    selected_state = st.selectbox('Select State',state_data['STATE NAME'].unique())

with col3:
    sheet = 'PC_Wise_Result.csv'
    Constituency_data = pd.read_csv(str(Path('Data',str(selected_year),sheet)))
    Constituency_data = Constituency_data[Constituency_data['STATE NAME'] == selected_state]

    selected_constituency = st.selectbox('Select Constituency',Constituency_data['PC NAME'].unique())

Constituency_data = Constituency_data[Constituency_data['PC NAME'] == selected_constituency]
Constituency_data.sort_values(by='TOTAL VOTES', ascending=False, inplace=True)

st.markdown('### Top 5 Performers In The Constituency')
st.dataframe(Constituency_data[['CANDIDATES NAME','SEX','AGE','PARTY NAME','TOTAL VOTES']].head().reset_index(drop=True).set_axis(range(1, 6)))


# Voter turn Out

sheet = 'PC_Wise_Voters_Turnout.csv'
Gender_wise_electors = pd.read_csv(str(Path('Data',str(selected_year),sheet)))

selected_constituency_data = Gender_wise_electors[Gender_wise_electors['PC NAME'] == selected_constituency][['VOTER TURN OUT %']]

st.metric('Voter turn Out %',round(int(selected_constituency_data.values[0]),2))