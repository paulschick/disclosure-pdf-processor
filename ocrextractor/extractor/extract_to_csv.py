import typer
import pytesseract
import os
import cv2
import pandas as pd
from extractor import DIR_ERROR, SUCCESS, config
from extractor.msg_formatter import format_msg

# TODO - add to config
# Should be optional, use fastest by default
tessdata_dir_config = r'--tessdata-dir /usr/share/tesseract-ocr/5/tessdata_best-4.1.0'


def extract_to_csv_if_not_present(limit=None) -> int:
    failed = []
    conf = config.get_config()
    failed_file = conf.failed_file
    with open(failed_file, 'r') as f:
        existing_failed = f.readlines()
    existing_failed = [x.strip() for x in existing_failed]
    csv_dir = conf.csv_dir
    images_dir = conf.images_dir

    msg = [
        ('Extracting images from', typer.colors.BRIGHT_BLUE, True),
        (f' {images_dir} ', typer.colors.BRIGHT_WHITE, False),
        ('to', typer.colors.BRIGHT_BLUE, False),
        (f' {csv_dir}', typer.colors.BRIGHT_WHITE, False),
    ]
    print()
    format_msg(msg)
    print()

    existing_csvs = set(os.listdir(csv_dir))

    msg = [
        ('Skipping', typer.colors.BRIGHT_RED, True),
        (f' {len(existing_csvs)} ', typer.colors.GREEN, False),
        ('existing csvs', typer.colors.BRIGHT_WHITE, False),
    ]
    format_msg(msg)
    print()

    if not images_dir.exists():
        typer.secho(f'Image source directory {images_dir} does not exist',
                    fg=typer.colors.RED)
        return DIR_ERROR

    i = 0
    for image_path in images_dir.iterdir():
        if image_path.suffix == '.png' and (i < limit if limit else True):
            image_name = image_path.name
            csv_name = image_name.split('.png')[0] + '.csv'
            csv_path = csv_dir / csv_name

            if csv_name not in existing_csvs and image_name not in existing_failed:
                msg = [
                    ('Extracting', typer.colors.BRIGHT_BLUE, True),
                    (f'\t{i + 1}', typer.colors.GREEN, False),
                    (f': {image_name} to {csv_name}', typer.colors.BRIGHT_WHITE, False),
                ]
                format_msg(msg)

                try:
                    df = _extract_to_df(str(image_path))
                    if not csv_path.exists():
                        msg = [
                            ('Writing to', typer.colors.BLUE, False),
                            (f' {csv_name}', typer.colors.BRIGHT_WHITE, False),
                        ]
                        format_msg(msg)
                        df.to_csv(csv_path, index=False)
                    else:
                        msg = [
                            (csv_name, typer.colors.BRIGHT_WHITE, False),
                            (' Already exists', typer.colors.BRIGHT_RED, True),
                        ]
                        format_msg(msg)
                except TypeError:
                    msg = [
                        (image_name, typer.colors.BRIGHT_WHITE, False),
                        (' Image Type Not Supported.', typer.colors.RED, False),
                    ]
                    format_msg(msg)
                    failed.append(image_path)

                i += 1
        elif limit and i >= limit:
            break

    total_failed = len(failed)
    msg = [
        ('Failed to extract', typer.colors.BRIGHT_RED, True),
        (f' {total_failed} ', typer.colors.GREEN, False),
        ('images', typer.colors.BRIGHT_WHITE, False),
    ]
    format_msg(msg)

    if total_failed > 0:
        msg = [
            ('Writing failed images to', typer.colors.BRIGHT_BLUE, True),
            (f' {failed_file}', typer.colors.BRIGHT_WHITE, False),
        ]
        format_msg(msg)
        with open(failed_file, 'a') as f:
            for image_path in failed:
                if image_path.name not in existing_failed:
                    f.write(image_path.name + '\n')

    return SUCCESS


def _mark_regions(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 30)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilate = cv2.dilate(thresh, kernel, iterations=4)

    cnts = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    image = None

    line_items_coordinates = []
    for c in cnts:
        area = cv2.contourArea(c)
        x, y, w, h = cv2.boundingRect(c)

        if y >= 600 and x <= 1000:
            if area > 10000:
                image = cv2.rectangle(img, (x, y), (2200, y + h), color=(255, 0, 255), thickness=3)
                line_items_coordinates.append([(x, y), (2200, y + h)])
            if y >= 2400 and x <= 2000:
                image = cv2.rectangle(img, (x, y), (2200, y + h), color=(255, 0, 255), thickness=3)
                line_items_coordinates.append([(x, y), (2200, y + h)])

    return image, line_items_coordinates


def _get_threshold(image_path):
    img, _ = _mark_regions(image_path)
    ret, thresh = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    return thresh


def _extract_text(image_path):
    thresh = _get_threshold(image_path)
    return pytesseract.image_to_string(thresh, config=tessdata_dir_config)


def _extract_to_df(image_path):
    thresh = _get_threshold(image_path)
    data: pd.DataFrame = pytesseract.image_to_data(
        thresh,
        config=tessdata_dir_config,
        output_type=pytesseract.Output.DATAFRAME
    )
    return data[data['text'].notnull()]
