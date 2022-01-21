import svgwrite
from dataclasses import dataclass
from typing import Any

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
    path: Any
    output_file_name: str

    def write(self):
        dwg = svgwrite.Drawing(self.output_file_name)
        dwg.add(dwg.polygon(points=self.path))
        dwg.save()


if __name__ == '__main__':
    sample_path = [[10.0, 0.0], [0.0, 0.0], [0.0, 10.0], [10.0, 10.0]]
    sample_file_name = 'handle_sample_img/sample_output_file.svg'
    svg = SvgWriter(sample_path, sample_file_name)
    svg.write()
