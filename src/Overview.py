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

# Performance of several parties in elections
st.markdown('### Performance Of Several Parties In Loksabha Elections')
sheet = 'Party_Seat_Won.csv'
data = pd.read_csv(str(Path('Data',sheet)))
parties_to_show = ['Communist Party of India (Marxist)', 'Indian National Congress','Bharatiya Janata Party',
       'Biju Janata Dal','Shiv Sena','All India Trinamool Congress']

plt.figure(figsize=(13,5))
for col in parties_to_show:
    plt.plot(data['Year'].values, data[col].values, label=col)

plt.xlabel('Year', fontsize=15)
plt.ylabel('Seats won by Parties', fontsize=15)
plt.xticks(data['Year'].values, rotation = 50, fontsize=13)
plt.yticks(fontsize=13)
# plt.gca().ticklabel_format(axis='y', style='plain')
plt.legend()
plt.savefig(Path('Plots/Overview_party_seat_won.png'),edgecolor='b',bbox_inches='tight')
plt.close()
st.image(str(Path('Plots/Overview_party_seat_won.png')))

st.markdown('')
st.markdown('')

col1, col2 = st.columns(2)
with col1:
    st.markdown('## Year Wise Analysis')
with col2:
    selected_year = st.selectbox('Select Year', [2019, 2014])


# Read Overview Json file
f = open(str(Path('Data',str(selected_year),'Overview.json')))
overview_json = json.load(f)


st.markdown('### Constituencies')

Constituencies = overview_json['Constituencies']
data = Constituencies.values()
index = Constituencies.keys()
df = pd.DataFrame(data=data, index=index, columns=['Population'])

total_constituencies = sum(data)

col4, col5 = st.columns(2)
with col4:
    st.metric('Number of Constituencies', total_constituencies)

    st.markdown('General : ' + str(round(Constituencies['General'] / total_constituencies * 100,2)) + '%')
    st.markdown('SC : ' + str(round(Constituencies['SC'] / total_constituencies * 100,2)) + '%')
    st.markdown('ST : ' + str(round(Constituencies['ST'] / total_constituencies * 100,2)) + '%')

with col5:
    sns.barplot(x=df.index, y='Population', data=df)
    # plt.grid()
    plt.xlabel('Caste', fontsize=15)
    plt.ylabel('Constituencies count', fontsize=15)
    plt.gca().ticklabel_format(axis='y', style='plain')
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.savefig(Path('Plots/Overview_constituencies_graph.png'),edgecolor='b',bbox_inches='tight')
    st.image(str(Path('Plots/Overview_constituencies_graph.png')))
    plt.close()



st.markdown('### Winners')

Winners = overview_json['Winners']
data = Winners.values()
index = Winners.keys()
df = pd.DataFrame(data=data, index=index, columns=['Population'])

col6,col7 = st.columns(2)
with col6:
    st.markdown('Male: ' + str(round(Winners['Male'] / total_constituencies * 100,2)) + '%')
    st.markdown('Female: ' + str(round(Winners['Female'] / total_constituencies * 100,2)) + '%')
    st.markdown('Third Gender: ' + str(round(Winners['Third Gender'] / total_constituencies * 100,2)) + '%')

with col7:
    sns.barplot(x=df.index, y='Population', data=df)
    # plt.grid()
    plt.xlabel('Gender', fontsize=15)
    plt.ylabel('Winning Candidate count', fontsize=15)
    plt.gca().ticklabel_format(axis='y', style='plain')
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.savefig(Path('Plots/Overview_winners_graph.png'),edgecolor='b',bbox_inches='tight')
    st.image(str(Path('Plots/Overview_winners_graph.png')))
    plt.close()

st.markdown('### Contestents')

Contestents = overview_json['Contestents']
data = Contestents.values()
index = Contestents.keys()
df = pd.DataFrame(data=data, index=index, columns=['Population'])

total_contestents = sum(data)

col8, col9 = st.columns(2)
with col8:
    st.metric('Number of Contestents', f'{total_contestents:,}')

    st.markdown('Male : ' + str(round(Contestents['Male'] / total_contestents * 100,2)) + '%')
    st.markdown('Female : ' + str(round(Contestents['Female'] / total_contestents * 100,2)) + '%')
    st.markdown('Third Gender : ' + str(round(Contestents['Third Gender'] / total_contestents * 100,2)) + '%')

