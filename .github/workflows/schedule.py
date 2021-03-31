from download_pkg import *
import os
from datetime import datetime, date
import holidays

today=date.today()
day_of_week=today.isoweekday()
de_holidays = holidays.CountryHoliday('DE')

#%% each day
try:
    print("Downloading daily RKI Covid Data...")
    download_RKI_COVID19()
except Exception as e:
    print(e)

try:
    print("Downloading daily RKI Nowcasting...")
    download_RKI_Nowcasting()
except Exception as e:
    print(e)

try:
    print("Downloading daily Intensivregister...")
    download_Intensivregister()
except Exception as e:
    print(e)

try:
    print("Downloading daily Impfquotenmonitoring...")
    download_RKI_Impfquotenmonitoring()
except Exception as e:
    print(e)

#%% each working day
if day_of_week in range(1,6) and today not in de_holidays:
    try:
        print("Downloading daily RKI Fallzahlen..")
        download_RKI_Fallzahlen()
    except Exception as e:
        print(e)

#%% each Tuesday
if day_of_week==2:
    print("Tuesday Download starting...")
    try:
        print("Downloading RKI Altersverteilung..")
        download_RKI_Altersverteilung()
    except Exception as e:
        print(e)

    try:
        print("Downloading RKI Klinische Aspekte..")
        download_RKI_Klinische_Aspekte()
    except Exception as e:
        print(e)

    try:
        print("Downloading RKI Ausbruchsdaten..")
        download_RKI_Ausbruchsdaten()
    except Exception as e:
        print(e)

#%% each Wednesday
if day_of_week==3:
    print("Wednesday Download starting...")
    try:
        print("Downloading RKI Testzahlen..")
        download_RKI_Testzahlen()
    except Exception as e:
        print(e)

#%% each Friday
if day_of_week==5:
    print("Friday Download starting...")
    try:
        print("Downloading RKI Todesfaelle..")
        download_RKI_Todesfaelle()
    except Exception as e:
        print(e)