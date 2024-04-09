# In this file we will add the genders of the winning andidates.
# We will copy the data of "4. List Of Successful Candidates.xls" to our data excel file.
# This script will add the gender column in required sheet.

import pandas as pd
from pathlib import Path
import easygui


file = Path(easygui.fileopenbox())

sheet = 'Successful_candidate'
succ_candidate = pd.read_excel(file, sheet_name=sheet, skiprows=2)

sheet = 'PC_wise_result'
contested_candidate = pd.read_excel(file, sheet_name=sheet, skiprows=2, usecols=['CANDIDATES NAME','SEX'])

succ_candidate['SEX'] = succ_candidate['WINNER NAME'].apply(lambda x : contested_candidate[contested_candidate['CANDIDATES NAME'] == x]['SEX'].values[0])


with pd.ExcelWriter(file, engine='openpyxl', mode='a',if_sheet_exists='replace') as writer:
    # Write the new DataFrame to a new sheet
    succ_candidate.to_excel(writer, sheet_name='Successful_candidate', index=False)

print('Execution Complete.....')