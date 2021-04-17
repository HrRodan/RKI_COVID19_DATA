# %%
import itertools
import os
import re
from datetime import date
from datetime import datetime
from datetime import timedelta

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
from matplotlib.ticker import (AutoMinorLocator)

from repo_tools_pkg.file_tools import find_latest_file

# %% Set Plot parameters
mpl.rcParams['lines.linewidth'] = 3
mpl.rcParams['axes.linewidth'] = 1.2
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.size']=16

# %% Set parameters
today = datetime.now(pytz.timezone('Europe/Berlin')).date()
yesterday = today - timedelta(days=1)
today_str = today.strftime('%Y-%m-%d')
file_path = os.path.dirname(__file__)
parent_directory = os.path.normpath(os.path.join(file_path, '..', '..', ''))
lk_to_plot = [9572, 9564, 9562, 14523]
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

number_states = {value: key for key, value in states_number.items()}
states_number_ir = {}
string_mapping = {"ü": "ue", "Ü": "UE", "ä": "ae", "Ä": "AE", "ö": "oe", "Ö": "OE", "ß": "ss", "-": "_"}
for key, value in number_states.items():
    state = value
    for key2, value2 in string_mapping.items():
        state = state.replace(key2, value2)
    states_number_ir[key] = state.upper()

number_population = {
    8: 11100394,
    9: 13124737,
    11: 3669491,
    12: 2521893,
    4: 681202,
    2: 1847253,
    6: 6288080,
    13: 1608138,
    3: 7993608,
    5: 17947221,
    7: 4093903,
    10: 986887,
    14: 4071971,
    15: 2194782,
    1: 2903773,
    16: 2133378,
    0: 83166711
}

# %% Read Covid
covid_path_latest = find_latest_file(os.path.join(parent_directory))
covid_df = pd.read_csv(covid_path_latest[0])
covid_df["Meldedatum"] = pd.to_datetime(covid_df["Meldedatum"]).dt.date

# %% Read Testzahl
testzahl_path = find_latest_file(os.path.join(parent_directory, "Testzahlen", "raw_data"))[0]
testzahl_df = pd.read_excel(testzahl_path, sheet_name='1_Testzahlerfassung', skipfooter=1)
testzahl_df = testzahl_df.drop(0)
datum = []
for key, value in testzahl_df.iterrows():
    kalender = value['Kalenderwoche'].split('/')
    kalender_clean = []
    for k in kalender:
        kalender_clean.append(int(re.sub('\\D', '', k)))
    datum.append(date.fromisocalendar(kalender_clean[1], kalender_clean[0], 7))
testzahl_df.index = pd.to_datetime(datum)
testzahl_df = testzahl_df.resample("1D").backfill()
testzahl_df.sort_index(ascending=True, inplace=True)
testzahl_df["Testungen_7d_mean"] = testzahl_df["Anzahl Testungen"] / 7
testzahl_df["Positiv_7d_mean"] = testzahl_df['Positiv getestet'] / 7

# %% Read Intensivregister
ir_path = find_latest_file(os.path.join(parent_directory, "Intensivregister", "raw_data"), 'bundesland')[0]
ir_df = pd.read_csv(ir_path)
ir_df["Datum"] = pd.to_datetime(ir_df["Datum"], utc=True).dt.date

# %% Read Intensivregister Landkreise
ir_lk_path = os.path.join(parent_directory, "Intensivregister", "DIVI_Intensivregister_Auszug_pro_Landkreis.csv")
ir_lk_df = pd.read_csv(ir_lk_path, encoding='utf-8', engine='python')
ir_lk_df["report_date"] = pd.to_datetime(ir_lk_df["report_date"]).dt.date
ir_lk_df["daten_stand"] = pd.to_datetime(ir_lk_df["daten_stand"])

# %% Read Impfquotenmonitoring
iqm_path = os.path.join(parent_directory, "Impfquotenmonitoring", 'RKI_COVID19_Impfquotenmonitoring.csv')
iqm_df = pd.read_csv(iqm_path)
iqm_df["ISODate"] = pd.to_datetime(iqm_df["ISODate"])

# %% Read Landkreise
landkreis_path = os.path.join(parent_directory, "Misc", 'Landkreise.csv')
landkreis_df = pd.read_csv(landkreis_path, skiprows=6, skipfooter=4, engine='python', sep=';', encoding='utf_8',
                           names=['IdLandkreis', 'Landkreis', 'Bevoelkerung'], na_values='-')

