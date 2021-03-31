__all__ = ["DownloadFile","download_RKI_COVID19",'download_Intensivregister','download_RKI_Altersverteilung',
           'download_RKI_Fallzahlen','download_RKI_Ausbruchsdaten','download_RKI_Impfquotenmonitoring',
           'download_RKI_Klinische_Aspekte','download_RKI_Nowcasting','download_RKI_Testzahlen','download_RKI_Todesfaelle']

from .DownloadFile import DownloadFile
from .download_RKI_COVID19 import download_RKI_COVID19
from .download_Intensivregister import download_Intensivregister
from .download_RKI_Fallzahlen import download_RKI_Fallzahlen
from .download_RKI_Ausbruchsdaten import download_RKI_Ausbruchsdaten
from .download_RKI_Altersverteilung import download_RKI_Altersverteilung
from .download_RKI_Impfquotenmonitoring import download_RKI_Impfquotenmonitoring
from .download_RKI_Klinische_Aspekte import download_RKI_Klinische_Aspekte
from .download_RKI_Nowcasting import download_RKI_Nowcasting
from .download_RKI_Testzahlen import download_RKI_Testzahlen
from .download_RKI_Todesfaelle import download_RKI_Todesfaelle
