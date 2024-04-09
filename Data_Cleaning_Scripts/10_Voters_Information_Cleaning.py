# In this file we will clean the "10. VOTERS INFORMATION" excel file.
# We will extract the only rows with state total and skip the cast wise rows.

import pandas as pd
from pathlib import Path
import easygui


file_path = Path(easygui.fileopenbox())

# Read seleted file
data = pd.read_excel(file_path, skiprows=2, skipfooter=4)

# Extract a column with only state name in it
state_names_data = data[(~data['STATE NAME'].isnull()) & (data['STATE NAME'] != 'State Total') & (data['STATE NAME'] != 'Grand Total')]['STATE NAME']
state_names_data = state_names_data.reset_index(drop=True)

# Extract the all data with only rows of state total
state_total_data = data[data['STATE NAME'] == 'State Total'].drop(columns='STATE NAME')
state_total_data = state_total_data.reset_index(drop=True)

# Concat both df (state name, state total data)
new_df = pd.concat([state_names_data,state_total_data], axis=1)

# Saving the updated file
new_df.to_excel(Path(file_path.parent, 'Updated_'+file_path.name), index=False)
