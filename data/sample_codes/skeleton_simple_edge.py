import svgwrite
import cv2

def write(output_file_name, path):
    dwg = svgwrite.Drawing(output_file_name)
    dwg.add(dwg.polygon(points=path))
    dwg.save()


def detect_edge(input_file_name):
    image = cv2.imread(input_file_name)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged_image = cv2.Canny(gray_image, 1, 255)
    cv2.imshow("edged image", edged_image)
    cv2.waitKey()
    contours, hierarchy = cv2.findContours(
        edged_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    def contour_points(contour):
        return [point[0].tolist() for point in contour]
    writeTargetPoints = []
    for contour in contours:
        writeTargetPoints.extend(contour_points(contour))
    return writeTargetPoints


sample_path = detect_edge("cat.png")
# # print(sample_path)
sample_file_name = 'output_skeleton_simple_edge.svg'
write(sample_file_name, sample_path)

# import svgwrite
# import cv2
# input_file_name = "sample.jpg"
# sample_file_name = 'sample_output_file_edged.svg'
# image = cv2.imread(input_file_name)
# gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# blur_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
# _, binary_image = cv2.threshold(blur_image, 130, 255, cv2.THRESH_BINARY)
# cv2.imshow("edged image", binary_image)
# cv2.waitKey()

# edged_image = cv2.Canny(gray_image, 60, 255)
# cv2.imshow("edged image", edged_image)
# cv2.waitKey()
# contours, hierarchy = cv2.findContours(
#     edged_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# def contour_points(contour):
#     return [point[0].tolist() for point in contour]
# writeTargetPoints = []
# for contour in contours:
#     writeTargetPoints.extend(contour_points(contour))
# write(sample_file_name, writeTargetPoints)
