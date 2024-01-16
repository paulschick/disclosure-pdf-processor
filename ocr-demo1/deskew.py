import cv2
import numpy as np


def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle > -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated


if __name__ == '__main__':
    img1 = cv2.imread("samples/2015-1-Charles-Dent-sideways.png", cv2.IMREAD_COLOR)
    img2 = deskew(img1)
    cv2.imshow("img1", img1)
    cv2.imshow("img2", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
