from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
INTERIM_DATA_DIR = DATA_DIR / "interim"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

DATA_SOURCES = {
    "fertility-vs-gdp": {
        "url": "https://ourworldindata.org/grapher/children-per-woman-fertility-rate-vs-level-of-prosperity",
    }
}
