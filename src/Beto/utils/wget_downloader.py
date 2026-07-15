from pathlib import Path
from Beto.utils.config import BRONZE_DIR
import pandas as pd


def wget_downloader(archivo_csv):
    df = pd.read_csv(archivo_csv)
    print(df)


archivo_csv = Path(BRONZE_DIR) / "scjn" / "sentencias" / "scjn_sentencias.csv"
wget_downloader(archivo_csv)
