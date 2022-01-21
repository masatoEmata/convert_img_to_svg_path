import base64
import svgwrite


def main():
    with open(input_file, "rb") as f:
        img = base64.b64encode(f.read())

    dwg = svgwrite.Drawing(output_file)
    dwg.add(dwg.image('data:image/png;base64,' + img.decode("ascii"),
            size=(200, 200))
            )
    dwg.save()


if __name__ == '__main__':
    input_file = 'sample_picture.jpg'
    output_file = 'sample_picture.svg'

    main()
