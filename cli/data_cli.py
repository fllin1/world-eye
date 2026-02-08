from pathlib import Path

import typer

from src.data.data_ingestor import DataIngestorFactory

app = typer.Typer()


@app.command()
def ingest(file_path: str, remove_temp: bool = True):
    """Ingest data from the given file path."""
    file_path = Path(file_path).absolute()

    assert file_path.exists(), f"File {file_path} does not exist."
    assert file_path.is_file(), f"File {file_path} is not a file."

    file_extension = file_path.suffix
    ingestor = DataIngestorFactory.get_ingestor(file_extension)
    df = ingestor.ingest(file_path, remove_temp=remove_temp)
    typer.echo(f"Data ingested from {file_path}.")
    typer.echo(df.head())


if __name__ == "__main__":
    app()
