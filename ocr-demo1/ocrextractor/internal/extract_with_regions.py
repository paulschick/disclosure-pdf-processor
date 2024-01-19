import cv2
import pandas as pd
import pytesseract


# TODO - add a config file for this


class ExtractorV1:
    tessdata_dir_config = r'--tessdata-dir /usr/share/tesseract-ocr/5/tessdata_best-4.1.0'
    """
    From here
    https://towardsdatascience.com/extracting-text-from-scanned-pdf-using-pytesseract-open-cv-cd670ee38052
    """

    def __init__(self, image_path: str):
        self.image_path = image_path

    def mark_regions(self):
        img = cv2.imread(self.image_path)
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

    def get_threshold(self):
        img, _ = self.mark_regions()
        ret, thresh = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
        return thresh

    def extract_text(self):
        thresh = self.get_threshold()
        text = pytesseract.image_to_string(thresh, config=ExtractorV1.tessdata_dir_config)
        return text

    def extract_to_df(self):
        thresh = self.get_threshold()
        data: pd.DataFrame = pytesseract.image_to_data(
            thresh,
            config=ExtractorV1.tessdata_dir_config,
            output_type=pytesseract.Output.DATAFRAME
        )
        return data[data['text'].notnull()]

    def dump_to_csv(self, output_path: str):
        df = self.extract_to_df()
        df.to_csv(output_path, index=False)
