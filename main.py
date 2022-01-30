import numpy as np
import cv2
import click
import string
from japanese_font import JapaneseFont
from character_recognizer import CommonRecognizer, SkeletonImage
from svg_writer import SvgWriter
from logs.common_logger import Log


@click.command()
@click.option('--x', help='The upper left coordinate of the input text as x.')
@click.option('--y', help='The upper left coordinate of the input text as y.')
@click.option('--font_path', help='Path to the font file')
@click.option('--size', help='Font size. The size of the "1" varies depending on the font.')
@click.option('--input_txt_title')
@click.option('--output_svg_title')
def main(x, y, font_path, size, input_txt_title, output_svg_title) -> None:
    def open_template():
        try:
            with open(f'data/input/txt/{input_txt_title}.txt', 'r', encoding='utf-8') as f:
                return string.Template(f.read())
        except FileNotFoundError as e:
            raise FileNotFoundError(
                f'{e}. Maybe there is no template.')

    def generate_text_img(text: str):
        array_length_i = 600
        array_length_j = 6000
        img = np.full((array_length_i, array_length_j, 3), (160, 160, 160), dtype=np.uint8)
        """
        sample img data: [[...]1, ..., [...]i]
        [...]1: [x1(1), ..., x1(j)]
        [...]i: [xi(j=1), ..., xi(j)]
        """
        _x, _y = int(x), int(y)
        colorBGR = (255, 0, 0)
        font_image = JapaneseFont(img=img, text=text, org=(_x, _y), fontFace=font_path, fontScale=int(size), color=colorBGR).cv2_putText()
        return font_image

    def generate_text_contours():
        template = open_template()
        message = template.substitute()
        txt_img = generate_text_img(message)
        gray_img = CommonRecognizer().generate_gray_img(txt_img)
        skeleton_img = SkeletonImage(txt_img, gray_img).skeletonize_img()
        contours = CommonRecognizer().generate_contours(skeleton_img)
        print(len(contours))
        return contours

    def generate_pic_contours():
        pic_img = cv2.imread('./data/input/img/cat.png')
        gray_img = CommonRecognizer().generate_gray_img(pic_img)
        contours = CommonRecognizer().generate_contours(gray_img)
        return contours

    contours = []
    contours.extend(generate_text_contours())
    # contours.extend(generate_pic_contours())
    SvgWriter(contours, f'./data/output/{output_svg_title}.svg').write_all()

    log = Log()
    log.app_info(contours)

if __name__ == "__main__":
    main()
