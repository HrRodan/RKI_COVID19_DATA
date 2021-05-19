#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import DownloadFile
import os

def download_Intensivregister():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..','..', 'Intensivregister', 'raw_data')
    filename_tagesdaten = 'DIVI_Intensivregister_Auszug_pro_Landkreis.csv'
    url_tagesdaten = "https://diviexchange.blob.core.windows.net/%24web/DIVI_Intensivregister_Auszug_pro_Landkreis.csv"
    filename_zeitreihe = 'bundesland-zeitreihe.csv'
    url_zeitreihe = "https://diviexchange.blob.core.windows.net/%24web/bundesland-zeitreihe.csv"
    filename_zeitreihe_tagesdaten = 'zeitreihe-tagesdaten.csv'
    url_zeitreihe_tagesdaten="https://diviexchange.blob.core.windows.net/%24web/zeitreihe-tagesdaten.csv"

    #download Tagedaten
    a = DownloadFile(url=url_tagesdaten, filename=filename_tagesdaten, download_path=data_path, compress=True,add_date=True,add_latest=False)
    a.write_file()

    #download Zeitreihe
    b = DownloadFile(url=url_zeitreihe, filename=filename_zeitreihe, download_path=data_path, compress=False,add_date=False,add_latest=False)
    b.write_file()

    # download Zeitreihe
    c = DownloadFile(url=url_zeitreihe_tagesdaten, filename=filename_zeitreihe_tagesdaten, download_path=data_path, compress=False,
                     add_date=False, add_latest=False)
    c.write_file()