with col9:
    sns.barplot(x=df.index, y='Population', data=df)
    # plt.grid()
    plt.xlabel('Gender', fontsize=15)
    plt.ylabel('Candidate count', fontsize=15)
    plt.gca().ticklabel_format(axis='y', style='plain')
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.savefig(Path('Plots/Overview_candidate_graph.png'),edgecolor='b',bbox_inches='tight')
    st.image(str(Path('Plots/Overview_candidate_graph.png')))
    plt.close()



st.markdown('### Electors', help='A elector is a person who is qualified to vote in an election.')

Electors = overview_json['Electors']
data = Electors.values()
index = Electors.keys()
df = pd.DataFrame(data=data, index=index, columns=['Population'])

total_electors = sum(data)

col10, col11 = st.columns(2)
with col10:
    st.metric('Total Electors', f'{total_electors:,}')

    st.markdown('Male : ' + str(round(Electors['Male'] / total_electors * 100,3)) + '%')
    st.markdown('Female : ' + str(round(Electors['Female'] / total_electors * 100,3)) + '%')
    st.markdown('Third Gender : ' + str(round(Electors['Third Gender'] / total_electors * 100,3)) + '%')

with col11:
    sns.barplot(x=df.index, y='Population', data=df)
    # plt.grid()
    plt.xlabel('Gender', fontsize=15)
    plt.ylabel('Elector count', fontsize=15)
    plt.gca().ticklabel_format(axis='y', style='plain')
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.savefig(Path('Plots/Overview_elector_graph.png'),edgecolor='b',bbox_inches='tight')
    st.image(str(Path('Plots/Overview_elector_graph.png')))
    plt.close()



st.markdown('### Voters', help='A voter in an election is an individual who casts a vote to their choice for a candidate.')

Voters = overview_json['Voters']
data = Voters.values()
index = Voters.keys()
df = pd.DataFrame(data=data, index=index, columns=['Population'])

total_voters = sum(data)

col12, col13 = st.columns(2)
with col12:
    st.metric('Total Voters', f'{total_voters:,}')

    st.markdown('Male : ' + str(round(Voters['Male'] / total_voters * 100,3)) + '%')
    st.markdown('Female : ' + str(round(Voters['Female'] / total_voters * 100,3)) + '%')
    st.markdown('Third Gender : ' + str(round(Voters['Third Gender'] / total_voters * 100,3)) + '%')

with col13:
    sns.barplot(x=df.index, y='Population', data=df)
    # plt.grid()
    plt.xlabel('Gender', fontsize=15)
    plt.ylabel('Voter count', fontsize=15)
    plt.gca().ticklabel_format(axis='y', style='plain')
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=13)
    plt.savefig(Path('Plots/Overview_voter_graph.png'),edgecolor='b',bbox_inches='tight')
    st.image(str(Path('Plots/Overview_voter_graph.png')))
    plt.close()

## Parties with highest seat won
st.markdown('### Top 10 Parties With Highest Seat Won in ' + str(selected_year))

sheet = 'Party_Wise_Seat_Won.csv'
part_wise_performance = pd.read_csv(str(Path('Data',str(selected_year),sheet)))
top_10_parties_with_seat_won = part_wise_performance.groupby('PARTY NAME')['SEAT WON'].sum().sort_values(ascending=False).head(10)

top_10_parties_with_seat_won = top_10_parties_with_seat_won.to_frame()
top_10_parties_with_seat_won.reset_index(inplace=True)
st.dataframe(top_10_parties_with_seat_won, hide_index =True)

## Parties with highest vote gain
st.markdown('### Top 10 Parties With Highest Vote Pulled')

# sheet = 'Party_Wise_Seat_Won.csv'
# part_wise_performance = pd.read_csv(str(Path('Data',str(selected_year),sheet)))
top_10_parties_with_vote = part_wise_performance.groupby('PARTY NAME')['TOTAL VALID VOTES POLLED BY PARTY'].sum().sort_values(ascending=False).head(10)

top_10_parties_with_vote = top_10_parties_with_vote.to_frame()
top_10_parties_with_vote.reset_index(inplace=True)
st.dataframe(top_10_parties_with_vote, hide_index =True)

