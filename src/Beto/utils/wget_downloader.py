from pathlib import Path
from Beto.utils.config import BRONZE_DIR
import pandas as pd
import wget


def procesar_descarga(df: pd.Series, carpeta_destino: Path) -> str:
    """Descarga una sola sentencia basándose en la fila del DataFrame."""
    url = df["urlInternet"]
    id = df["id_scjn"]
    if pd.isna(url):
        return "Sin URL"

    archivo_salida = carpeta_destino / f"sentencia_{id}.docx"
    try:
        # wget requiere strings
        wget.download(str(url), out=str(archivo_salida))
        return "Descargado"
    except Exception as error:
        return f"Error: {error}"


def wget_downloader1(archivo_csv: Path, ruta_salida: Path) -> None:
    """Lee el CSV de metadatos e inicia la descarga masiva de sentencias."""
    ruta_salida.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(archivo_csv)
    df["estado_descarga"] = df.apply(
        lambda fila: procesar_descarga(fila, ruta_salida), axis=1
    )
    print(df[["urlInternet", "estado_descarga"]].head())


ruta_salida = Path(BRONZE_DIR) / "scjn" / "sentencias" / "sentencias_docx"
archivo_csv = (
    Path(BRONZE_DIR) / "scjn" / "sentencias" / "metadatos" / "scjn_sentencias.csv"
)


def procesar_descarga(
    df: pd.Series, carpeta_destino: Path, col_id: str, col_url: str
) -> str:
    """Descarga una sola sentencia basándose en los nombres de columna provistos."""
    url = df[col_url]
    id_doc = df[col_id]

    if pd.isna(url):
        return "Sin URL"

    # Reemplaza caracteres inválidos para nombres de archivo si el ID es texto
    archivo_salida = carpeta_destino / f"sentencia_{str(id_doc).strip()}.docx"

    try:
        wget.download(str(url), out=str(archivo_salida))
        return "Descargado"
    except Exception as error:
        return f"Error: {error}"


def wget_downloader(
    archivo_csv: Path,
    ruta_salida: Path,
    col_url: str = "url",
    col_id: str = "id",
) -> None:
    ruta_salida.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(archivo_csv)

    if col_id not in df.columns or col_url not in df.columns:
        raise ValueError(
            f"Columnas no encontradas. El CSV contiene: {list(df.columns)}"
        )

    df["estado_descarga"] = df.apply(
        lambda fila: procesar_descarga(fila, ruta_salida, col_id, col_url),
        axis=1,
    )

    print(df[[col_url, "estado_descarga"]].head())


ruta_salida = Path(BRONZE_DIR) / "scjn" / "sentencias" / "sentencias_docx"
archivo_csv = (
    Path(BRONZE_DIR) / "scjn" / "sentencias" / "metadatos" / "scjn_sentencias.csv"
)

wget_downloader(archivo_csv, ruta_salida, col_id="id_scjn", col_url="urlInternet")
