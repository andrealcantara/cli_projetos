import configparser
import json
import os
from pathlib import Path
from typing import Dict, Any, NamedTuple, List

import typer

from projeto import DB_WRITE_ERROR, SUCCESS, JSON_ERROR, DB_READ_ERROR, NOT_FOUND

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB_FILE_PATH = os.path.join(BASE_DIR, 'base-dados.json')


def get_database_path(config_file: Path) -> Path:
    """Return the current path to the to-do database."""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])


def init_database(db_path: Path) -> int:
    """Create the to-do database."""
    try:
        db_path.write_text("[]")  # Empty projects
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR


class DBResponse(NamedTuple):
    projetos: List[Dict[str, Any]]
    error: int


class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    def ler_projetos(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                except json.JSONDecodeError:  # Catch wrong JSON format
                    return DBResponse([], JSON_ERROR)
        except OSError:  # Catch file IO problems
            return DBResponse([], DB_READ_ERROR)

    def escrever_projetos(self, projetos: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(projetos, db, indent=4)
            return DBResponse(projetos, SUCCESS)
        except OSError:
            return DBResponse(projetos, DB_WRITE_ERROR)

    def buscar_projetos(self, value: str, field: str = 'name') -> DBResponse:
        db_response = self.ler_projetos()
        if db_response.error:
            return db_response
        for db in db_response.projetos:
            if db.get(field) == value:
                return DBResponse([db], SUCCESS)
        return DBResponse([], NOT_FOUND)
