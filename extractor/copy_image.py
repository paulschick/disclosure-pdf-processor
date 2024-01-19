import shutil

from extractor import DIR_ERROR, IMAGE_COPY_ERROR, SUCCESS, config
import typer
import os


def copy_images_if_not_present() -> int:
    conf = config.get_config()
    image_source_dir = conf.image_source_directory
    images_dir = conf.images_dir
    typer.secho(f'Copying images from {image_source_dir} to {images_dir}',
                fg=typer.colors.BLUE)
    existing_images = set(os.listdir(images_dir))
    typer.echo(f'Skipping {len(existing_images)} existing images')
    if not image_source_dir.exists():
        typer.secho(f'Image source directory {image_source_dir} does not exist',
                    fg=typer.colors.RED)
        return DIR_ERROR

    for parent_dir in image_source_dir.iterdir():
        if parent_dir.is_dir():
            for file in parent_dir.iterdir():
                if file.suffix == '.png':
                    if file.name not in existing_images:
                        typer.echo(f'Copying {file.name}')
                        try:
                            shutil.copy(file, images_dir)
                        except OSError:
                            typer.secho(f'Copying {file.name} failed',
                                        fg=typer.colors.RED)
                            return IMAGE_COPY_ERROR

    existing_images = set(os.listdir(images_dir))
    typer.secho(f'Copied {len(existing_images)} images',
                fg=typer.colors.GREEN)

    return SUCCESS
