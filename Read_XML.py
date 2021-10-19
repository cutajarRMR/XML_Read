import pandas as pd
import numpy as np
from xml.etree import ElementTree as et

FileDir = r'V:\SurveyStore\Customised\Projects\AUS SS Online\2021\08 - Aug\PP Online\Module 4 - Telstra\ES Variables\Cadet_FullData\\'
root = et.parse(FileDir + 'ES_Telco_Aug21.xml').getroot()
asc = pd.read_csv(FileDir + 'ES_Telco_Aug21.asc', header=None, names=['data'])

new_df = pd.DataFrame() # Set empty DataFrame
for var in root[0][0].findall('variable'): # Loop All variables
    nam = var.find('name').text # Get variable Name
    vartype = var.get('type') # Get variable Type
    start = var.find('position').get('start') # Get Start position of
    if vartype == 'multiple': # Need to loop through each group if var is multi
        loopcount = 0 # Set temp count var
        for multivar in var[3].findall('value'): # Loop through each group in multi
            try: # First try precode
                bit = multivar.get('{http://www.confirmit.com/sssextension}precode')
            except: # Else use code
                bit = multivar.get('code')
            #multiname = nam + '-' + bit # Set var name
            multistart = int(start) + loopcount # Set start position
            new_df[nam + '-' + bit] = asc['data'].str.slice(int(multistart)-1,int(multistart)) # Append var to Main df
            loopcount+= 1 # Increment temp var
    else:
        finish = var.find('position').get('finish') #  Get End position
        new_df[nam] = asc['data'].str.slice(int(start)-1,int(finish))  # Append var to Main df

new_df
