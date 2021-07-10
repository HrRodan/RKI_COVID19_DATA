#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import DownloadFile
import os

def download_RKI_Nowcasting():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..','..', 'Nowcasting', 'raw_data')
    print(data_path)
    filename = 'Nowcasting_Zahlen_csv.csv'
    url = "https://raw.githubusercontent.com/robert-koch-institut/SARS-CoV-2-Nowcasting_und_-R-Schaetzung/main/Nowcast_R_aktuell.csv"

    a = DownloadFile(url=url, filename=filename, download_path=data_path, compress=True,add_date=True,add_latest=False)
    a.write_file()
