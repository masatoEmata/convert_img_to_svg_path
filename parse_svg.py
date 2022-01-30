from dataclasses import dataclass
from typing import List
from svgpathtools import svg2paths2, wsvg, Path, CubicBezier

@dataclass
class svgLetterHandler:
    input_file_path: str
    x_delta: float
    y_delta: float

    def read_svg_letter(self):
        paths, attributes, svg_attributes = svg2paths2(self.input_file_path)
        return (paths, attributes, svg_attributes)

    def move_paths(self, paths):
        moved_paths = []
        for path in paths:
            moved_paths.append(self.__move_path(path))
        return moved_paths

    def __calc_move_point(self, complex_pair: complex, x_delta: float, y_delta: float):
        x, y = complex_pair.real + x_delta, complex_pair.imag + y_delta
        return complex(x, y)

    def __move_cubic_bezier(self, cubic_bezier):
        moved_start = self.__calc_move_point(cubic_bezier.start, self.x_delta, self.y_delta)
        moved_c1 = self.__calc_move_point(cubic_bezier.control1, self.x_delta, self.y_delta)
        moved_c2 = self.__calc_move_point(cubic_bezier.control2, self.x_delta, self.y_delta)
        moved_end = self.__calc_move_point(cubic_bezier.end, self.x_delta, self.y_delta)
        return CubicBezier(
            start=moved_start,
            control1=moved_c1,
            control2=moved_c2,
            end=moved_end
        )
    def __move_path(self, path: Path):
        cubic_beziers = [self.__move_cubic_bezier(cb) for cb in path]
        return Path(*cubic_beziers)

    def write_svg_attributes(self, paths: List, svg_attributes: dict, output_file_name: str):
        wsvg(paths, svg_attributes=svg_attributes, filename=output_file_name)


if __name__ == '__main__':
    input_file_path = './data/input/svg/letter1.svg'
    output_file_name = './data/output/sample_short_moved.svg'
    x_delta, y_delta = 100, 100

    handler = svgLetterHandler(input_file_path, x_delta, y_delta)
    svg_letter = handler.read_svg_letter()

    paths = svg_letter[0]
    svg_attributes = svg_letter[2]
    moved_paths = handler.move_paths(paths)
    handler.write_svg_attributes(moved_paths, svg_attributes, output_file_name)
