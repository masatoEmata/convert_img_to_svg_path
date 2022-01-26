import cv2
from dataclasses import dataclass
import numpy as np
from typing import Any

@dataclass
class CommonRecognizer:
    def generate_contours(img):
        ret, thresh = cv2.threshold(img, 27, 25, 0)
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours
        # https://stackoverflow.com/questions/43108751/convert-contour-paths-to-svg-paths

    def show_image_summary(img):
        print(
            f'[DEBUG] img type: {type(img)}, length(Lv1): {len(img)}, length(Lv2){len(img[0])}')
        cv2.imshow('show_image_summary', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def generate_gray_img(color_img):
        def generate_gray_scale_img():
            gray_scale_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
            _, gray_scale_img = cv2.threshold(
                gray_scale_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            cv2.imshow('grayscale', gray_scale_img)
            cv2.waitKey(0)
            return gray_scale_img

        def generate_inversive_img():
            gray_scale_img = generate_gray_scale_img()
            return cv2.bitwise_not(gray_scale_img)

        return generate_inversive_img()


@dataclass
class SkeletonImage:
    color_img: np.ndarray
    gray_img: Any

    def display_skeleton_image(self, cap, skeleton):

        def colorimg_with_skeleton():
            colorimg = self.color_img.copy()
            colorimg = colorimg // 2 + 127
            colorimg[skeleton == 255] = 0
            return colorimg

        def show_colorimg():
            cv2.imshow(cap + '_skeleton', skeleton)
            cv2.imshow(cap + '_color image', colorimg_with_skeleton())
            cv2.waitKey(0)

        show_colorimg()

    def skeletonize_img(self):
        IMG_TITLE_CAP = 'ZHANGSUEN'
        THINNING_TYPE = cv2.ximgproc.THINNING_ZHANGSUEN
        # IMG_TITLE_CAP = 'GUOHALL'
        # THINNING_TYPE = cv2.ximgproc.THINNING_GUOHALL
        skeleton = cv2.ximgproc.thinning(self.gray_img, thinningType=THINNING_TYPE)
        self.display_skeleton_image(IMG_TITLE_CAP, skeleton)
        return skeleton
        # https://emotionexplorer.blog.fc2.com/blog-entry-200.html



if __name__ == '__main__':
    cr = CommonRecognizer
    result = cr.trace()
    print(result)