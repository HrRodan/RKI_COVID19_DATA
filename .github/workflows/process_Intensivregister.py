import os
import re
import pandas as pd
import numpy as np
from datetime import date, datetime, time, timedelta

#%%
path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','..', 'Intensivregister', 'raw_data')
path_csv=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','..', 'Intensivregister', 'DIVI_Intensivregister_Auszug_pro_Landkreis.csv')
iso_date_re = '([0-9]{4})(-?)(1[0-2]|0[1-9])\\2(3[01]|0[1-9]|[12][0-9])'
file_list=os.listdir(path)
pattern='DIVI_Intensivregister'
dfs=[]

#%%
for file in file_list:
    file_path_full=os.path.join(path,file)
    if not os.path.isdir(file_path_full):
        filename=os.path.basename(file)
        re_filename=re.search(pattern,filename)
        re_search=re.search(iso_date_re, filename)
        if re_search and re_filename:
            report_date=date(int(re_search.group(1)), int(re_search.group(3)), int(re_search.group(4)))
            df=pd.read_csv(file_path_full)
            df['report_date']=report_date
            df.rename(columns={'kreis':'IdLandkreis','gemeindeschluessel':'IdLandkreis','bundesland':'IdBundesland','faelle_covid_aktuell_beatmet':'faelle_covid_aktuell_invasiv_beatmet'},inplace=True)
            dfs.append(df)
#%%
time_report=timedelta(hours=9,minutes=15)
divi_df=pd.concat(dfs)
divi_df.drop(['faelle_covid_aktuell_im_bundesland','Unnamed: 0'],axis='columns',inplace=True)
float_columns=divi_df.select_dtypes('float').columns
for c in float_columns:
    divi_df[c] = divi_df[c].astype('Int64')
divi_df['daten_stand']=pd.to_datetime(divi_df['daten_stand'])
divi_df['report_date']=pd.to_datetime(divi_df['report_date']).dt.date
divi_df['daten_stand'].fillna(pd.to_datetime(divi_df['report_date']) + time_report, inplace=True)
divi_df.sort_values(['report_date','IdLandkreis'], inplace=True)

#%% write file
# use newline='' to avoid \r\n line break on windows
with open(path_csv, 'w', newline='', encoding='utf-8') as csvfile:
    divi_df.to_csv(csvfile,index=False,header=True, line_terminator='\n', encoding='utf-8')