# %% Read Nowcasting
nc_path = find_latest_file(os.path.join(parent_directory, "Nowcasting", "raw_data"))[0]
nc_df = pd.read_csv(nc_path, engine='python', skipfooter=18, sep=';', na_values='.', decimal=',')
nc_df["Datum"] = pd.to_datetime(nc_df["Datum"], format='%d.%m.%Y').dt.date
nc_df = nc_df[nc_df['Datum'] >= pd.to_datetime('2020-04-01')]
nc_df.sort_values('Datum', inplace=True)


# %% Eval covid_df per Bundesland

def covid_df_sum_bl_lk(id_bl_lk, landkreis=False):
    if id_bl_lk == 0:
        bundesland_id = number_states.keys()
    else:
        bundesland_id = [id_bl_lk]

    if landkreis:
        population = landkreis_df[landkreis_df['IdLandkreis'] == id_bl_lk].iloc[0]['Bevoelkerung']
    else:
        population = number_population[id_bl_lk]

    if landkreis:
        covid_df_sum = covid_df[((covid_df["NeuerFall"].isin([0, 1])) | (covid_df["NeuerTodesfall"].isin([0, 1]))) & (
                covid_df["IdLandkreis"] == id_bl_lk)].groupby("Meldedatum").agg(
            {"AnzahlFall": "sum", "AnzahlTodesfall": "sum"}).sort_values("Meldedatum", ascending=True)
    else:
        covid_df_sum = covid_df[
            ((covid_df["NeuerFall"].isin([0, 1])) | (covid_df["NeuerTodesfall"].isin([0, 1]))) & covid_df[
                "IdBundesland"].isin(bundesland_id)].groupby("Meldedatum").agg(
            {"AnzahlFall": "sum", "AnzahlTodesfall": "sum"}).sort_values("Meldedatum", ascending=True)

    covid_df_sum.index = pd.to_datetime(covid_df_sum.index)
    # Ein Datensatz pro Tag mit 0 aufüllen
    covid_df_sum = covid_df_sum.resample("1D").asfreq().fillna(0)
    covid_df_sum["AnzahlFall_7d_mean"] = covid_df_sum["AnzahlFall"].rolling(7).mean()
    covid_df_sum["Inzidenz_7d"] = covid_df_sum["AnzahlFall"].rolling(7).sum() / (population / 100000)
    covid_df_sum["AnzahlTodesfall_7d_mean"] = covid_df_sum["AnzahlTodesfall"].rolling(7).mean()
    covid_df_sum["CFR_7d_mean"] = covid_df_sum["AnzahlTodesfall_7d_mean"] / covid_df_sum["AnzahlFall_7d_mean"]
    covid_df_sum.loc[covid_df_sum.index < pd.to_datetime('2020-03-01'), ["CFR_7d_mean"]] = np.nan
    covid_df_sum.index = pd.to_datetime(covid_df_sum.index)
    covid_df_sum.sort_index(ascending=True, inplace=True)
    covid_df_sum["Cum_sum"] = covid_df_sum["AnzahlFall"].cumsum()
    covid_df_sum["Cum_sum_Todesfall"] = covid_df_sum["AnzahlTodesfall"].cumsum()
    return covid_df_sum


# %% Neue Fälle in der Publikation
def covid_faelle_neu(id_bl_lk, landkreis=False):
    if id_bl_lk == 0:
        bundesland_id = number_states.keys()
    else:
        bundesland_id = [id_bl_lk]

    if landkreis:
        covid_df_neu = covid_df[((covid_df["NeuerFall"].isin([-1, 1])) | (covid_df["NeuerTodesfall"].isin([-1, 1]))) & (
                covid_df["IdLandkreis"] == id_bl_lk)]
    else:
        covid_df_neu = covid_df[((covid_df["NeuerFall"].isin([-1, 1])) | (covid_df["NeuerTodesfall"].isin([-1, 1]))) & (
            covid_df["IdBundesland"].isin(bundesland_id))]

    faelle_neu = covid_df_neu['AnzahlFall'].sum()
    todesfaelle_neu = covid_df_neu['AnzahlTodesfall'].sum()
    return (faelle_neu, todesfaelle_neu)


# %% Read Intensivregister per BL

