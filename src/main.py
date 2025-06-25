import typer
from rich.console import Console
from rich.table import Table
from config import load_config
from extractor import extract_submissions
from analyzer import analyze_submissions

app = typer.Typer()
console = Console()

@app.command()
def correct(
    submissions_zip: str = typer.Argument(..., help="ZIP file with student submissions"),
    config_file: str = typer.Option("config.yaml", help="YAML config file"),
    workdir: str = typer.Option("workdir", help="Work directory for extracted files"),
):
    """
    Correct C submissions and print results.
    """
    console.print("[bold blue]Extracting submissions...[/bold blue]")
    students = extract_submissions(submissions_zip, workdir)
    config = load_config(config_file)
    results = analyze_submissions(config, workdir)

    table = Table(title="Correction Results")
    table.add_column("Student")
    table.add_column("Points", justify="right")
    table.add_column("Errors")

    for res in results:
        table.add_row(res["student"], str(res["points"]), ", ".join(res["errors"]))

    console.print(table)

if __name__ == "__main__":
    app()
