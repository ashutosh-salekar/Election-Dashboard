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

col1, col2 = st.columns(2)
with col1:
    selected_year = st.selectbox('Select Year', [2019, 2014])

with col2:
    sheet = 'State_Wise_Seat_Won.csv'
    state_data = pd.read_csv(str(Path('Data',str(selected_year),sheet)), usecols=['STATE NAME', 'PARTY TYPE', 'PARTY NAME', 'SEATS WON'])
    
    selected_state = st.selectbox('Select State',state_data['STATE NAME'].unique())

seats_in_selected_state = state_data[state_data['STATE NAME'] == selected_state]['SEATS WON'].sum()
st.markdown(f'### Constituencies in {selected_state}')
st.markdown(f'### {int(seats_in_selected_state)}')


st.markdown('### Party Wise Seat Won')

col3, col4 = st.columns(2)
with col3:
    seat_won_data = state_data[(state_data['STATE NAME'] == selected_state) & (state_data['SEATS WON'] > 0)][['PARTY NAME','PARTY TYPE','SEATS WON']].sort_values(by='SEATS WON', ascending=False).head(5)
    st.dataframe(seat_won_data, hide_index=True)

with col4:
    plt.pie(seat_won_data['SEATS WON'], autopct='%1.1f%%')
    plt.legend(seat_won_data['PARTY NAME'], bbox_to_anchor = (1,1))
    plt.savefig(Path('Plots/State_party_seat_won.png'),edgecolor='b',bbox_inches='tight')
    plt.close()
    st.image(str(Path('Plots/State_party_seat_won.png')))



st.markdown('### Contestents')

sheet = 'PC_Wise_Result.csv'
Gender_wise_candidates = pd.read_csv(str(Path('Data',str(selected_year),sheet)), usecols=['SEX','STATE NAME'])
Genderwise_candidates_in_selected_state = Gender_wise_candidates[Gender_wise_candidates['STATE NAME'] == selected_state]['SEX'].value_counts()

total_contestents = sum(Genderwise_candidates_in_selected_state.values)

col5, col6 = st.columns(2)
with col5:

    if 'MALE' in Genderwise_candidates_in_selected_state.index:
        st.markdown('Male : ' + str(round(Genderwise_candidates_in_selected_state['MALE'] / total_contestents * 100,2)) + '%')

    if 'FEMALE' in Genderwise_candidates_in_selected_state.index:
        st.markdown('Female : ' + str(round(Genderwise_candidates_in_selected_state['FEMALE'] / total_contestents * 100,2)) + '%')

    if 'THIRD' in Genderwise_candidates_in_selected_state.index:
        st.markdown('Third Gender : ' + str(round(Genderwise_candidates_in_selected_state['THIRD'] / total_contestents * 100,2)) + '%')

with col6:
    sns.barplot(x=Genderwise_candidates_in_selected_state.index, y=Genderwise_candidates_in_selected_state.values)
    # plt.grid()
    plt.xlabel('Gender', fontsize=15)
    plt.ylabel('Candidate count', fontsize=15)
    plt.gca().ticklabel_format(axis='y', style='plain')
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.savefig(Path('Plots/State_genderwise_candidates.png'),edgecolor='b',bbox_inches='tight')
    plt.close()
    st.image(str(Path('Plots/State_genderwise_candidates.png')))



st.markdown('### Winners', help='Percentage of gender wise winners over total seats in the state')

sheet = 'Successful_Candidate.csv'
Gender_wise_winners = pd.read_csv(str(Path('Data',str(selected_year),sheet)), usecols=['SEX','STATE'])
Genderwise_winners_by_selected_state = Gender_wise_winners[Gender_wise_winners['STATE'] == selected_state]['SEX'].value_counts()

col7, col8 = st.columns(2)
with col7:

    if 'MALE' in Genderwise_winners_by_selected_state.index:
        st.markdown('Male : ' + str(round(Genderwise_winners_by_selected_state['MALE'] / seats_in_selected_state * 100,2)) + '%')

    if 'FEMALE' in Genderwise_winners_by_selected_state.index:
        st.markdown('Female : ' + str(round(Genderwise_winners_by_selected_state['FEMALE'] / seats_in_selected_state * 100,2)) + '%')

    if 'THIRD' in Genderwise_winners_by_selected_state.index:
        st.markdown('Third Gender : ' + str(round(Genderwise_winners_by_selected_state['THIRD'] / seats_in_selected_state * 100,2)) + '%')