def ir_df_sum_bl(id_bl):
    ir_df_bl = ir_df[ir_df["Bundesland"] == states_number_ir[id_bl]].groupby("Datum").last()
    ir_df_bl.index = pd.to_datetime(ir_df_bl.index)
    ir_df_bl = ir_df_bl.resample("1D").backfill()
    return ir_df_bl


# %% Eval Impfquotenmonitoring per Bundesland
def iqm_df_sum_bl(id_bl, mean_days=14):
    iqm_df_bl = iqm_df[iqm_df["IdBundesland"] == id_bl]
    iqm_df_bl.set_index('ISODate', inplace=True)
    iqm_df_bl = iqm_df_bl.resample("1D").ffill()
    iqm_df_bl.sort_index(inplace=True)
    # eval projected
    iqm_df_project = iqm_df_bl.iloc[-mean_days - 1:]
    mean_1st = iqm_df_project['Impfungenkumulativ'].diff().mean()
    kum_1st = iqm_df_project['Impfungenkumulativ'].max()
    days_75 = (number_population[id_bl] * 0.75 - kum_1st) / mean_1st
    mean_2nd = iqm_df_project['ZweiteImpfungkumulativ'].diff().mean()
    kum_2nd = iqm_df_project['ZweiteImpfungkumulativ'].max()
    days_75_2nd = (number_population[id_bl] * 0.75 - kum_2nd) / mean_2nd
    project_vaccine = {
        'mean_1st': mean_1st,
        'mean_1st_quote': mean_1st / number_population[id_bl] * 100,
        'days_75': np.round(days_75, 0),
        'mean_2nd' : mean_2nd,
        'kum_2nd' : kum_2nd,
        'days_75_2nd' : days_75_2nd,
        'mean_2nd_quote': mean_2nd / number_population[id_bl] * 100,
    }
    return (iqm_df_bl, project_vaccine)


# %% Eval Intensivregister per Landkreis
def ir_df_sum_lk(id_lk):
    ir_lk_df_temp = ir_lk_df[ir_lk_df["IdLandkreis"] == id_lk]
    return ir_lk_df_temp


# %% Plot Bundesland

