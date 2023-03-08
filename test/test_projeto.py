from typer.testing import CliRunner

from projeto import cli, __version__, __app_name__
from projeto.db import DEFAULT_DB_FILE_PATH

runner = CliRunner()


def test_version():
    result = runner.invoke(cli.app, ["-v"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}"

def test_init():
    result = runner.invoke(cli.app, ['init'])
    assert result.exit_code == 0
    assert f"O DB do projeto é {DEFAULT_DB_FILE_PATH}."
