from curses.ascii import isspace
from dataclasses import dataclass
from typing import List, Tuple, Dict
from svgpathtools import svg2paths2, wsvg, Path
from svgpathtools import CubicBezier, Line, Arc


@dataclass
class SvgLetterReader:
    input_file_path: str
    def read_svg_letter(self):
        paths, attributes, svg_attributes = svg2paths2(self.input_file_path)
        return (paths, attributes, svg_attributes)


@dataclass
class SvgLetterMover:
    x_delta: float
    y_delta: float
    scaling: float

    def __calc_move_point(self, complex_pair: complex, x_delta: float, y_delta: float, scaling: float):
        x, y = scaling * (complex_pair.real + x_delta), scaling * (complex_pair.imag + y_delta)
        return complex(x, y)

    def __move_cubic_bezier(self, cubic_bezier: CubicBezier):
        moved_start = self.__calc_move_point(cubic_bezier.start, self.x_delta, self.y_delta, self.scaling)
        moved_c1 = self.__calc_move_point(cubic_bezier.control1, self.x_delta, self.y_delta, self.scaling)
        moved_c2 = self.__calc_move_point(cubic_bezier.control2, self.x_delta, self.y_delta, self.scaling)
        moved_end = self.__calc_move_point(cubic_bezier.end, self.x_delta, self.y_delta, self.scaling)
        return CubicBezier(
            start=moved_start,
            control1=moved_c1,
            control2=moved_c2,
            end=moved_end
        )

    def __move_line(self, line: Line):
        moved_start = self.__calc_move_point(line.start, self.x_delta, self.y_delta, self.scaling)
        moved_end = self.__calc_move_point(line.end, self.x_delta, self.y_delta, self.scaling)
        return Line(
            start=moved_start,
            end=moved_end
        )

    def __move_arc(self, arc: Arc):
        moved_start = self.__calc_move_point(arc.start, self.x_delta, self.y_delta, self.scaling)
        moved_end = self.__calc_move_point(arc.end, self.x_delta, self.y_delta, self.scaling)
        moved_radius = self.__calc_move_point(arc.radius, 0, 0, self.scaling)
        return Arc(
            start=moved_start,
            radius=moved_radius,
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

    def __move_path(self, path: Path) -> Path:
        moved_path = [self.__move_path_elm(elm) for elm in path]
        return Path(*moved_path)

    def move_paths(self, paths: List[Path]) -> List:
        combined_path = self.__combine_paths(paths)
        return self.__move_path(combined_path)


@dataclass
class SvgLetterWriter:
    moved_paths: List
    svg_attributes: Dict
    output_file_path: str

    def write(self):
        wsvg(self.moved_paths, svg_attributes=self.svg_attributes, filename=self.output_file_path)


@dataclass
class Position:
    letter_height: int
    letter_width: int
    left_spacing: float
    top_spacing: float
    scaling: float


def main():
    def __init_position(index: int, letter_length: int, spacing: float) -> float:
        return index * (letter_length * (1 + spacing))

    def __load_charctors(input_file_path) -> Tuple:
        reader = SvgLetterReader(input_file_path)
        svg_letter = reader.read_svg_letter()
        paths = svg_letter[0]
        svg_attributes = svg_letter[2]
        return (paths, svg_attributes)

    def __move_paths(x_delta: float, y_delta: float, scaling: float, paths: List[Path]) -> List:
        mover = SvgLetterMover(x_delta, y_delta, scaling)
        return mover.move_paths(paths)

    def __move_charactor(input_file_path: str, x_delta: float, y_delta: float, scaling: float) -> Tuple:
        paths, svg_attributes = __load_charctors(input_file_path)
        moved_paths = __move_paths(x_delta, y_delta, scaling, paths)
        return (moved_paths, svg_attributes)

    def move_whole_charactor(passage: str, position: Position) -> Tuple:
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
                tmp_moved_paths, svg_attributes = __move_charactor(input_file_path, left, top, position.scaling)
                moved_paths.extend(tmp_moved_paths)
        return (moved_paths, svg_attributes)

    def read_passage_text():
        return ' こんにちは'

    passage = read_passage_text()
    output_file_title = 'sample_character_konnichiwa_x2'
    output_file_path = f'./data/output/svg/{output_file_title}.svg'
    position = Position(13, 13, 0.25, 0.5, 2)
    moved_paths, svg_attributes = move_whole_charactor(passage, position)
    SvgLetterWriter(moved_paths, svg_attributes, output_file_path).write()


if __name__ == '__main__':
    main()