def plot_covid_bl(id_bl):
    number_plots = 4
    fig_size = (10, 20)
    if id_bl == 0:
        number_plots = 7
        fig_size = (10, 32)
    covid_df_sum = covid_df_sum_bl_lk(id_bl).sort_index()
    inzidenz = covid_df_sum["Inzidenz_7d"].iloc[-1]
    ir_df_plot = ir_df_sum_bl(id_bl)
    mean_days_plot = 14
    iqm_df_plot, iqm_project_plot = iqm_df_sum_bl(id_bl, mean_days=mean_days_plot)
    faelle_neu_plot, todesfaelle_neu_plot = covid_faelle_neu(id_bl, False)
    max_y_covid = int(covid_df_sum["Inzidenz_7d"].max()) * 1.2
    covid_major_yticks = np.arange(0, max_y_covid, 50)
    covid_minor_yticks = np.arange(25, max_y_covid, 25)
    # start Plot
    fig, ax = plt.subplots(number_plots, figsize=fig_size)
    fig.suptitle(f"Covid Situation in {number_states[id_bl]} \nStichtag: {today_str}", fontsize=20, weight='bold')
    # Inzidenz
    ax[0].plot(covid_df_sum.index, covid_df_sum["Inzidenz_7d"], color='blue')
    ax[0].set_title(f"{number_states[id_bl]} - 7-Tage Inzidenz")
    ax[0].set_yticks(covid_major_yticks)
    ax[0].set_yticks(covid_minor_yticks, minor=True)
    ax[0].yaxis.grid(which='minor', linestyle=':')
    ax[0].text(0.95, 0.90, f'{inzidenz:.1f}', horizontalalignment='right',
               verticalalignment='bottom', fontsize=16, color='red', weight='bold', transform=ax[0].transAxes)
    ax[0].plot(covid_df_sum.index[-1], inzidenz, marker='x', color='red', markersize=7, markeredgewidth=3)
    ax[0].set_ylabel('Anzahl', fontsize=16)
    # Absolute Zahlen
    ax[1].plot(covid_df_sum.index, covid_df_sum["AnzahlTodesfall_7d_mean"], color='black')
    ax[1].set_title(f"{number_states[id_bl]} - Covid (Todes)-Fälle pro Tag im 7 Tage Mittel")
    ax[1].annotate('', xy=(date(2020, 10, 15), ax[1].get_ylim()[1] / 2),
                   xytext=(date(2020, 7, 1), ax[1].get_ylim()[1] / 2),
                   arrowprops=dict(arrowstyle="<-", color='red', linewidth=2))
    ax[1].annotate('', xy=(date(2021, 1, 20), ax[1].get_ylim()[1] * 0.7),
                   xytext=(date(2021, 3, 15), ax[1].get_ylim()[1] * 0.7),
                   arrowprops=dict(arrowstyle="<-", color='black', linewidth=2))
    ax[1].set_ylabel('Anzahl Todesfälle 7d Mittel', fontsize=16)
    ax1_2 = ax[1].twinx()
    ax1_2.plot(covid_df_sum.index, covid_df_sum["AnzahlFall_7d_mean"], color='red')
    ax1_2.set_ylabel('Anzahl Erkrankte 7d Mittel', fontsize=16, color='red')
    ax1_2.yaxis.tick_left()
    ax1_2.yaxis.set_label_position("left")
    ax1_2.tick_params(axis='y', labelcolor='red')
    for item in (
            [ax1_2.title, ax1_2.xaxis.label, ax1_2.yaxis.label] + ax1_2.get_xticklabels() + ax1_2.get_yticklabels()):
        item.set_fontsize(16)
    props = dict(facecolor='lightgrey', alpha=1, edgecolor='none')
    ax[1].text(0.05, 0.85,
               f'Differenz zum Vortag\n'
               f'(Differenz zum letzten Report)'
               , horizontalalignment='left', transform=ax[1].transAxes,
               verticalalignment='bottom', fontsize=14, color='black', ma='left', weight='bold')
    ax[1].text(0.25, 0.8,
               f'Erkrankungen:\n'
               f'Todesfälle:'
               , horizontalalignment='right', bbox=props, transform=ax[1].transAxes,
               verticalalignment='top', fontsize=14, color='black', ma='left')
    ax[1].text(0.25, 0.8,
               f'{covid_df_sum["AnzahlFall"].iloc[-1]:.0f} ({faelle_neu_plot:.0f})\n'
               f'{covid_df_sum["AnzahlTodesfall"].iloc[-1]:.0f} ({todesfaelle_neu_plot:.0f})'
               , horizontalalignment='left', bbox=props, transform=ax[1].transAxes,
               verticalalignment='top', fontsize=14, color='black', ma='left')
    # Intensivregister
    ax[2].plot(ir_df_plot.index, ir_df_plot["Aktuelle_COVID_Faelle_Erwachsene_ITS"], color='orange',
               label="Covid Patienten ITS")
    ax[2].plot(ir_df_plot.index, ir_df_plot["Freie_IV_Kapazitaeten_Davon_COVID"], color='blue',
               label="Freie IV Kapazität für Covid")
    ax[2].plot(ir_df_plot.index, ir_df_plot["Freie_IV_Kapazitaeten_Gesamt"], color='lightblue',
               label="Freie IV Kapazität Gesamt")
    ax[2].set_title(f"{number_states[id_bl]} - Intensivbetten")
    ax[2].legend(prop={'size': 16})
    ax[2].set_ylabel('Anzahl', fontsize=16)
    # Impfungen
    ax[3].plot(iqm_df_plot.index, iqm_df_plot["Impfungenkumulativ"] / number_population[id_bl] * 100,
               label="Erstimpfungen kumuliert", color='darkviolet')
    ax[3].plot(iqm_df_plot.index, iqm_df_plot["ZweiteImpfungkumulativ"] / number_population[id_bl] * 100,
               label="Zweitimpfung kumuliert")
    ax[3].set_title(f"{number_states[id_bl]} - Impfquote")
    ax[3].legend(prop={'size': 16})
    ax[3].set_ylim(-2, 70)
    ax[3].yaxis.set_minor_locator(AutoMinorLocator(2))
    ax[3].yaxis.grid(which='minor', linestyle=':')
    ax[3].yaxis.grid()
    ax[3].text(0.07, 0.8,
               f'{mean_days_plot}-Tage Tendenz\n'
               f'Erstimpfung'
               , horizontalalignment='left', transform=ax[3].transAxes,
               verticalalignment='bottom', fontsize=15, color='black', ma='left', weight='bold')
    ax[3].text(0.2, 0.75,
               f'Impfungen: \n'
               f'Impfquote: \n'
               f'75% in:'
               , horizontalalignment='right', bbox=props, transform=ax[3].transAxes,
               verticalalignment='top', fontsize=14, color='black', ma='left')
    ax[3].text(0.2, 0.75,
               f'{iqm_project_plot["mean_1st"]:.0f} pro Tag\n'
               f'{iqm_project_plot["mean_1st_quote"]:.2f}% pro Tag\n'
               f'{iqm_project_plot["days_75"]:.0f} Tagen ({(today + timedelta(days=iqm_project_plot["days_75"])).strftime("%Y-%m")})'
               , horizontalalignment='left', bbox=props, transform=ax[3].transAxes,
               verticalalignment='top', fontsize=14, color='black', ma='left')
    ax[3].text(0.07, 0.35,
               f'Zweitimpfung'
               , horizontalalignment='left', transform=ax[3].transAxes,
               verticalalignment='bottom', fontsize=15, color='black', ma='left', weight='bold')
    ax[3].text(0.2, 0.3,
               f'Impfungen: \n'
               f'Impfquote: \n'
               f'75% in:'
               , horizontalalignment='right', bbox=props, transform=ax[3].transAxes,
               verticalalignment='top', fontsize=14, color='black', ma='left')
    ax[3].text(0.2, 0.3,
               f'{iqm_project_plot["mean_2nd"]:.0f} pro Tag\n'
               f'{iqm_project_plot["mean_2nd_quote"]:.2f}% pro Tag\n'
               f'{iqm_project_plot["days_75_2nd"]:.0f} Tagen ({(today + timedelta(days=iqm_project_plot["days_75"])).strftime("%Y-%m")})'
               , horizontalalignment='left', bbox=props, transform=ax[3].transAxes,
               verticalalignment='top', fontsize=14, color='black', ma='left')
    ax[3].set_ylabel('Bevölkerungsanteil [%]', fontsize=16)
    if id_bl == 0:
        # Testzahl
        ax[4].plot(testzahl_df.index, testzahl_df["Testungen_7d_mean"], color='green', label='Gesamt')
        ax[4].plot(testzahl_df.index, testzahl_df["Positiv_7d_mean"], color='blue', label='Positiv')
        ax[4].set_title(f"{number_states[id_bl]} - Testungen pro Tag im 7 Tage Mittel")
        ax[4].ticklabel_format(axis='y', style='sci', scilimits=(-3, 3))
        ax[4].legend(prop={'size': 16})
        ax[4].set_ylabel('Anzahl', fontsize=16)
        # CFR
        ax[5].plot(covid_df_sum.index, covid_df_sum["CFR_7d_mean"] * 100, color='black')
        ax[5].set_title(f"{number_states[id_bl]} - CFR (case fatality rate) im 7 Tage Mittel")
        ax[5].set_ylabel('CFR [%]', fontsize=16)
        # R-Wert
        ax[6].plot(nc_df['Datum'], nc_df['Schätzer_7_Tage_R_Wert'], color='black')
        ax[6].set_title(f"{number_states[id_bl]} - Schätzer 7-Tage R-Wert")
        ax[6].set_ylabel('7-Tage R-Wert', fontsize=16)
        ax[6].axhline(1, color='red', ls='--')
        ax[6].fill_between(nc_df['Datum'], nc_df['OG_PI_7_Tage_R_Wert'], nc_df['UG_PI_7_Tage_R_Wert'],
                           color='lightgrey', alpha=0.8)
        ax[6].text(0.95, 0.95, f'{nc_df["Schätzer_7_Tage_R_Wert"].iloc[-2]:.2f} '
                               f'({nc_df["UG_PI_7_Tage_R_Wert"].iloc[-2]:.2f} .. '
                               f'{nc_df["OG_PI_7_Tage_R_Wert"].iloc[-2]:.2f})',
                   horizontalalignment='right',
                   verticalalignment='top', fontsize=16, color='red', weight='bold', transform=ax[6].transAxes)
        ax[6].plot(nc_df['Datum'].iloc[-2], nc_df["Schätzer_7_Tage_R_Wert"].iloc[-2], marker='x', color='red',
                   markersize=7, markeredgewidth=3)
    for axs in ax.flat:
        axs.set_title(label=axs.get_title(), weight='bold')
        axs.set_xlim([date(2020, 2, 20), covid_df_sum.index.max() + timedelta(days=7)])
        axs.yaxis.tick_right()
        axs.yaxis.set_label_position("right")
        axs.xaxis.grid()
        axs.yaxis.grid()
        axs.axvline(today, ls='-', color='gold', linewidth=1)
        for item in ([axs.title, axs.xaxis.label, axs.yaxis.label] + axs.get_xticklabels() + axs.get_yticklabels()):
            item.set_fontsize(16)
    fig.align_ylabels()
    fig.tight_layout(rect=[0, 0, 1, 0.97], h_pad=2)
    plt.savefig(os.path.join(parent_directory, 'Auswertung', f"covid_bl_{id_bl}.png"), bbox_inches='tight', dpi=60)
    plt.show()
    plt.close(fig)


