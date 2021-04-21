import os
import re
from datetime import date

import numpy as np
import pandas as pd
from repo_tools_pkg.file_tools import find_latest_file

# %%
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
path_fallzahlen = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Fallzahlen',
                        'RKI_COVID19_Fallzahlen.csv')

iso_date_re = '([0-9]{4})(-?)(1[0-2]|0[1-9])\\2(3[01]|0[1-9]|[12][0-9])'
pattern = 'RKI_COVID19'
dtypes_fallzahlen= {'Datenstand': 'object', 'IdBundesland': 'Int32', 'IdLandkreis': 'Int32',
              'AnzahlFall': 'Int32', 'AnzahlTodesfall': 'Int32','AnzahlFall_neu': 'Int32',
              'AnzahlTodesfall_neu': 'Int32', 'report_date':'object'}
dtypes_covid = {'Datenstand': 'object', 'IdBundesland': 'Int32', 'IdLandkreis': 'Int32', 'NeuerFall': 'Int8',
              'NeuerTodesfall': 'Int8', 'AnzahlFall': 'Int32', 'AnzahlTodesfall': 'Int32'}
key_list=['Datenstand','IdBundesland','IdLandkreis']

# %% read covid latest
covid_path_latest, date_latest = find_latest_file(os.path.join(path), file_pattern=pattern)
covid_df = pd.read_csv(covid_path_latest, usecols=dtypes_covid.keys(), dtype=dtypes_covid)

# %% read fallzahlen current
fallzahlen_df=pd.read_csv(path_fallzahlen, engine='python', dtype=dtypes_fallzahlen, usecols=dtypes_fallzahlen.keys())
fallzahlen_df['Datenstand']=pd.to_datetime(fallzahlen_df['Datenstand']).dt.date
fallzahlen_df['report_date']=pd.to_datetime(fallzahlen_df['report_date']).dt.date

# %% eval fallzahlen new
print(date_latest)
covid_df['AnzahlFall_neu'] = np.where(covid_df['NeuerFall'].isin([-1, 1]), covid_df['AnzahlFall'], 0)
covid_df['AnzahlFall'] = np.where(covid_df['NeuerFall'].isin([0, 1]), covid_df['AnzahlFall'], 0)
covid_df['AnzahlTodesfall_neu'] = np.where(covid_df['NeuerTodesfall'].isin([-1, 1]), covid_df['AnzahlTodesfall'], 0)
covid_df['AnzahlTodesfall'] = np.where(covid_df['NeuerTodesfall'].isin([0, 1]), covid_df['AnzahlTodesfall'], 0)
covid_df.drop(['NeuerFall', 'NeuerTodesfall'], inplace=True, axis=1)
covid_df['Datenstand'] = pd.to_datetime(covid_df['Datenstand'], format='%d.%m.%Y, %H:%M Uhr').dt.date
covid_df = covid_df.groupby(key_list, as_index=False).sum()
covid_df['report_date'] = date_latest

# %% concat and dedup
fallzahlen_new = pd.concat([covid_df, fallzahlen_df])
fallzahlen_new.drop_duplicates(subset=key_list, keep='last', inplace=True)
fallzahlen_new.sort_values(by=key_list, inplace=True)

# %% write csv
with open(path_fallzahlen, 'wb') as csvfile:
    fallzahlen_new.to_csv(csvfile, index=False, header=True, line_terminator='\n', encoding='utf-8', date_format='%Y-%m-%d')


# %% clean file
# fallzahlen_df_dedup=fallzahlen_df.drop_duplicates(subset=key_list,keep='first')
# with open(path_fallzahlen, 'wb') as csvfile:
#      fallzahlen_df_dedup.to_csv(csvfile, index=True, header=True, line_terminator='\n', encoding='utf-8', date_format='%Y-%m-%d')
