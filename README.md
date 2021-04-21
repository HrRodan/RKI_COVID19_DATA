# RKI_COVID19_DATA

Zusammengesammeltes Archiv von RKI COVID19-Dashboard Datenbank Dumps ab `2020-03-21`.

Repo wurde initial geforkt von https://github.com/micb25/RKI_COVID19_DATA und anschließend erweitert.

Sekundäre Quellen in separaten Ordnern:

- Impfquotenmonitoring
- Nowcasting
- Testzahlen
- Intensivregister 
- Todesfälle
- Klinische Aspekte
- Ausbruchsdaten
- Testzahlen

Update aller Quellen jeden Tag um 8, 14 und 22 Uhr.

Zusammgenstellte Daten zur einfachen Verarbeitung:

- Die Tagesreports aus dem DIVI Intensivregister wurden [zusammengefasst](https://github.com/HrRodan/RKI_COVID19_DATA/blob/master/Intensivregister/DIVI_Intensivregister_Auszug_pro_Landkreis.csv), um ein Verlauf auf Landkreisebene darzustellen.
  Das DIVI Register stellt Verlaufsdaten nur auf Bundeslandebene bereit.
- Die Fallzahlen, die jeden Tag vom RKI neu berichtet werden, also die Differenz zum Vortag für Neuinfektionen und Todesfälle, wurden aus allen RKI-Dumps ermittelt
und für jeden Reportingtag auf Landkreisebene [aggregiert](https://github.com/HrRodan/RKI_COVID19_DATA/blob/master/Fallzahlen/RKI_COVID19_Fallzahlen.csv). Vom RKI selbst wird der [Verlauf der Tagesdifferenzen](https://github.com/HrRodan/RKI_COVID19_DATA/tree/master/Fallzahlen/raw_data) nur für Gesamtdeutschland angeboten.

Quellenvermerk: 
- Robert Koch-Institut (RKI), [dl-de/by-2-0](https://www.govdata.de/dl-de/by-2-0)
- DIVI-Intensivregister (www.intensivregister.de)

CSV-Quelle (aktueller Tag):
- [https://www.arcgis.com/home/item.html?id=f10774f1c63e40168479a1feb6c7ca74](https://www.arcgis.com/home/item.html?id=f10774f1c63e40168479a1feb6c7ca74)

CSV-Quellen (archiviert):
- [https://github.com/ard-data/2020-rki-archive/tree/master/data/0_archived](https://github.com/ard-data/2020-rki-archive/tree/master/data/0_archived)
- [https://github.com/ihucos/rki-covid19-data](https://github.com/ihucos/rki-covid19-data)
- [https://github.com/CharlesStr/CSV-Dateien-mit-Covid-19-Infektionen-](https://github.com/CharlesStr/CSV-Dateien-mit-Covid-19-Infektionen-)
- [https://raw.githubusercontent.com/jenslaufer/Data2Decision/0ae8e98bcb91927c7740c0204fb164c0078a9495/data/CoV_data/RKI_COVID19.csv](https://raw.githubusercontent.com/jenslaufer/Data2Decision/0ae8e98bcb91927c7740c0204fb164c0078a9495/data/CoV_data/RKI_COVID19.csv)
- [https://raw.githubusercontent.com/musicplanet/covid-data-de/b90943b18a102a7be24953d3941801e8a54aa119/RKI_COVID19-210322020.csv](https://raw.githubusercontent.com/musicplanet/covid-data-de/b90943b18a102a7be24953d3941801e8a54aa119/RKI_COVID19-210322020.csv)


