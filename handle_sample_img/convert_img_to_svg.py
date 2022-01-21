import base64
import svgwrite
def convert_file_format(input_file_name: str, output_file_name: str):
    with open(input_file_name, "rb") as f:
        img = base64.b64encode(f.read())

    dwg = svgwrite.Drawing(output_file_name)
    dwg.add(dwg.image('data:image/png;base64,' + img.decode("ascii"),
            size=(200, 200))
            )
    dwg.save()


if __name__ == '__main__':
    input_file_name = 'sample_picture.jpg'
    output_file_name = 'sample_picture.svg'

    convert_file_format(input_file_name, output_file_name)
