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
    selected_year = st.selectbox('Select Year', [2019, 2014],)

with col2:
    selected_party_catg = st.selectbox('Select Party Category',['National Party','State Party', 'Unrecognised Party'])

with col3:
    sheet = 'Party_List.csv'
    party_name_list = pd.read_csv(str(Path('Data',str(selected_year),sheet)), usecols=['PARTY TYPE','PARTY NAME','ABBREVIATION'])

    party_catg = {'National Party':'N', 'State Party':'S','Unrecognised Party':'U'}
    party_name_list = party_name_list[party_name_list['PARTY TYPE'] == party_catg[selected_party_catg]]
    selected_party = st.selectbox('Select Party',party_name_list['PARTY NAME'].values)

f = open(str(Path('Data',str(selected_year),'Overview.json')))
overview_json = json.load(f)

Constituencies = overview_json['Constituencies']
data = Constituencies.values()
total_constituencies = sum(data)

sheet = 'Party_Wise_Seat_Won.csv'
party_wise_seat_votes = pd.read_csv(str(Path('Data',str(selected_year),sheet)), usecols=['PARTY NAME','STATE NAME','TOTAL VALID VOTES POLLED IN STATE','SEAT WON','TOTAL VALID VOTES POLLED BY PARTY'])
Selected_party_data = party_wise_seat_votes[party_wise_seat_votes['PARTY NAME'] == selected_party]

col4, col5 = st.columns(2)
with col4:
    seat_won = Selected_party_data['SEAT WON'].sum()
    st.metric('Seat Won', seat_won)

with col5:
    st.metric('Seat Won %', round(seat_won/total_constituencies * 100,2), help='Percentage of seat won by party over total seats')

col6, col7 = st.columns(2)
with col6:
    total_vote_get = Selected_party_data['TOTAL VALID VOTES POLLED BY PARTY'].sum()
    st.metric('Total Vote Received',f'{total_vote_get:,}')

with col7:
    Voters = overview_json['Voters']
    data = Voters.values()
    total_vote_polled = sum(data)
    st.metric('Vote %', round(total_vote_get/total_vote_polled * 100,2), help='Percentage of votes received by party over total votes polled in the election.')


# Gender wise distribution of Contestents
st.markdown('### Contestents')

party_abbreviation = party_name_list[party_name_list['PARTY NAME'] == selected_party]['ABBREVIATION'].values[0]
sheet = 'PC_Wise_Result.csv'
Gender_wise_candidates = pd.read_csv(str(Path('Data',str(selected_year),sheet)), usecols=['SEX','PARTY NAME'])
Genderwise_contestent_by_selected_party = Gender_wise_candidates[Gender_wise_candidates['PARTY NAME'] == party_abbreviation]['SEX'].value_counts()

total_contestents = sum(Genderwise_contestent_by_selected_party.values)

col8, col9 = st.columns(2)
with col8:
    st.metric('Number of Contestents', f'{total_contestents:,}')

    if 'MALE' in Genderwise_contestent_by_selected_party.index:
        st.markdown('Male : ' + str(round(Genderwise_contestent_by_selected_party['MALE'] / total_contestents * 100,2)) + '%')

    if 'FEMALE' in Genderwise_contestent_by_selected_party.index:
        st.markdown('Female : ' + str(round(Genderwise_contestent_by_selected_party['FEMALE'] / total_contestents * 100,2)) + '%')

    if 'THIRD' in Genderwise_contestent_by_selected_party.index:
        st.markdown('Third Gender : ' + str(round(Genderwise_contestent_by_selected_party['THIRD'] / total_contestents * 100,2)) + '%')

with col9:
    sns.barplot(x=Genderwise_contestent_by_selected_party.index, y=Genderwise_contestent_by_selected_party.values)
    # plt.grid()
    plt.xlabel('Gender')
    plt.ylabel('Candidate count')
    plt.gca().ticklabel_format(axis='y', style='plain')
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.savefig(Path('Plots/Party_genderwise_candidates.png'),edgecolor='b',bbox_inches='tight')
    plt.close()
    st.image(str(Path('Plots/Party_genderwise_candidates.png')))
    

# Gender wise distribution of winners
st.markdown('### Winners', help='Gender wise seat won over total seat won by a party')

# party_abbreviation = party_name_list[party_name_list['PARTY NAME'] == selected_party]['ABBREVIATION'].values[0]
sheet = 'Successful_Candidate.csv'
Gender_wise_winners = pd.read_csv(str(Path('Data',str(selected_year),sheet)), usecols=['SEX','PARTY'])
Genderwise_winners_by_selected_party = Gender_wise_winners[Gender_wise_winners['PARTY'] == selected_party]['SEX'].value_counts()

if not Genderwise_winners_by_selected_party.empty:
    # Logic to handle parties with no winning seats

    col10, col11 = st.columns(2)
    with col10:

        if 'MALE' in Genderwise_winners_by_selected_party.index:
            st.markdown('Male : ' + str(round(Genderwise_winners_by_selected_party['MALE'] / seat_won * 100,2)) + '%')

        if 'FEMALE' in Genderwise_winners_by_selected_party.index:
            st.markdown('Female : ' + str(round(Genderwise_winners_by_selected_party['FEMALE'] / seat_won * 100,2)) + '%')

        if 'THIRD' in Genderwise_winners_by_selected_party.index:
            st.markdown('Third Gender : ' + str(round(Genderwise_winners_by_selected_party['THIRD'] / seat_won * 100,2)) + '%')

    with col11:
        sns.barplot(x=Genderwise_winners_by_selected_party.index, y=Genderwise_winners_by_selected_party.values)
        # plt.grid()
        plt.xlabel('Gender')
        plt.ylabel('Winner count')
        plt.gca().ticklabel_format(axis='y', style='plain')
        plt.xticks(fontsize=13)
        plt.yticks(fontsize=13)
        plt.savefig(Path('Plots/Party_genderwise_winners.png'),edgecolor='b',bbox_inches='tight')
        plt.close()
        st.image(str(Path('Plots/Party_genderwise_winners.png')))

else:
    st.markdown("#### :red[Party has won no seats.]")