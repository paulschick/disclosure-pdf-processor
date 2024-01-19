import configparser
from pathlib import Path
import typer

from extractor import (
    DIR_ERROR, FILE_ERROR, CONFIG_WRITE_ERROR, SUCCESS, __app_name__
)

CONFIG_DIR_PATH = Path(typer.get_app_dir(__app_name__))
CONFIG_FILE_PATH = CONFIG_DIR_PATH / "config.ini"


def init_app() -> int:
    try:
        CONFIG_DIR_PATH.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        CONFIG_FILE_PATH.touch(exist_ok=True)
    except OSError:
        return FILE_ERROR
    return _create_data_dirs()


def _create_data_dirs() -> int:
    config_parser = configparser.ConfigParser()
    data_dir = CONFIG_DIR_PATH / 'data'
    config_parser['default'] = {
        'data_dir': str(data_dir),
        'images_dir': str(data_dir / 'images'),
        'csv_dir': str(data_dir / 'csv'),
        'failed_file': str(data_dir / 'failed.txt'),
    }
    typer.secho(
        f'Creating directories and files in "{CONFIG_DIR_PATH}"',
        fg=typer.colors.BLUE)
    try:
        with CONFIG_FILE_PATH.open('w') as config_file:
            config_parser.write(config_file)
        typer.secho(f'\tCreated "{CONFIG_FILE_PATH}"', fg=typer.colors.BLUE)
    except OSError:
        return CONFIG_WRITE_ERROR
    # make directories and file
    try:
        data_dir.mkdir(exist_ok=True)
    except OSError:
        return DIR_ERROR
    try:
        (data_dir / 'images').mkdir(exist_ok=True)
        typer.secho(f'\tCreated "{data_dir / "images"}"', fg=typer.colors.BLUE)
    except OSError:
        return DIR_ERROR
    try:
        (data_dir / 'csv').mkdir(exist_ok=True)
        typer.secho(f'\tCreated "{data_dir / "csv"}"', fg=typer.colors.BLUE)
    except OSError:
        return DIR_ERROR
    try:
        (data_dir / 'failed.txt').touch(exist_ok=True)
        typer.secho(f'\tCreated "{data_dir / "failed.txt"}"', fg=typer.colors.BLUE)
    except OSError:
        return FILE_ERROR
    return SUCCESS
