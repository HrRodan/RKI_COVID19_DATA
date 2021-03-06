#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import DownloadFile
import os

def download_RKI_Fallzahlen():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..','..', 'Fallzahlen', 'raw_data')
    filename_kum = 'Fallzahlen_Kum_Tab.xlsx'
    url_kum = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Fallzahlen_Kum_Tab.xlsx?__blob=publicationFile"
    filename_archiv = 'Fallzahlen_Archiv.xlsx'
    url_archiv = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Fallzahlen_Archiv.xlsx?__blob=publicationFile"

    #download kum
    a = DownloadFile(url=url_kum, filename=filename_kum, download_path=data_path, compress=False,add_date=True,add_latest=False)
    a.write_file()

    # #download archiv
    # b = DownloadFile(url=url_archiv, filename=filename_archiv, download_path=data_path, compress=False,add_date=True,add_latest=False)
    # b.write_file()