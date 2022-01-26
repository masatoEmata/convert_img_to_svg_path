from PIL import Image, ImageDraw, ImageFont
import numpy as np
from dataclasses import dataclass

@dataclass
class JapaneseFont:
    img: np.ndarray
    text: str
    org: tuple
    fontFace: str
    fontScale: int
    color: tuple

    def cv2_putText(self):
        x, y = self.org
        imgPIL = Image.fromarray(self.img)
        draw = ImageDraw.Draw(imgPIL)
        fontPIL = ImageFont.truetype(font=self.fontFace, size=self.fontScale)
        w, h = draw.textsize(self.text, font=fontPIL)
        draw.text(xy=(x, y-h), text=self.text, fill=self.color, font=fontPIL)
        return np.array(imgPIL, dtype=np.uint8)
    
    # https://qiita.com/mo256man/items/b6e17b5a66d1ea13b5e3