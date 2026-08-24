from pathlib import Path


def get_project_root() -> Path:
    """Busca la raíz del proyecto basada en la presencia de pyproject.toml."""
    current_path = Path(__file__).resolve()
    for parent in current_path.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    return current_path.parent


PROJECT_ROOT = get_project_root()
BETO_ROOT = PROJECT_ROOT / "src" / "Beto"
PIPE_DIR = BETO_ROOT / "pipeline"
DATA_DIR = PROJECT_ROOT / "data"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"
