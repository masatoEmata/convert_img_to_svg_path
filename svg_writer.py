import svgwrite
from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass
class SvgWriter:
    """ Write svg file with path.
    Args:
        path (List, optional): Nest array of characters' path.
        output_file_name (str): The name of output file.
    Returns:
        None
    Other:
        Make svg file.
    """
    contours: List[List[float]]
    output_file_name: str

    def contour_points(self, contour: np.ndarray):
        return [point[0].tolist() for point in contour]

    def write(self, dwg: svgwrite.drawing.Drawing, contour: np.ndarray):
        path = self.contour_points(contour)
        dwg.add(dwg.polygon(points=path))

    def write_all(self):
        dwg = svgwrite.Drawing(self.output_file_name)
        for contour in self.contours:
            self.write(dwg, contour)
        dwg.save()


if __name__ == '__main__':
    sample_path = [[10.0, 0.0], [0.0, 0.0], [0.0, 10.0], [10.0, 10.0]]
    sample_file_name = 'handle_sample_img/sample_output_file.svg'
    svg = SvgWriter(sample_path, sample_file_name)
    svg.write()
