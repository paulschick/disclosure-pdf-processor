import os
from pathlib import Path
import pandas as pd
from internal.extract_with_regions import ExtractorV1

# Immutable
MAX_ROW_KEY = 'display.max_rows'
DEFAULT_MAX_ROWS = pd.get_option(MAX_ROW_KEY)
TEST_IMG_1_NAME = '2024-1-Lloyd-Doggett-20024268.png'


def get_samples_dir() -> Path:
    return Path(os.getcwd()).parent / 'samples'


def get_image_path(image_name=None) -> Path:
    if image_name:
        return get_samples_dir() / image_name
    return get_samples_dir() / TEST_IMG_1_NAME


def get_create_csv_dir():
    csv_dir = Path(os.getcwd()).parent / 'csv'
    if not csv_dir.exists():
        csv_dir.mkdir()
    return csv_dir


def get_csv_path(image_name=None) -> Path:
    if not image_name:
        image_name = TEST_IMG_1_NAME
    image_name = image_name.split('.')[0]
    return get_create_csv_dir() / f'{image_name}.csv'


def write_if_not_exists(df: pd.DataFrame, image_name=None) -> None:
    csv_path = get_csv_path(image_name)
    if not csv_path.exists():
        df.to_csv(csv_path, index=False)


def example_print_confidences(df: pd.DataFrame):
    """
    Example of how to print confidences
    Don't use this for determining if a line is valid
    it misses key information like the date
    """
    print(f'Length of df without conf over 90: {len(df)}')
    df_under = df[df['conf'] < 90]
    df = df[df['conf'] > 90]
    print(f'Length of df with conf over 90: {len(df)}')
    print(f'Length of df with conf under 90: {len(df_under)}')
    pd.set_option(MAX_ROW_KEY, None)
    print(df_under[['conf', 'text']])
    pd.set_option(MAX_ROW_KEY, DEFAULT_MAX_ROWS)
    print(df.head())


def print_text_lines(text: str) -> None:
    lines = text.split('\n')
    i = 0
    for line in lines:
        if line:
            print(f'{i}: {line}')
            i += 1


if __name__ == '__main__':
    extractor = ExtractorV1(str(get_image_path()))
    text = extractor.extract_text()
    print_text_lines(text)
    df = extractor.extract_to_df()
    example_print_confidences(df)
    write_if_not_exists(df)
