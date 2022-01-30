import cv2
import numpy as np


import svgwrite


def generate_svg(contours, output_file_name):
    def contour_points(contour):
        return [point[0].tolist() for point in contour]

    dwg = svgwrite.Drawing(output_file_name)
    for contour in contours:
        path = contour_points(contour)
        dwg.add(dwg.polygon(points=path))
    dwg.save()


# Read Image
img = cv2.imread('cat.png')
# img = cv2.resize(img, (750, 1000))

# Find the gray image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Gray
gray = cv2.blur(gray, (2, 2))
cv2.imwrite('for_smooth_edge_gray.png', gray)

# Find the canny image
canny = cv2.Canny(gray, 30, 150)  # Canny

# Find contours
contours, _ = cv2.findContours(canny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on canny (this connects the contours)
cv2.drawContours(canny, contours, -1, 255, 6)
cv2.imwrite('for_smooth_edge_canny.png', canny)


# Get mask for floodfill
h, w = canny.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)

# Floodfill from point (0, 0)
cv2.floodFill(canny, mask, (0, 0), 123)
cv2.imwrite('for_smooth_edge_flood.png', canny)

# Exclude everying but the floodfill region
canny = cv2.inRange(canny, 122, 124)
cv2.imwrite('for_smooth_edge_floodonly.png', canny)

generate_svg(contours, 'for_smooth_edge_floodonly.svg')


# cv2.putText(img,"Hello World!!!", (x,y), cv2.CV_FONT_HERSHEY_SIMPLEX, 2, 255)

# https://qapicks.com/question/70222415-ebaab14f7b48
# https://segmentfault.com/a/1190000015665320