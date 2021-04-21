import os
import re
from datetime import date

import numpy as np
import pandas as pd

# %%
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
path_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Fallzahlen',
                        'RKI_COVID19_Fallzahlen.csv')

iso_date_re = '([0-9]{4})(-?)(1[0-2]|0[1-9])\\2(3[01]|0[1-9]|[12][0-9])'
file_list = os.listdir(path)
file_list.sort(reverse=False)
pattern = 'RKI_COVID19'
dfs = []
dtypes_new = {'Datenstand': 'object', 'IdBundesland': 'Int32', 'IdLandkreis': 'Int32', 'NeuerFall': 'Int8',
              'NeuerTodesfall': 'Int8', 'AnzahlFall': 'Int32', 'AnzahlTodesfall': 'Int32'}
dtypes_old = {'Datenstand': 'object', 'IdBundesland': 'Int32', 'Landkreis ID': 'Int32', 'Neuer Fall': 'Int8',
              'Neuer Todesfall': 'Int8', 'AnzahlFall': 'Int32', 'AnzahlTodesfall': 'Int32'}
# %%
count = 0
for file in file_list:
    file_path_full = os.path.join(path, file)
    if not os.path.isdir(file_path_full):
        filename = os.path.basename(file)
        re_filename = re.search(pattern, filename)
        re_search = re.search(iso_date_re, filename)
        if re_search and re_filename:
            count += 1
            report_date = date(int(re_search.group(1)), int(re_search.group(3)), int(re_search.group(4)))
            # if report_date>date(2020,3,23):
            if report_date >= date(2020, 4, 1):
                print(report_date)
                try:
                    df = pd.read_csv(file_path_full, usecols=dtypes_new.keys(), dtype=dtypes_new)
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path_full, usecols=dtypes_new.keys(), dtype=dtypes_new,  encoding='cp1252')
                except ValueError:
                    df = pd.read_csv(file_path_full, usecols=dtypes_old.keys(), dtype=dtypes_old)

                df.rename(columns={'Neuer Fall': 'NeuerFall', 'Neuer Todesfall': 'NeuerTodesfall',
                             'Landkreis ID': 'IdLandkreis'}, inplace=True)
                df['AnzahlFall_neu'] = np.where(df['NeuerFall'].isin([-1, 1]), df['AnzahlFall'], 0)
                df['AnzahlFall'] = np.where(df['NeuerFall'].isin([0, 1]), df['AnzahlFall'], 0)
                df['AnzahlTodesfall_neu'] = np.where(df['NeuerTodesfall'].isin([-1, 1]), df['AnzahlTodesfall'], 0)
                df['AnzahlTodesfall'] = np.where(df['NeuerTodesfall'].isin([0, 1]), df['AnzahlTodesfall'], 0)
                df.drop(['NeuerFall', 'NeuerTodesfall'], inplace=True, axis=1)
                try:
                    df['Datenstand'] = pd.to_datetime(df['Datenstand'])
                except:
                    df['Datenstand'] = pd.to_datetime(df['Datenstand'], format='%d.%m.%Y, %H:%M Uhr')
                df = df.groupby(['IdBundesland', 'IdLandkreis', 'Datenstand']).sum()
                df['report_date'] = report_date
                dfs.append(df)
                #if count>0: break

# %%
covid_df = pd.concat(dfs)

# %% dedup and write csv
covid_df = covid_df[~covid_df.index.duplicated(keep='first')]
with open(path_csv, 'wb') as csvfile:
    covid_df.to_csv(csvfile, index=True, header=True, line_terminator='\n', encoding='utf-8')
