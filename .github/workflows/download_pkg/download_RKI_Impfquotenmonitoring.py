#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from . import DownloadFile


def download_RKI_Impfquotenmonitoring():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'Impfquotenmonitoring',
                             'raw_data')
    filename = 'RKI_COVID19_Impfquotenmonitoring.xlsx'
    url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.xlsx?__blob=publicationFile"
    url_github_bl = "https://raw.githubusercontent.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/master/Aktuell_Deutschland_Bundeslaender_COVID-19-Impfungen.csv"
    url_github_lk = "https://raw.githubusercontent.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/master/Aktuell_Deutschland_Landkreise_COVID-19-Impfungen.csv"
    filename_github_bl = "Aktuell_Deutschland_Bundeslaender_COVID-19-Impfungen.csv"
    filename_github_lk = "Aktuell_Deutschland_Landkreise_COVID-19-Impfungen.csv"

    a = DownloadFile(url=url, filename=filename, download_path=data_path, compress=False, add_date=True,
                     add_latest=False)
    a.write_file()

    b = DownloadFile(url=url_github_bl, filename=filename_github_bl, download_path=data_path, compress=False,
                     add_date=False, add_latest=False)
    b.write_file()

    b = DownloadFile(url=url_github_lk, filename=filename_github_lk, download_path=data_path, compress=False,
                     add_date=False, add_latest=False)
    b.write_file()
