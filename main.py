import numpy as np
import cv2

from japanese_font import JapaneseFont
from character_recognizer import CommonRecognizer, SkeletonImage
from svg_writer import SvgWriter


def main():

    def generate_text_img(text: str):
        img = np.full((300, 300, 3), (100, 160, 160), dtype=np.uint8)
        x, y = 50, 150
        fontPIL = "C:\Windows\Fonts\Pigmo-00.otf"
        size = 50
        colorBGR = (255, 0, 0)
        font_image = JapaneseFont(img=img, text=text, org=(
            x, y), fontFace=fontPIL, fontScale=size, color=colorBGR).cv2_putText()
        return font_image

    def generate_text_contours():
        txt_img = generate_text_img('ねこ\n合同会社')
        gray_img = CommonRecognizer.generate_gray_img(txt_img)
        skeleton_img = SkeletonImage(txt_img, gray_img).skeletonize_img()
        contours = CommonRecognizer.generate_contours(skeleton_img)
        return contours

    def generate_pic_contours():
        pic_img = cv2.imread('./data/img/cat.png')
        gray_img = CommonRecognizer.generate_gray_img(pic_img)
        contours = CommonRecognizer.generate_contours(gray_img)
        return contours

    contours = []
    contours.extend(generate_text_contours())
    contours.extend(generate_pic_contours())

    SvgWriter(contours, './data/output/cat2.svg').write_all()


if __name__ == "__main__":
    main()
