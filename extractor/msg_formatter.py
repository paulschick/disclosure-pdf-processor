import typer


def format_msg(msg_components):
    msg = ''
    for component in msg_components:
        text = component[0]
        color = component[1]
        bold = component[2]
        styled = typer.style(text, fg=color, bold=bold)
        msg += styled
    typer.secho(msg)
