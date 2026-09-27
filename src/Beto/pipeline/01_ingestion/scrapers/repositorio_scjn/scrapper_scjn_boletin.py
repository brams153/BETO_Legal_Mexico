import logging
from pathlib import Path
import pandas as pd
import wget

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def descargar_archivo(
    url: str,
    id_doc: str,
    carpeta_destino: Path,
    prefijo: str = "doc_",
    extension: str = ".docx",
    sobreescribir: bool = False,
) -> str:
    """
    Descarga un archivo individual y lo guarda con el formato: {prefijo}{id_doc}{extension}.
    """
    if pd.isna(url) or not str(url).strip():
        return "Sin URL"

    id_limpio = str(id_doc).strip().replace("/", "-")
    nombre_archivo = f"{prefijo}{id_limpio}{extension}"
    archivo_salida = carpeta_destino / nombre_archivo

    if not sobreescribir and archivo_salida.exists():
        return "Ya existía"

    try:
        # bar=None evita que wget inunde la consola con barras de progreso individuales
        wget.download(str(url), out=str(archivo_salida), bar=None)
        return "Descargado"
    except Exception as error:
        return f"Error: {error}"


def descargar_desde_csv(
    archivo_csv: Path,
    ruta_salida: Path,
    col_url: str = "url",
    col_id: str = "id",
    prefijo: str = "sentencia_",
    extension: str = ".docx",
) -> pd.DataFrame:
    """
    Lee un CSV de metadatos e inicia la descarga masiva de archivos.
    Retorna el DataFrame actualizado con el estado de las descargas.
    """
    ruta_salida.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(archivo_csv)

    if col_id not in df.columns or col_url not in df.columns:
        raise ValueError(
            f"Faltan columnas requeridas. El CSV solo contiene: {list(df.columns)}"
        )

    logging.info(f"Iniciando procesamiento de {len(df)} registros...")

    df["estado_descarga"] = df.apply(
        lambda fila: descargar_archivo(
            url=fila[col_url],
            id_doc=fila[col_id],
            carpeta_destino=ruta_salida,
            prefijo=prefijo,
            extension=extension,
        ),
        axis=1,
    )

    # Resumen de resultados
    resumen = df["estado_descarga"].value_counts()
    logging.info(f"Resumen de descargas:\n{resumen}")

    return df


if __name__ == "__main__":
    from Beto.utils.config import BRONZE_DIR

    ruta_salida = Path(BRONZE_DIR) / "scjn" / "sentencias" / "sentencias_docx"
    archivo_csv = (
        Path(BRONZE_DIR) / "scjn" / "sentencias" / "metadatos" / "scjn_sentencias.csv"
    )

    df_resultado = descargar_desde_csv(
        archivo_csv=archivo_csv,
        ruta_salida=ruta_salida,
        col_id="id_scjn",
        col_url="urlInternet",
        prefijo="sentencia_",
        extension=".docx",
    )
