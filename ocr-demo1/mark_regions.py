import cv2
import pytesseract
import matplotlib.pyplot as plt

tessdata_dir_config = r'--tessdata-dir /usr/share/tesseract-ocr/5/tessdata_best-4.1.0'


def mark_region(img_path: str):
    """
    From here
    https://towardsdatascience.com/extracting-text-from-scanned-pdf-using-pytesseract-open-cv-cd670ee38052
    """
    img = cv2.imread(img_path)
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


if __name__ == '__main__':
    fp1 = 'samples/2024-1-Lloyd-Doggett-20024268.png'
    fp2 = 'samples/2015-2-Charles-Dent.png'
    i, coor = mark_region(fp1)
    # plt.figure(figsize=(12, 10))

    # Gets the best text extraction with threshold
    ret, thresh1 = cv2.threshold(i, 120, 255, cv2.THRESH_BINARY)
    # plt.imshow(thresh1)
    # plt.show()
    text = pytesseract.image_to_string(thresh1, config=tessdata_dir_config)
    # print(text)
    text_lines = text.split('\n')
    i = 0
    for line in text_lines:
        if line:
            print(f'{i}: {line}')
            i += 1
