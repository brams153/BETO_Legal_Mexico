import importlib
from Beto.utils.config import PIPE_DIR, BRONZE_DIR
from Beto.utils.client import obtener_cliente_http

modulo_scjn = importlib.import_module(
    "Beto.pipeline.01_ingestion.scrapers.repositorio_scjn.scrapper_scjn"
)

ExtraerSCJN = modulo_scjn.ExtraerSCJN


class ExtraerSCJN_boletin(ExtraerSCJN):
    def __init__(
        self,
        session,
        output_path,
        pagina_n,
        params,
        url_base,
        diccionario_completo,
        diccionario_ids_urls,
    ):
        super().__init__(
            session,
            output_path,
            pagina_n,
            params,
            url_base,
            diccionario_completo,
            diccionario_ids_urls,
        )
        self.output_path = BRONZE_DIR / "scjn" / "boletines" / "metadatos"
        self.output_path.mkdir(parents=True, exist_ok=True)
        self.url_base = "https://scjn.gob.mx"

    def obtener_urls_docx(self):
        nuevos_filtros = ["urlInternet", "boletin"]
        return super().obtener_urls_docx(filtros=nuevos_filtros)
