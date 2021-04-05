#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from download_pkg import DownloadFile
import os
from datetime import date, timedelta

#%% Start
def download_DIVI_Archiv(dl_date, dl_number):
    date_str=dl_date.strftime('%Y-%m-%d')
    if dl_date<date(2020,6,11):
        suffix=['12-15','09-15']
    elif dl_date<date(2020,6,26):
        suffix=['12-15-2']
    elif dl_date==date(2020,9,14):
        suffix=['14-15']
    else:
        suffix=['12-15']
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..','..', 'Intensivregister', 'raw_data')
    filename_archiv = f'DIVI_Intensivregister_Auszug_pro_Landkreis_{date_str}.csv'
    url_archive_base= "https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv/viewdocument/{num}/divi-intensivregister-{date_str}-{suffix}"
    print(url_archive_base.format(date_str=date_str, suffix=suffix[0], num=dl_number))
    #download Tagedaten
    for s in suffix:
        try:
            a = DownloadFile(url=url_archive_base.format(date_str=date_str, suffix=s, num=str(dl_number)), filename=filename_archiv, download_path=data_path, compress=True,add_date=False,add_latest=False, verbose=False)
            a.write_file()
            return True
            break
        except:
            print("not available")
    return False

#%% Start
#Parameter nach Bedarf anpassen. Die IDs in der URL sind nicht nur aufsteigend mit steigendem Datum.
dl_date_start=date(2020,6,5)
dl_date_end=date(2021,4,4)
dl_dates=[dl_date_start+timedelta(days=x) for x in range((dl_date_end-dl_date_start).days+1)]
numbers=iter(list(range(5055,5581)))

for dl_date in dl_dates:
    while True:
        num=next(numbers)
        a=download_DIVI_Archiv(dl_date,num)
        if a:
            break
        #print(num)
        #numbers.remove(num)