st.markdown('### State Wise Voter Turnout %', help='Ratio of Voters to Electors')

sheet = 'State_Wise_Voters_Turnout.csv'
state_wise_voter_turnout = pd.read_csv(str(Path('Data',str(selected_year),sheet)))

col14, col15 = st.columns(2)
with col14:
    st.markdown('#### :green[States With High Voter Turnout Ratio]')
    st.dataframe(state_wise_voter_turnout.sort_values(by='VOTERS TURNOUT %', ascending=False)[['NAME OF STATE/UT','VOTERS TURNOUT %']].head(10), hide_index=True)

with col15:
    st.markdown('#### :red[States With Low Voter Turnout Ratio]')
    st.dataframe(state_wise_voter_turnout.sort_values(by='VOTERS TURNOUT %', ascending=True)[['NAME OF STATE/UT','VOTERS TURNOUT %']].head(10), hide_index=True)



st.markdown('### Constituency Wise Voter Turnout', help='Ratio of Voters to Electors')

sheet = 'PC_Wise_Voters_Turnout.csv'
PC_wise_voter_turnout = pd.read_csv(str(Path('Data',str(selected_year),sheet)))

col16, col17 = st.columns(2)
with col16:
    st.markdown('#### :green[PC With High Voter Turnout Ratio]')
    st.dataframe(PC_wise_voter_turnout.sort_values(by='VOTER TURN OUT %', ascending=False)[['STATE NAME','PC NAME','VOTER TURN OUT %']].head(10), hide_index=True)

with col17:
    st.markdown('#### :red[PC With Low Voter Turnout Ratio]')
    st.dataframe(PC_wise_voter_turnout.sort_values(by='VOTER TURN OUT %', ascending=True)[['STATE NAME','PC NAME','VOTER TURN OUT %']].head(10), hide_index=True)


st.markdown('### State Wise NOTA Votes')

sheet = 'Voters_Information.csv'
state_wise_NOTA = pd.read_csv(str(Path('Data',str(selected_year),sheet)), usecols=['STATE NAME','VOTER_TOTAL','NOTA VOTES'])

state_wise_NOTA['NOTA_RATIO %'] = state_wise_NOTA['NOTA VOTES'] / state_wise_NOTA['VOTER_TOTAL'] * 100

col18, col19 = st.columns(2)
with col18:
    st.markdown('#### :green[State With Low NOTA Votes Ratio]')
    st.dataframe(state_wise_NOTA.sort_values(by='NOTA_RATIO %', ascending=True)[['STATE NAME','NOTA_RATIO %']].head(10), hide_index=True)

with col19:
    st.markdown('#### :red[State With High NOTA Votes Ratio]')
    st.dataframe(state_wise_NOTA.sort_values(by='NOTA_RATIO %', ascending=False)[['STATE NAME','NOTA_RATIO %']].head(10), hide_index=True)


st.markdown('### PC Wise NOTA Votes')

sheet = 'PC_Wise_Result.csv'
PC_wise_NOTA = pd.read_csv(str(Path('Data',str(selected_year),sheet)), usecols=['STATE NAME','PC NAME','PARTY NAME','OVER TOTAL VOTES POLLED IN CONSTITUENCY'])

PC_wise_NOTA = PC_wise_NOTA[PC_wise_NOTA['PARTY NAME'] == 'NOTA']
PC_wise_NOTA.rename(columns = {'OVER TOTAL VOTES POLLED IN CONSTITUENCY':'NOTA_RATIO %'}, inplace = True)

col20, col21 = st.columns(2)
with col20:
    st.markdown('#### :green[Constituecies With Low NOTA Votes Ratio]')
    st.dataframe(PC_wise_NOTA.sort_values(by='NOTA_RATIO %', ascending=True)[['STATE NAME','PC NAME','NOTA_RATIO %']].head(10), hide_index=True)

with col21:
    st.markdown('#### :red[Constituecies With High NOTA Votes Ratio]')
    st.dataframe(PC_wise_NOTA.sort_values(by='NOTA_RATIO %', ascending=False)[['STATE NAME','PC NAME','NOTA_RATIO %']].head(10), hide_index=True)