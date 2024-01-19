import os
from pathlib import Path
from internal.extract_with_regions import ExtractorV1

if __name__ == '__main__':
    image_name = '2024-1-Lloyd-Doggett-20024268.png'
    image_path = str(Path(os.getcwd()).parent / 'samples' / image_name)
    extractor = ExtractorV1(image_path)
    print(extractor.extract_text())
