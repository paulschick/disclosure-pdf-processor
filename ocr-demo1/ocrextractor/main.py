import os
from pathlib import Path
import pandas as pd
from internal.extract_with_regions import ExtractorV1
import shutil

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


def get_csv_path_v2(image_name) -> Path:
    return get_create_csv_dir() / image_name


def write_if_not_exists(df: pd.DataFrame, image_name=None) -> None:
    csv_path = get_csv_path(image_name)
    if not csv_path.exists():
        df.to_csv(csv_path, index=False)


def write_if_not_exists_v2(df: pd.DataFrame, image_name) -> None:
    csv_path = get_csv_path_v2(image_name)
    if not csv_path.exists():
        print(f'Writing to {csv_path}')
        df.to_csv(csv_path, index=False)
    else:
        print(f'{csv_path} already exists')


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


def convert_samples_to_csv():
    failed = []
    for file in get_samples_dir().iterdir():
        if file.suffix == '.png':
            try:
                print(f'Converting {file.name}')
                extractor = ExtractorV1(str(file))
                df = extractor.extract_to_df()
                write_if_not_exists(df, file.name)
            except Exception as e:
                print(f'Failed to convert {file.name}: {e}')
                failed.append(file.name)
    print(f'Failed to convert {len(failed)} files: {failed}')
    return failed


def convert_images_to_csv(limit=10):
    failed = []
    i = 0
    for file in Path(Path(os.getcwd()).parent / 'images').iterdir():
        if file.suffix == '.png':
            try:
                print(f'Converting {file.name}')
                extractor = ExtractorV1(str(file))
                df = extractor.extract_to_df()
                name = file.name
                name = str.join('.', name.split('.')[:-1]) + '.csv'
                print(f'Writing to {name}')
                write_if_not_exists_v2(df, name)
                i += 1
                if i >= limit:
                    break
            except Exception as e:
                print(f'Failed to convert {file.name}: {e}')
                failed.append(file.name)
    print(f'Failed to convert {len(failed)} files')
    return failed


def convert_to_csv_if_not_exists(limit=10):
    failed = []
    i = 0
    for file in Path(Path(os.getcwd()).parent / 'images').iterdir():
        if file.suffix == '.png':
            try:
                name = file.name
                name = str.join('.', name.split('.')[:-1]) + '.csv'
                csv_path = get_create_csv_dir() / name
                if not csv_path.exists():
                    print(f'Converting {file.name}')
                    extractor = ExtractorV1(str(file))
                    df = extractor.extract_to_df()
                    print(f'Writing to {name}')
                    write_if_not_exists_v2(df, name)
                    i += 1
                    if i >= limit:
                        break
                else:
                    print(f'{name} already exists')
            except Exception as e:
                print(f'Failed to convert {file.name}: {e}')
                failed.append(file.name)
    print(f'Failed to convert {len(failed)} files')
    return failed


def write_failed_to_text(failed):
    # If exists, open and append what's not in the file
    # If not exists, create and write
    if len(failed) == 0:
        return
    if not os.path.exists('failed.txt'):
        with open('failed.txt', 'w') as f:
            for file in failed:
                f.write(file + '\n')
    else:
        with open('failed.txt', 'r') as f:
            existing = f.readlines()
        with open('failed.txt', 'w') as f:
            for file in failed:
                if file not in existing:
                    f.write(file + '\n')


def copy_images_from_disclosurecli():
    # get home dir
    home_dir = Path.home()
    # get disclosurecli dir
    disclosurecli_dir = home_dir / '.disclosurecli' / 'data' / 'images'
    dest_dir = Path(os.getcwd()).parent / 'images'
    # go into each dir in images and copy png files
    for d in disclosurecli_dir.iterdir():
        if d.is_dir():
            for file in d.iterdir():
                if file.suffix == '.png':
                    print(f'Copying {file.name}')
                    shutil.copy(file, dest_dir)


if __name__ == '__main__':
    extractor = ExtractorV1(str(get_image_path()))
    # Command 1 - copy images
    # copy_images_from_disclosurecli()

    # Command 2 - convert to csv
    # convert_images_to_csv()
    failed = convert_to_csv_if_not_exists()
    write_failed_to_text(failed)

    # text = extractor.extract_text()
    # print_text_lines(text)
    # df = extractor.extract_to_df()
    # example_print_confidences(df)
    # write_if_not_exists(df)
    # print('convert samples to csv')
    # _ = convert_samples_to_csv()
