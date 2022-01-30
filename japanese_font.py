from PIL import Image, ImageDraw, ImageFont
import numpy as np
from dataclasses import dataclass

@dataclass
class JapaneseFont:
    img: np.ndarray  # 第一引数の値が小さすぎると文字描画領域が小さくなり文字が出力されなくなる。文字が収まる最小領域を確保できれば良い。
    text: str  # 日本語OK。\nを使っての改行もOK。
    org: tuple  # テキストの左上の座標を(x,y)で指定する。
    fontFace: str
    fontScale: int  # 「1」の大きさはフォントにより異なる。
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