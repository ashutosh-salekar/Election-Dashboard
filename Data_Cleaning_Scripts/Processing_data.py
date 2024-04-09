import pandas as pd
import numpy as np
from pathlib import Path
import easygui
import os

folder = easygui.diropenbox()
folder

CSV_folder = Path(folder,'CSV_files')
CSV_folder.mkdir(exist_ok=True)

def column_name_upper_case(columns):
    return [i.upper() for i in columns]

def column_name_strip(columns):
    return [i.strip() for i in columns]

def List_of_Political_Parties_Participated():
    """
    Action performed in function
    1. Upper case the column name
    2. Strip the column name
    3. Save data in CSV file
    
    Manual preprocessing requird
    1. Delete Heading and the bottom inside the file
    """
    
    IP_file_name = 'List of Political Parties Participated.xlsx'
    OP_file_name = 'Party_List.csv'
    
    file_path = str(Path(folder,IP_file_name))
    file_data = pd.read_excel(file_path)
    
    col = file_data.columns
    col = column_name_upper_case(col)
    col = column_name_strip(col)
    file_data.columns = col
    
    if os.path.isfile(str(Path(folder,CSV_folder,OP_file_name))):
        os.remove(str(Path(folder,CSV_folder,OP_file_name)))
    
    file_data.to_csv(str(Path(folder,CSV_folder,OP_file_name)), index=False)
    
    print('Successfully processed "', IP_file_name, '" and saved as "', OP_file_name, '"')

def List_Of_Successful_Candidates():
    """
    Action performed in function
    1. Upper case the column name
    2. Strip the column name
    3. Repalce party name abbreviation by full party name
    4. Save data in CSV file 
    
    Manual preprocessing requird
    1. Delete Heading and the bottom inside the file
    2. If party name abbreviation is present update the "party_name_abbreviation_flag"
    """
    
    party_name_abbreviation_flag = 0

    IP_file_name1 = 'List Of Successful Candidates.xlsx'
    IP_file_name2 = 'Party_List.csv'
    OP_file_name = 'Successful_Candidate.csv'
    
    file_path = str(Path(folder,IP_file_name1))
    file_data1 = pd.read_excel(file_path)

    file_path2 = str(Path(folder,CSV_folder,IP_file_name2))
    file_data2 = pd.read_csv(file_path2)
    
    col = file_data1.columns
    col = column_name_upper_case(col)
    col = column_name_strip(col)
    file_data1.columns = col
    
    if party_name_abbreviation_flag == 1:
        # Logic to repalce party name abbreviation by full party name
        file_data1['PARTY'] = file_data1['PARTY'].apply(lambda x: 'Independent' if x == 'IND' else file_data2[file_data2['ABBREVIATION'] == x]['PARTY NAME'].values[0])

    if os.path.isfile(str(Path(folder,CSV_folder,OP_file_name))):
        os.remove(str(Path(folder,CSV_folder,OP_file_name)))
    
    file_data1.to_csv(str(Path(folder,CSV_folder,OP_file_name)), index=False)
    
    print('Successfully processed "', IP_file_name1, '" and saved as "', OP_file_name, '"')


def VOTERS_INFORMATION_Extract_State_Total(data):
    """
    Extract state's total data by neglecting castwise data
    """
    
    # Extract a column with only state name in it
    state_names_data = data[(~data['STATE NAME'].isnull()) & (data['STATE NAME'] != 'State Total') & (data['STATE NAME'] != 'Grand Total')]['STATE NAME']
    state_names_data = state_names_data.reset_index(drop=True)

    # Extract the all data with only rows of state total
    state_total_data = data[data['STATE NAME'] == 'State Total'].drop(columns='STATE NAME')
    state_total_data = state_total_data.reset_index(drop=True)

    # Concat both df (state name, state total data)
    new_df = pd.concat([state_names_data,state_total_data], axis=1)
    
    return new_df


