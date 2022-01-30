import cv2

### Standard
image =cv2.imread('sample.jpg')
# cv2.imshow('hello world',image)
# cv2.waitKey(500)
# print(image.shape)
# print('Height of image:',(image.shape[0],'pixels'))
# print('Width of image:',(image.shape[1],'pixels'))

### Gray
# gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('grayscale', gray_img)
# cv2.waitKey(500)
# print(gray_img.shape)


### HSV
# hsv_image=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
# cv2.imshow('HSV image',hsv_image)
# cv2.waitKey(500)
# cv2.imshow('Hue channel',hsv_image[:,:,0])
# cv2.waitKey(500)
# cv2.imshow('saturation channel',hsv_image[:,:,1])
# cv2.waitKey(500)
# cv2.imshow('value channel',hsv_image[:,:,2])
# cv2.waitKey(500)


### Drawing Images and Shapes
# import numpy as np
# black_square = np.zeros((512,512),np.uint8)
# print(black_square)
# # cv2.imshow("black rectangle(color)", black_square)
# # cv2.waitKey(500)
# THICKNESS = 1
# COLOR = (255,127,0)
# cv2.line(black_square, (0,0), (511,511), COLOR, THICKNESS)
# cv2.rectangle(black_square, (30,50), (100,150), COLOR, -1)
# cv2.circle(black_square, (100,100), (50), COLOR, -1)
# cv2.putText(black_square,"hello world", (75,290), cv2.FONT_ITALIC,2,(100,170,0),3)
# cv2.imshow("blue line",black_square)
# cv2.waitKey(500)

### contours
# import cv2
import numpy as np
# file_name = "sample.jpg"
file_name = "letter_emata.png"
image = cv2.imread(file_name)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

### contours - Canny
edged_image = cv2.Canny(gray_image, 30, 200)
# cv2.imshow("gray image", gray_image)
# cv2.imshow("edged image", edged_image)
cv2.waitKey(500)

contours, hierarchy=cv2.findContours(
    edged_image,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_NONE)
print('Numbers of contours found=' + str(len(contours)))
cv2.drawContours(image, contours, -1, (0,255,0), 1)
# cv2.imshow('contours', image)
cv2.waitKey()
cv2.destroyAllWindows()

writeTargetPoints = [point[0].tolist() for point in contours[0]]
print(writeTargetPoints)
# writeTargetPoints = []
# for point in contours[0]:

#     writeTargetPoints.append(point[0])
# print(writeTargetPoints)
# print(contours[0][0])
# print(type(contours[0][0].tolist()))

### contours - Approximating Contours and Finding their Convex hull
# ret, thresh=cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY_INV)
# contours, hierarchy=cv2.findContours(thresh.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
# for c in contours:
#     x,y,w,h=cv2.boundingRect(c)
#     cv2.rectangle(gray_image,(x,y),(x+w,y+h),(0,0,255),2)
#     cv2.imshow('Bounding rect',gray_image)
#     #calculate accuracy as a percent of contour perimeter
#     # accuracy=0.03*cv2.arcLength(c,True)
#     # approx=cv2.approxPolyDP(c,accuracy,True)
#     # cv2.drawContours(image,[approx],0,(0,255,0),2)
#     # cv2.imshow('Approx polyDP', image)
# cv2.waitKey(0)

### contours - Convex Hull
# ret, thresh=cv2.threshold(gray_image,176,255,0)
# contours, hierarchy=cv2.findContours(thresh.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
# n=len(contours)-1
# contours=sorted(contours,key=cv2.contourArea,reverse=False)[:n]
# for c in contours:
#     hull=cv2.convexHull(c)
#     cv2.drawContours(image,[hull],0,(0,255,0),2)
#     cv2.imshow('convex hull',image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()



### Detect Line

# # init cv2
# # import cv2
# import numpy as np
# image = cv2.imread("boxs.png")

# # Grayscale and canny edges extracted
# gray2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# edged_image2 = cv2.Canny(gray2, 100, 170, apertureSize=3)
# cv2.imshow("edged image", edged_image2)
# cv2.waitKey(1000)

# # Run Hough lines using rho accuracy of 1 pixel
# # theta accuracy of (np.pi / 180) which is 1 degree
# # line threshold is set to 240(number of points on line)
# lines = cv2.HoughLines(edged_image2, 1, np.pi/180, 240)
# # print(lines)
# # we iterate through each line and convert into the format
# # required by cv2.lines(i.e. requiring end points)

# for i in range(0, len(lines)):
#     for rho, theta in lines[i]:
#         a = np.cos(theta)
#         b = np.sin(theta)
#         x0 = a*rho
#         y0 = b*rho
#         x1 = int(x0+1000*(-b))
#         y1 = int(y0+1000*(a))
#         x2 = int(x0-1000*(-b))
#         y2 = int(y0-1000*(a))
#         cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# cv2.imshow('hough lines', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
