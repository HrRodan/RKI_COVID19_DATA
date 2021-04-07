from download_pkg import *
import os
from datetime import datetime, date, time
import holidays
import pytz

t_now=datetime.now(pytz.timezone('Europe/Berlin')).time()
today=datetime.now(pytz.timezone('Europe/Berlin')).date()
day_of_week=today.isoweekday()
de_holidays = holidays.CountryHoliday('DE')
t_14=time(hour=14)
t_22=time(hour=22)
print(f"Starting at {t_now}")

#%% each day
try:
    print("Downloading daily RKI Covid Data...")
    download_RKI_COVID19()
except Exception as e:
    print(e)

if t_now>=t_22:
    try:
        print("Downloading daily RKI Nowcasting...")
        download_RKI_Nowcasting()
    except Exception as e:
        print(e)

if t_now>=t_14:
    try:
        print("Downloading daily Intensivregister...")
        download_Intensivregister()
    except Exception as e:
        print(e)

#%% each working day (including saturday)
if day_of_week in range(1,7) and today not in de_holidays and t_now>=t_14:
    try:
        print("Downloading daily RKI Fallzahlen..")
        download_RKI_Fallzahlen()
    except Exception as e:
        print(e)

    try:
        print("Downloading daily Impfquotenmonitoring...")
        download_RKI_Impfquotenmonitoring()
    except Exception as e:
        print(e)


#%% each Tuesday
if day_of_week==2 and t_now>=t_22:
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
if day_of_week==3 and t_now>=t_22:
    print("Wednesday Download starting...")
    try:
        print("Downloading RKI Testzahlen..")
        download_RKI_Testzahlen()
    except Exception as e:
        print(e)

#%% each Friday
if day_of_week==5 and t_now>=t_22:
    print("Friday Download starting...")
    try:
        print("Downloading RKI Todesfaelle..")
        download_RKI_Todesfaelle()
    except Exception as e:
        print(e)