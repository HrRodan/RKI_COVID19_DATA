#%%
import pandas as pd
from datetime import datetime
from datetime import date
from datetime import timedelta
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from repo_tools_pkg.file_tools import find_latest_file
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import matplotlib as mpl


# %% Set parameters
today = datetime.now().date()
yesterday = today - timedelta(days=1)
today_str = today.strftime('%Y-%m-%d')
file_path=os.path.dirname(__file__)
parent_directory=os.path.normpath(os.path.join(file_path, '..',''))
states_number = {
    "Deutschland": 0,
    "Schleswig-Holstein": 1,
    "Hamburg": 2,
    "Niedersachsen": 3,
    "Bremen": 4,
    "Nordrhein-Westfalen": 5,
    "Hessen": 6,
    "Rheinland-Pfalz": 7,
    "Baden-Württemberg": 8,
    "Bayern": 9,
    "Saarland": 10,
    "Berlin": 11,
    "Brandenburg": 12,
    "Mecklenburg-Vorpommern": 13,
    "Sachsen": 14,
    "Sachsen-Anhalt": 15,
    "Thüringen": 16
}

number_states = {value:key for key, value in states_number.items()}
states_number_ir={}
string_mapping={"ü":"ue","Ü":"UE","ä":"ae","Ä":"AE","ö":"oe","Ö":"OE","ß":"ss","-":"_"}
for key, value in number_states.items():
    state=value
    for key2, value2 in string_mapping.items():
        state=state.replace(key2, value2)
    states_number_ir[key]=state.upper()

number_population = {
    8:11100394,
    9:13124737,
    11:3669491,
    12:2521893,
    4:681202,
    2:1847253,
    6:6288080,
    13:1608138,
    3:7993608,
    5:17947221,
    7:4093903,
    10:986887,
    14:4071971,
    15:2194782,
    1:2903773,
    16:2133378,
    0:83166711
}

#%% Read Covid
covid_path_latest=find_latest_file(os.path.join(parent_directory))
covid_df=pd.read_csv(covid_path_latest[0])
covid_df["Meldedatum"]=pd.to_datetime(covid_df["Meldedatum"]).dt.date

#%% Read Testzahl
testzahl_path=find_latest_file(os.path.join(parent_directory,"Testzahlen","raw_data"))[0]
testzahl_df=pd.read_excel(testzahl_path,sheet_name='1_Testzahlerfassung', skipfooter=1)
testzahl_df=testzahl_df.drop(0)
datum=[]
for key, value in testzahl_df.iterrows():
    kalender=value['Kalenderwoche'].split('/')
    datum.append(date.fromisocalendar(int(kalender[1]), int(kalender[0]),7))
testzahl_df.index=pd.to_datetime(datum)
testzahl_df=testzahl_df.resample("1D").backfill()
testzahl_df.sort_index(ascending=True)
testzahl_df["Testungen_7d_mean"]=testzahl_df["Anzahl Testungen"]/7

#%% Read Intensivregister
ir_path=find_latest_file(os.path.join(parent_directory,"Intensivregister","raw_data"),'bundesland')[0]
ir_df=pd.read_csv(ir_path)
ir_df["Datum"]=pd.to_datetime(ir_df["Datum"], utc=True).dt.date

#%% Read Impfquotenmonitoring
iqm_path=os.path.join(parent_directory,"Impfquotenmonitoring",'RKI_COVID19_Impfquotenmonitoring.csv')
iqm_df=pd.read_csv(iqm_path)
iqm_df["ISODate"]=pd.to_datetime(iqm_df["ISODate"]).dt.date


#%% Eval covid_df per Bundesland

def covid_df_sum_bl_lk(id,landkreis=False):
    if id==0:
        bundesland_id=number_states.keys()
    else:
        bundesland_id=[id]
    covid_df_sum=covid_df[((covid_df["NeuerFall"].isin([0,1])) | (covid_df["NeuerTodesfall"].isin([0,1])))&covid_df["IdBundesland"].isin(bundesland_id)].groupby("Meldedatum").agg({"AnzahlFall":"sum","AnzahlTodesfall":"sum"}).sort_values("Meldedatum",ascending=True)
    covid_df_sum.index=pd.to_datetime(covid_df_sum.index)
    #Ein Datensatz pro Tag mit 0 aufüllen
    covid_df_sum=covid_df_sum.resample("1D").asfreq().fillna(0)
    covid_df_sum["AnzahlFall_7d_mean"]=covid_df_sum["AnzahlFall"].rolling(7).mean()
    covid_df_sum["Inzidenz_7d"] = covid_df_sum["AnzahlFall"].rolling(7).sum()/(number_population[id]/100000)
    covid_df_sum["AnzahlTodesfall_7d_mean"]=covid_df_sum["AnzahlTodesfall"].rolling(7).mean()
    covid_df_sum.index=pd.to_datetime(covid_df_sum.index)
    covid_df_sum=covid_df_sum.sort_index(ascending=True)
    covid_df_sum["Cum_sum"]=covid_df_sum["AnzahlFall"].cumsum()
    return covid_df_sum

