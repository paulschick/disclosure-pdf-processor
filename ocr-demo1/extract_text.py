import cv2
from PIL import Image
import pytesseract

tessdata_dir_config = r'--tessdata-dir /usr/share/tesseract-ocr/5/tessdata_best-4.1.0'


def extract_text(image):
    text = pytesseract.image_to_string(image=image, lang='eng', config=tessdata_dir_config)
    return text


if __name__ == '__main__':
    # img = cv2.imread("samples/2015-2-Charles-Dent.png", cv2.IMREAD_COLOR)
    img1 = Image.open("samples/2015-1-Charles-Dent-sideways.png")
    # img2 = Image.open("samples/2015-2-Charles-Dent.png")
    img2 = Image.open("samples/2024-1-Lloyd-Doggett-20024268.png")
    # txt = extract_text(img)
    txt2 = extract_text(img2)
    # print(txt)
    print(txt2)
    print(pytesseract.image_to_osd(img2, lang='eng', config=tessdata_dir_config))
    print('--')
    print(pytesseract.image_to_osd(img2, lang='eng'))
    print('-- sideways img --')
    print(extract_text(img1))
    print('best')
    print(pytesseract.image_to_osd(img1, lang='eng', config=tessdata_dir_config))
    print('--')
    print('fast')
    print(pytesseract.image_to_osd(img1, lang='eng'))
    print('--scanned img --')
    img3 = Image.open("samples/2015-2-Charles-Dent.png")
    print(extract_text(img3))