def VOTERS_INFORMATION():
    """
    Action performed in function
    1. Upper case the column name
    2. Strip the column name
    3. Extrat state's total data 
    4. Save data in CSV file
    
    Manual preprocessing requird
    1. Delete Heading, level 1 column headers and the bottom text
    2. Add column heading as 'STATE NAME' to the 1st column
    3. Delete 2nd and 3rd column of cast categories and respective seats
    4. Add prefix as 'elector_' and 'voter_' for the columns with same name.
    """
    
    IP_file_name = 'VOTERS INFORMATION.xlsx'
    OP_file_name = 'Voters_Information.csv'
    
    file_path = str(Path(folder,IP_file_name))
    file_data = pd.read_excel(file_path)
    
    col = file_data.columns
    col = column_name_upper_case(col)
    col = column_name_strip(col)
    file_data.columns = col
    
    file_data = VOTERS_INFORMATION_Extract_State_Total(file_data)
    
    if os.path.isfile(str(Path(folder,CSV_folder,OP_file_name))):
        os.remove(str(Path(folder,CSV_folder,OP_file_name)))
    
    file_data.to_csv(str(Path(folder,CSV_folder,OP_file_name)), index=False)
    
    print('Successfully processed "', IP_file_name, '" and saved as "', OP_file_name, '"')


def State_Wise_Voters_Turn_Out():
    """
    Action performed in function
    1. Upper case the column name
    2. Strip the column name
    3. Save data in CSV file
    
    Manual preprocessing requird
    1. Delete Heading, level 1 column headers, last row and description at the bottom
    2. Handle the typo in the column name, "VOTERS TOUROUT %" -> "VOTERS TOURNOUT %"
    """
    
    IP_file_name = 'State Wise Voters Turn Out.xlsx'
    OP_file_name = 'State_Wise_Voters_Turnout.csv'
    
    file_path = str(Path(folder,IP_file_name))
    file_data = pd.read_excel(file_path)
    
    col = file_data.columns
    col = column_name_upper_case(col)
    col = column_name_strip(col)
    file_data.columns = col
    
    if os.path.isfile(str(Path(folder,CSV_folder,OP_file_name))):
        os.remove(str(Path(folder,CSV_folder,OP_file_name)))
    
    file_data.to_csv(str(Path(folder,CSV_folder,OP_file_name)), index=False)
    
    print('Successfully processed "', IP_file_name, '" and saved as "', OP_file_name, '"')


def PC_Wise_Voters_Turn_Out():
    """
    Action performed in function
    1. Upper case the column name
    2. Strip the column name
    3. Save data in CSV file
    
    Manual preprocessing requird
    1. Delete Heading, level 1 column headers and description at the bottom
    2. Remove '()' from the column name 'VOTER TURN OUT (%)'
    3. Add column heading 'POSTAL VOTES' in correct row
    4. Add suffix '_turnout' to the same column headers
    """
    
    IP_file_name = 'PC Wise Voters Turn Out.xlsx'
    OP_file_name = 'PC_Wise_Voters_Turnout.csv'
    
    file_path = str(Path(folder,IP_file_name))
    file_data = pd.read_excel(file_path)
    
    col = file_data.columns
    col = column_name_upper_case(col)
    col = column_name_strip(col)
    file_data.columns = col
    
    if os.path.isfile(str(Path(folder,CSV_folder,OP_file_name))):
        os.remove(str(Path(folder,CSV_folder,OP_file_name)))
    
    file_data.to_csv(str(Path(folder,CSV_folder,OP_file_name)), index=False)
    
    print('Successfully processed "', IP_file_name, '" and saved as "', OP_file_name, '"')

def State_Wise_Seat_Won_and_Valid_Votes_Polled_by_Political_Parties():
    """
    Action performed in function
    1. Upper case the column name
    2. Strip the column name
    3. Save data in CSV file
    
    Manual preprocessing requird
    1. Delete Heading and description at the bottom
    """
    
    IP_file_name = 'State Wise Seat Won & Valid Votes Polled by Political Parties.xlsx'
    OP_file_name = 'State_Wise_Seat_Won.csv'
    
    file_path = str(Path(folder,IP_file_name))
    file_data = pd.read_excel(file_path)
    
    col = file_data.columns
    col = column_name_upper_case(col)
    col = column_name_strip(col)
    file_data.columns = col
    
    if os.path.isfile(str(Path(folder,CSV_folder,OP_file_name))):
        os.remove(str(Path(folder,CSV_folder,OP_file_name)))
    
    file_data.to_csv(str(Path(folder,CSV_folder,OP_file_name)), index=False)
    
    print('Successfully processed "', IP_file_name, '" and saved as "', OP_file_name, '"')