with col8:
    sns.barplot(x=Genderwise_winners_by_selected_state.index, y=Genderwise_winners_by_selected_state.values)
    # plt.grid()
    plt.xlabel('Gender', fontsize=15)
    plt.ylabel('Winner count', fontsize=15)
    plt.gca().ticklabel_format(axis='y', style='plain')
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.savefig(Path('Plots/State_genderwise_winners.png'),edgecolor='b',bbox_inches='tight')
    plt.close()
    st.image(str(Path('Plots/State_genderwise_winners.png')))


st.markdown('### Electors')

sheet = 'Voters_Information.csv'
Gender_wise_electors = pd.read_csv(str(Path('Data',str(selected_year),sheet)), usecols=['STATE NAME','ELECTOR_MALE','ELECTOR_FEMALE','ELECTOR_THIRD GENDER','VOTER_MALE','VOTER_FEMALE','VOTER_THIRD GENDER','NOTA VOTES'])
Gender_wise_electors = Gender_wise_electors[Gender_wise_electors['STATE NAME'] == selected_state]

data = Gender_wise_electors[['ELECTOR_MALE','ELECTOR_FEMALE','ELECTOR_THIRD GENDER']].values.reshape(3,1)
index = ['Male','Female','Third Gender']
df = pd.DataFrame(data=data, index=index, columns=['Population'])

total_electors = int(sum(data))

col9, col10 = st.columns(2)
with col9:
    st.markdown('Total Electors: '+ f'{total_electors:,}')
    st.markdown('Male: '+ str(round(df.loc['Male'][0] / total_electors * 100,2)) + '%')
    st.markdown('Female: '+ str(round(df.loc['Female'][0] / total_electors * 100,2)) + '%')
    st.markdown('Third Gender: '+ str(round(df.loc['Third Gender'][0] / total_electors * 100,2)) + '%')

with col10:
    sns.barplot(x=df.index, y='Population', data=df)
    # plt.grid()
    plt.xlabel('Gender', fontsize=15)
    plt.ylabel('Elector count', fontsize=15)
    plt.gca().ticklabel_format(axis='y', style='plain')
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.savefig(Path('Plots/State_elector_distribution.png'),edgecolor='b',bbox_inches='tight')
    st.image(str(Path('Plots/State_elector_distribution.png')))
    plt.close()


st.markdown('### Voters')

data = Gender_wise_electors[['VOTER_MALE','VOTER_FEMALE','VOTER_THIRD GENDER']].values.reshape(3,1)
index = ['Male','Female','Third Gender']
df = pd.DataFrame(data=data, index=index, columns=['Population'])

total_voters = int(sum(data))

col11, col12 = st.columns(2)
with col11:
    st.markdown('Total Voters: '+ f'{total_voters:,}')
    st.markdown('Male: '+ str(round(df.loc['Male'][0] / total_voters * 100,2)) + '%')
    st.markdown('Female: '+ str(round(df.loc['Female'][0] / total_voters * 100,2)) + '%')
    st.markdown('Third Gender: '+ str(round(df.loc['Third Gender'][0] / total_voters * 100,2)) + '%')

with col12:
    sns.barplot(x=df.index, y='Population', data=df)
    # plt.grid()
    plt.xlabel('Gender', fontsize=15)
    plt.ylabel('Voter count', fontsize=15)
    plt.gca().ticklabel_format(axis='y', style='plain')
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.savefig(Path('Plots/State_voter_distribution.png'),edgecolor='b',bbox_inches='tight')
    st.image(str(Path('Plots/State_voter_distribution.png')))
    plt.close()


st.markdown('### NOTA Votes')

col13, col14 = st.columns(2)
with col13:
    NOTA_votes = Gender_wise_electors['NOTA VOTES'].values[0]
    st.metric('NOTA Count',f'{NOTA_votes:,}')
with col14:
    st.metric('NOTA Percentage',str(round(NOTA_votes / total_voters * 100,2)) + ' %')