#%% Read Intensivregister per BL

def ir_df_sum_bl(id):
    ir_df_bl=ir_df.copy()
    ir_df_bl=ir_df_bl[ir_df_bl["Bundesland"]==states_number_ir[id]].groupby("Datum").last()
    ir_df_bl.index=pd.to_datetime(ir_df_bl.index)
    ir_df_bl=ir_df_bl.resample("1D").backfill()
    return ir_df_bl

#%% Eval Impfquotenmonitoring per Bundesland
def iqm_df_sum_bl(id):
    iqm_df_bl=iqm_df.copy()
    iqm_df_bl=iqm_df_bl[iqm_df_bl["IdBundesland"]==id]
    return iqm_df_bl

#%% Plot Bundesland

def plot_covid_bl(id):
    number_plots=4
    if id==0:
        number_plots=5
    covid_df_sum=covid_df_sum_bl_lk(id)
    ir_df=ir_df_sum_bl(id)
    iqm_df=iqm_df_sum_bl(id)
    mpl.rcParams['lines.linewidth'] = 3
    mpl.rcParams['axes.linewidth'] = 1.2
    max_y_covid=int(covid_df_sum["Inzidenz_7d"].max())*1.2
    covid_major_yticks=np.arange(0,max_y_covid,50)
    covid_minor_yticks = np.arange(25, max_y_covid, 25)
    fig, ax = plt.subplots(number_plots, figsize=(10, 20))
    fig.suptitle(f"Covid Situation in {number_states[id]} - Stichtag: {today_str}", fontsize = 20, weight='bold')
    ax[0].plot(covid_df_sum.index, covid_df_sum["Inzidenz_7d"], color='blue')
    ax[0].set_title(f"{number_states[id]} - 7-Tage Inzidenz")
    ax[0].set_yticks(covid_major_yticks)
    ax[0].set_yticks(covid_minor_yticks , minor=True)
    ax[0].yaxis.grid()
    ax[0].yaxis.grid(which='minor', linestyle=':')
    ax[1].plot(covid_df_sum.index, covid_df_sum["AnzahlTodesfall_7d_mean"], color='red')
    ax[1].set_title(f"{number_states[id]} - Covid Todesfälle pro Tag im 7 Tage Mittel")
    ax[2].plot(ir_df.index, ir_df["Aktuelle_COVID_Faelle_Erwachsene_ITS"], color='orange', label="Covid Patienten ITS")
    ax[2].plot(ir_df.index, ir_df["Freie_IV_Kapazitaeten_Davon_COVID"], color='blue', label="Freie IV Kapazität für Covid")
    ax[2].plot(ir_df.index, ir_df["Freie_IV_Kapazitaeten_Gesamt"], color='lightblue', label="Freie IV Kapazität Gesamt")
    ax[2].set_title(f"{number_states[id]} - Anzahl belegter Intensivbetten mit Covd-Patienten")
    ax[2].legend(prop={'size': 16})
    ax[3].plot(iqm_df["ISODate"],iqm_df["Impfungenkumulativ"]/number_population[id]*100, label="Erstimpfungen kumuliert", color='darkviolet')
    ax[3].plot(iqm_df["ISODate"], iqm_df["ZweiteImpfungkumulativ"] / number_population[id]*100, label="Zweitimpfung kumuliert")
    ax[3].set_title(f"{number_states[id]} - Impfquote")
    ax[3].legend(prop={'size': 16})
    ax[3].set_ylim(-2,70)
    ax[3].yaxis.set_minor_locator(AutoMinorLocator(2))
    ax[3].yaxis.grid(which='minor', linestyle=':')
    ax[3].yaxis.grid()
    if id==0:
        ax[4].set_title(f"{number_states[id]} - Testzahlen", fontsize=16)
        ax[4].plot(testzahl_df.index, testzahl_df["Testungen_7d_mean"], color='green')
        ax[4].set_title(f"{number_states[id]} - Testungen pro Tag im 7 Tage Mittel")
    for axs in ax.flat:
        axs.set_title(label=axs.get_title(), weight='bold')
        axs.set_ylabel('Anzahl', fontsize=16)
        axs.set_xlim([date(2020, 2, 20), covid_df_sum.index.max() + timedelta(days=5)])
        axs.yaxis.tick_right()
        for item in ([axs.title,axs.xaxis.label, axs.yaxis.label] + axs.get_xticklabels() + axs.get_yticklabels()):
            item.set_fontsize(16)
    ax[3].set_ylabel('Bevölkerungsanteil [%]',fontsize=16)
    fig.tight_layout(rect=[0, 0, 1, 0.97], h_pad=2)
    plt.savefig(f"covid_bl_{id}.png", bbox_inches='tight')
    plt.show()

#%% Plot All
for key in number_states:
    plot_covid_bl(key)

