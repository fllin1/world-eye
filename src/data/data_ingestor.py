import shutil
import zipfile
from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd

from src.config import EXTERNAL_DATA_DIR, RAW_DATA_DIR


class DataIngestor(ABC):
    @abstractmethod
    def ingest(self) -> pd.DataFrame:
        """Ingest data from the source and return a pandas DataFrame."""
        pass


class ZipDataIngestor(DataIngestor):
    def ingest(self, zip_path: Path, remove_temp: bool = True) -> pd.DataFrame:
        """Ingest data from a zip file and return a pandas DataFrame."""

        assert zip_path.exists(), f"Zip file {zip_path} does not exist."
        assert zip_path.suffix == ".zip", f"Zip file {zip_path} is not a zip file."

        temp_dir = zip_path.parent / "temp"

        with zipfile.ZipFile(zip_path, "r") as zip_file:
            zip_file.extractall(temp_dir)

        csv_files = list(temp_dir.glob("*.csv"))

        if len(csv_files) != 1:
            raise ValueError(f"Expected 1 CSV file, but got {len(csv_files)}.")

        file_path = csv_files[0]
        df = pd.read_csv(file_path)

        df.to_csv(RAW_DATA_DIR / file_path.name, index=False)
        if remove_temp:
            shutil.rmtree(temp_dir)

        return df


class DataIngestorFactory:
    @staticmethod
    def get_ingestor(file_extension: str) -> DataIngestor:
        """Get the appropriate data ingestor for the given file extension."""
        if file_extension == ".zip":
            return ZipDataIngestor()
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")


if __name__ == "__main__":
    zip_path = EXTERNAL_DATA_DIR / "fertility-vs-gdp.zip"

    ingestor = DataIngestorFactory.get_ingestor(".zip")
    df = ingestor.ingest(zip_path, remove_temp=False)
    print(df.head())
