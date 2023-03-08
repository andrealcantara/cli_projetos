from pathlib import Path
from typing import Optional

import typer

from projeto import __app_name__, __version__, db, config, ERRORS

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help='Mostrar a versão da aplicacao e sair',
            callback=_version_callback,
            is_eager=True)
) -> None:
    return


@app.command()
def init(db_path: str = typer.Option(str(db.DEFAULT_DB_FILE_PATH),
                                     "--db-path",
                                     "-db",
                                     prompt='Local da base de dados')) -> None:
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(f'Criacao do arquivo de configuracao falhou com o error {[ERRORS[app_init_error]]}',
                    fg=typer.colors.RED, )
        raise typer.Exit(1)
    db_init_error = db.init_database(Path(db_path))
    if db_init_error:
        typer.secho(f'Criacao do banco de dados falhou com o error {[ERRORS[app_init_error]]}',
                    fg=typer.colors.RED, )
        raise typer.Exit(1)
    else:
        typer.secho(f'O DB do projeto é {db_path}.', fg=typer.colors.GREEN)

def add_project(name: str = typer.Option(None,
                                     "--name",
                                     "-n",
                                     prompt='Nome do Projeto')) -> None:

    return
