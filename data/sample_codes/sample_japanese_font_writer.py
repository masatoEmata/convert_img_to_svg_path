import numpy as np
import cv2

from japanese_font import JapaneseFont
from utils import Utils
from skeleton_image import SkeletonImage

def main():
    def generate_text_img(text):
        img = np.full((400, 800, 3), (160, 160, 160), dtype=np.uint8)
        x, y = 250, 200
        fontPIL = "C:\Windows\Fonts\Pigmo-00.otf"
        size = 50
        colorBGR = (255, 0, 0)
        font_image = JapaneseFont(img=img, text=text, org=(x, y), fontFace=fontPIL, fontScale=size, color=colorBGR).cv2_putText()
        return font_image

    def generate_text_contours():
        txt_img = generate_text_img('ねこ\n合同会社')
        gray_img = Utils.generate_gray_img(txt_img)
        skeleton_img = SkeletonImage(txt_img, gray_img).skeletonize_img()
        contours = Utils.generate_contours(skeleton_img)
        return contours

    def generate_pic_contours():
        pic_img = cv2.imread('sample_img_cat.png')
        gray_img = Utils.generate_gray_img(pic_img)
        contours = Utils.generate_contours(gray_img)
        return contours

    contours = []
    contours.extend(generate_text_contours())
    contours.extend(generate_pic_contours())

    Utils.generate_svg(contours, 'output_cat.svg')

if __name__ == "__main__":
    main()

