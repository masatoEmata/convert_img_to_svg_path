from dataclasses import dataclass
from svgpathtools import svg2paths2, wsvg, Path, CubicBezier

@dataclass
class svgLetterHandler:
    input_file_path: str

    def read_svg_letter(self):
        paths, attributes, svg_attributes = svg2paths2(self.input_file_path)
        return (paths, attributes, svg_attributes)

    def move_paths(self, paths, x_delta: float, y_delta: float):
        moved_paths = []
        for path in paths:
            moved_paths.append(self.move_path(path, x_delta, y_delta))
        return moved_paths

    def calc_move_point(self, complex_pair, x_delta: float, y_delta: float):
        x, y = complex_pair.real + x_delta, complex_pair.imag + y_delta
        return complex(x, y)

    def move_path(self, path, x_delta: float, y_delta: float):
        cubic_beziers = []
        for cubic_bezier in path:
            moved_start = self.calc_move_point(cubic_bezier.start, x_delta, y_delta)
            moved_c1 = self.calc_move_point(cubic_bezier.control1, x_delta, y_delta)
            moved_c2 = self.calc_move_point(cubic_bezier.control2, x_delta, y_delta)
            moved_end = self.calc_move_point(cubic_bezier.end, x_delta, y_delta)
            cb = CubicBezier(
                start=moved_start,
                control1=moved_c1,
                control2=moved_c2,
                end=moved_end
            )
            cubic_beziers.append(cb)
        return Path(*cubic_beziers)

    def write_svg_attributes(self, paths, svg_attributes, output_file_name):
        wsvg(paths, svg_attributes=svg_attributes, filename=output_file_name)


if __name__ == '__main__':
    input_file_path = './data/input/svg/letter1.svg'
    output_file_name = './data/output/svg/sample_short_moved.svg'
    x_delta, y_delta = 100, 100

    handler = svgLetterHandler(input_file_path)
    svg_letter = handler.read_svg_letter()

    paths = svg_letter[0]
    print(f"変更前のパス: \n  {paths}")
    print(f"\n\n")
    svg_attributes = svg_letter[2]
    moved_paths = handler.move_paths(paths, x_delta, y_delta)
    print(f"変更後のパス: \n  {moved_paths}")
    handler.write_svg_attributes(moved_paths, svg_attributes, output_file_name)

