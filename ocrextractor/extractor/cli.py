import typer
from extractor import __app_name__, __version__, config, ERRORS
from typing import Optional

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
            help="Show the application's version and exit",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return


@app.command()
def init() -> None:
    app_init_err = config.init_app()
    if app_init_err:
        typer.secho(
            f'Creating directories and files failed with error: "{ERRORS[app_init_err]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f'Created directories and files in "{config.CONFIG_DIR_PATH}"',
            fg=typer.colors.GREEN,
        )


if __name__ == '__main__':
    app()