# %% Plot Landkreis
def plot_covid_lk(id_lk):
    name_lk = landkreis_df[landkreis_df['IdLandkreis'] == id_lk].iloc[0]['Landkreis']
    covid_df_sum = covid_df_sum_bl_lk(id_lk, landkreis=True).sort_index()
    inzidenz = covid_df_sum["Inzidenz_7d"].iloc[-1]
    ir_df_lk_plot = ir_df_sum_lk(id_lk)
    faelle_neu_plot, todesfaelle_neu_plot = covid_faelle_neu(id_lk, True)
    max_y_covid = int(covid_df_sum["Inzidenz_7d"].max()) * 1.2
    # covid_major_yticks=np.arange(0,max_y_covid,50)
    # covid_minor_yticks = np.arange(25, max_y_covid, 25)
    fig, ax = plt.subplots(4, figsize=(10, 20))
    fig.suptitle(f"Covid Situation in {name_lk} \nStichtag: {today_str}", fontsize=20, weight='bold')
    ax[0].plot(covid_df_sum.index, covid_df_sum["Inzidenz_7d"], color='blue')
    ax[0].set_title(f"{name_lk} \n7-Tage Inzidenz")
    # ax[0].set_yticks(covid_major_yticks)
    # ax[0].set_yticks(covid_minor_yticks , minor=True)
    ax[0].yaxis.set_minor_locator(AutoMinorLocator(2))
    ax[0].yaxis.grid(which='minor', linestyle=':')
    ax[0].text(0.95, 0.90, f'{inzidenz:.1f}', horizontalalignment='right',
               verticalalignment='bottom', fontsize=16, color='red', weight='bold', transform=ax[0].transAxes)
    ax[0].plot(covid_df_sum.index[-1], inzidenz, marker='x', color='red', markersize=7, markeredgewidth=3)
    ax[1].plot(covid_df_sum.index, covid_df_sum["AnzahlTodesfall_7d_mean"], color='black')
    ax[1].set_title(f"{name_lk} \nCovid (Todes)-Fälle pro Tag im 7 Tage Mittel")
    ax[1].annotate('', xy=(date(2020, 10, 15), ax[1].get_ylim()[1] / 2),
                   xytext=(date(2020, 7, 1), ax[1].get_ylim()[1] / 2),
                   arrowprops=dict(arrowstyle="<-", color='red', linewidth=2))
    ax[1].annotate('', xy=(date(2021, 1, 20), ax[1].get_ylim()[1] * 0.7),
                   xytext=(date(2021, 3, 15), ax[1].get_ylim()[1] * 0.7),
                   arrowprops=dict(arrowstyle="<-", color='black', linewidth=2))
    ax1_2 = ax[1].twinx()
    ax1_2.plot(covid_df_sum.index, covid_df_sum["AnzahlFall_7d_mean"], color='red')
    ax1_2.set_ylabel('Anzahl Erkrankte 7d Mittel', fontsize=16, color='red')
    ax1_2.yaxis.tick_left()
    ax1_2.yaxis.set_label_position("left")
    ax1_2.tick_params(axis='y', labelcolor='red')
    props = dict(facecolor='lightgrey', alpha=1, edgecolor='none')
    ax[1].text(0.05, 0.85,
               f'Differenz zum Vortag\n'
               f'(Differenz zum letzten Report)'
               , horizontalalignment='left', transform=ax[1].transAxes,
               verticalalignment='bottom', fontsize=14, color='black', ma='left', weight='bold')
    ax[1].text(0.25, 0.8,
               f'Erkrankungen:\n'
               f'Todesfälle:'
               , horizontalalignment='right', bbox=props, transform=ax[1].transAxes,
               verticalalignment='top', fontsize=14, color='black', ma='left')
    ax[1].text(0.25, 0.8,
               f'{covid_df_sum["AnzahlFall"].iloc[-1]:.0f} ({faelle_neu_plot:.0f})\n'
               f'{covid_df_sum["AnzahlTodesfall"].iloc[-1]:.0f} ({todesfaelle_neu_plot:.0f})'
               , horizontalalignment='left', bbox=props, transform=ax[1].transAxes,
               verticalalignment='top', fontsize=14, color='black', ma='left')
    ax[2].plot(covid_df_sum.index, covid_df_sum["Cum_sum_Todesfall"], color='black')
    ax[2].set_title(f"{name_lk} \nKumulierte Covid (Todes) - Fälle")
    ax[2].annotate('', xy=(date(2020, 10, 15), ax[2].get_ylim()[1] / 2),
                   xytext=(date(2020, 7, 1), ax[2].get_ylim()[1] / 2),
                   arrowprops=dict(arrowstyle="<-", color='red', linewidth=2))
    ax[2].annotate('', xy=(date(2021, 1, 20), ax[2].get_ylim()[1] * 0.7),
                   xytext=(date(2021, 3, 15), ax[2].get_ylim()[1] * 0.7),
                   arrowprops=dict(arrowstyle="<-", color='black', linewidth=2))
    ax2_2 = ax[2].twinx()
    ax2_2.plot(covid_df_sum.index, covid_df_sum["Cum_sum"], color='red')
    ax2_2.set_ylabel('Kumulierte Anzahl Erkrankter', fontsize=16, color='red')
    ax2_2.yaxis.tick_left()
    ax2_2.yaxis.set_label_position("left")
    ax2_2.tick_params(axis='y', labelcolor='red')
    for item in (
            [ax1_2.title, ax1_2.xaxis.label, ax1_2.yaxis.label] + ax1_2.get_xticklabels() + ax1_2.get_yticklabels() +
            [ax2_2.title, ax2_2.xaxis.label, ax2_2.yaxis.label] + ax2_2.get_xticklabels() + ax2_2.get_yticklabels()):
        item.set_fontsize(16)

    ax[3].plot(ir_df_lk_plot['report_date'], ir_df_lk_plot["faelle_covid_aktuell_invasiv_beatmet"], color='orange',
               label="Covid Patienten ITS")
    ax[3].plot(ir_df_lk_plot['report_date'], ir_df_lk_plot["betten_frei"], color='lightblue',
               label="Freie IV Kapazität Gesamt")
    ax[3].set_title(f"{name_lk} \nIntensivbetten")
    ax[3].legend(prop={'size': 16})

    for axs in itertools.chain(ax.flat):
        axs.set_title(label=axs.get_title(), weight='bold')
        axs.set_ylabel('Anzahl', fontsize=16)
        axs.set_xlim([date(2020, 2, 20), covid_df_sum.index.max() + timedelta(days=7)])
        axs.yaxis.tick_right()
        axs.yaxis.set_label_position("right")
        axs.xaxis.grid()
        axs.yaxis.grid()
        axs.axvline(today, ls='-', color='gold', linewidth=1)
        for item in ([axs.title, axs.xaxis.label, axs.yaxis.label] + axs.get_xticklabels() + axs.get_yticklabels()):
            item.set_fontsize(16)
    ax[1].set_ylabel('Anzahl Todesfälle 7d Mittel', fontsize=16)
    ax[2].set_ylabel('Kumulierte Anzahl Todesfälle', fontsize=16)
    fig.align_ylabels()
    fig.tight_layout(rect=[0, 0, 1, 0.97], h_pad=2)
    plt.savefig(os.path.join(parent_directory, 'Auswertung', 'Landkreise', f"covid_lk_{id_lk}.png"),
                bbox_inches='tight', dpi=60)
    plt.show()
    plt.close(fig)


# %% Plot All BL
for key in number_states:
    plot_covid_bl(key)

# %% Plot certain LK
for id_ in lk_to_plot:
    plot_covid_lk(id_)