def Partywise_Seat_Won_Valid_Votes_Polled_in_Each_State():
    """
    Action performed in function
    1. Upper case the column name
    2. Strip the column name
    3. Save data in CSV file
    
    Manual preprocessing requird
    1. Delete Heading and description at the bottom
    """
    
    IP_file_name = 'Partywise Seat Won Valid Votes Polled in Each State.xlsx'
    OP_file_name = 'Party_Wise_Seat_Won.csv'
    
    file_path = str(Path(folder,IP_file_name))
    file_data = pd.read_excel(file_path)
    
    col = file_data.columns
    col = column_name_upper_case(col)
    col = column_name_strip(col)
    file_data.columns = col
    
    if os.path.isfile(str(Path(folder,CSV_folder,OP_file_name))):
        os.remove(str(Path(folder,CSV_folder,OP_file_name)))
    
    file_data.to_csv(str(Path(folder,CSV_folder,OP_file_name)), index=False)
    
    print('Successfully processed "', IP_file_name, '" and saved as "', OP_file_name, '"')



def Constituency_Wise_Detailed_Result():
    """
    Action performed in function
    1. Upper case the column name
    2. Strip the column name
    3. Save data in CSV file
    
    Manual preprocessing requird
    1. Delete Heading and description at the bottom
    """
    
    IP_file_name = 'Constituency Wise Detailed Result.xlsx'
    OP_file_name = 'PC_Wise_Result.csv'
    
    file_path = str(Path(folder,IP_file_name))
    file_data = pd.read_excel(file_path)
    
    col = file_data.columns
    col = column_name_upper_case(col)
    col = column_name_strip(col)
    file_data.columns = col
    
    if os.path.isfile(str(Path(folder,CSV_folder,OP_file_name))):
        os.remove(str(Path(folder,CSV_folder,OP_file_name)))
    
    file_data.to_csv(str(Path(folder,CSV_folder,OP_file_name)), index=False)
    
    print('Successfully processed "', IP_file_name, '" and saved as "', OP_file_name, '"')


def Add_Gender_Of_Winning_Candidates():
    """
    Action performed in function
    1. Add the gender column for winnning candidates
    
    """
    
    IP_file_name1 = 'Successful_Candidate.csv'
    IP_file_name2 = 'PC_Wise_Result.csv'
    OP_file_name = 'Successful_Candidate.csv'
    
    file_path = str(Path(folder, CSV_folder, IP_file_name1))
    succ_candidate = pd.read_csv(file_path)

    file_path = str(Path(folder, CSV_folder, IP_file_name2))
    contested_candidate = pd.read_csv(file_path, usecols=['CANDIDATES NAME','SEX'])
    
    succ_candidate['SEX'] = succ_candidate['WINNER NAME'].apply(lambda x : get_candidate_gender(x, contested_candidate))
    
    if os.path.isfile(str(Path(folder,CSV_folder,OP_file_name))):
        os.remove(str(Path(folder,CSV_folder,OP_file_name)))
    
    succ_candidate.to_csv(str(Path(folder,CSV_folder,OP_file_name)), index=False)
    
    print('Successfully processed "', IP_file_name1, '" and saved as "', OP_file_name, '"')


def get_candidate_gender(x, contested_candidate):
    try:
        return contested_candidate[contested_candidate['CANDIDATES NAME'].str.lower() == x.lower()]['SEX'].values[0]
    except:
        print(x)
        return None

# List_of_Political_Parties_Participated()
List_Of_Successful_Candidates()
# VOTERS_INFORMATION()
# State_Wise_Voters_Turn_Out()
# PC_Wise_Voters_Turn_Out()
# State_Wise_Seat_Won_and_Valid_Votes_Polled_by_Political_Parties()
# Partywise_Seat_Won_Valid_Votes_Polled_in_Each_State()
Constituency_Wise_Detailed_Result()
Add_Gender_Of_Winning_Candidates()