from curses.ascii import isspace
from dataclasses import dataclass
from typing import List
from svgpathtools import svg2paths2, wsvg, Path
from svgpathtools import CubicBezier, Line, Arc


@dataclass
class SvgLetterMover:
    input_file_path: str
    x_delta: float
    y_delta: float

    def read_svg_letter(self):
        paths, attributes, svg_attributes = svg2paths2(self.input_file_path)
        return (paths, attributes, svg_attributes)

    def __calc_move_point(self, complex_pair: complex, x_delta: float, y_delta: float):
        x, y = complex_pair.real + x_delta, complex_pair.imag + y_delta
        return complex(x, y)

    def __move_cubic_bezier(self, cubic_bezier: CubicBezier):
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

    def __move_line(self, line: Line):
        moved_start = self.__calc_move_point(line.start, self.x_delta, self.y_delta)
        moved_end = self.__calc_move_point(line.end, self.x_delta, self.y_delta)
        return Line(
            start=moved_start,
            end=moved_end
        )

    def __move_arc(self, arc: Arc):
        moved_start = self.__calc_move_point(arc.start, self.x_delta, self.y_delta)
        moved_end = self.__calc_move_point(arc.end, self.x_delta, self.y_delta)
        return Arc(
            start=moved_start,
            radius=arc.radius,
            rotation=arc.rotation,
            large_arc=arc.large_arc,
            sweep=arc.sweep,
            end=moved_end
        )

    def __move_path_elm(self, elm):
        if type(elm) == CubicBezier:
            return self.__move_cubic_bezier(elm)
        elif type(elm) == Line:
            return self.__move_line(elm)
        elif type(elm) == Arc:
            return self.__move_arc(elm)

    def __combine_paths(self, paths: List[Path]) -> Path:
        combine_paths = []
        for path in paths:
            for elm in path:
                combine_paths.append(elm)
        return Path(*combine_paths)

    def move_paths(self, paths: List[Path]) -> List:
        combined_path = self.__combine_paths(paths)
        return self.__move_path(combined_path)

    def __move_path(self, path: Path) -> Path:
        moved_path = [self.__move_path_elm(elm) for elm in path]
        return Path(*moved_path)


@dataclass
class Position:
    letter_height: int
    letter_width: int
    left_spacing: float
    top_spacing: float


def main():
    def __init_position(index: int, letter_length: int, spacing: float) -> float:
        return index * (letter_length * ( 1 + spacing))

    def __move_charactor(input_file_path, x_delta, y_delta):
        mover = SvgLetterMover(input_file_path, x_delta, y_delta)
        svg_letter = mover.read_svg_letter()

        paths = svg_letter[0]
        svg_attributes = svg_letter[2]
        moved_paths = mover.move_paths(paths)

        return (moved_paths, svg_attributes)

    def move_whole_charactor(position:Position):
        moved_paths = []
        svg_attributes = {}
        for left_index, char in enumerate(passage):
            if char.isspace():
                continue
            else:
                input_file_path = f'./data/input/svg/{char}.svg'
                left = __init_position(left_index, position.letter_width, position.left_spacing)
                top_index = 0
                top = __init_position(top_index, position.letter_height, position.top_spacing)
                tmp_moved_paths, svg_attributes = __move_charactor(input_file_path, left, top)
                moved_paths.extend(tmp_moved_paths)
        return (moved_paths, svg_attributes)

    def read_passage_text():
        return ' こんにちは'

    passage = read_passage_text()
    output_file_title = 'sample_short_moved'
    output_file_path = f'./data/output/svg/{output_file_title}.svg'
    position = Position(13, 13, 0.25, 0.5)
    moved_paths, svg_attributes = move_whole_charactor(position)
    wsvg(moved_paths, svg_attributes=svg_attributes, filename=output_file_path)


if __name__ == '__main__':
    main()
