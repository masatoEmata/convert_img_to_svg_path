
import cv2
import svgwrite



def generate_gray_img(colorimg):
    # グレースケール変換
    gray = cv2.cvtColor(colorimg, cv2.COLOR_BGR2GRAY)
    _, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow('grayscale', gray)
    cv2.waitKey(0)

    # 二値画像反転
    image = cv2.bitwise_not(gray)
    return image

def display_result_image(cap, color_image, skeleton):
    colorimg = color_image.copy()

    # カラー画像に細線化を合成
    colorimg = colorimg // 2 + 127
    colorimg[skeleton == 255] = 0

    cv2.imshow(cap + '_skeleton', skeleton)
    cv2.imshow(cap + '_color image', colorimg)
    cv2.waitKey(0)

def skeletonize_img(colorimg, gray_img):
    IMG_TITLE_CAP = 'ZHANGSUEN'
    THINNING_TYPE = cv2.ximgproc.THINNING_ZHANGSUEN
    # IMG_TITLE_CAP = 'GUOHALL'
    # THINNING_TYPE = cv2.ximgproc.THINNING_GUOHALL
    print('gray_img: ',gray_img)
    skeleton = cv2.ximgproc.thinning(gray_img, thinningType=THINNING_TYPE)
    display_result_image(IMG_TITLE_CAP, colorimg, skeleton)
    return skeleton
    # https://emotionexplorer.blog.fc2.com/blog-entry-200.html


def generate_contours(img):
    ret, thresh = cv2.threshold(img, 27, 25, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_L1)
    # https://stackoverflow.com/questions/43108751/convert-contour-paths-to-svg-paths
    return contours

def generate_svg(contours, output_file_name):
    def write(path):
        dwg = svgwrite.Drawing(output_file_name)
        dwg.add(dwg.polygon(points=path))
        dwg.save()

    def contour_points(contour):
        return [point[0].tolist() for point in contour]

    def generate_path():
        writeTargetPoints = []
        for contour in contours:
            writeTargetPoints.extend(contour_points(contour))
        return writeTargetPoints
    write(generate_path())


def main():
    # img_path = 'sample.jpg'
    img_path = 'sample_img_emata.png'
    # 入力画像の取得
    colorimg = cv2.imread(img_path, cv2.IMREAD_COLOR)
    gray_img = generate_gray_img(colorimg)

    # 細線化(スケルトン化) THTHINNING_GUOHALLINNING_ZHANGSUEN
    skeleton_img = skeletonize_img(colorimg, gray_img)
    print(skeleton_img)
    contours = generate_contours(skeleton_img)

    generate_svg(contours, 'for_smooth_edge_floodonly.svg')


if __name__ == '__main__':
    main()


# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
# kernel = np.ones((7, 7), np.uint8)
# # Read the image as a grayscale image
# img = cv2.imread('center_line_before.jpeg', 0)
# #Threshold the image
# ret, img = cv2.threshold(img, 100, 255, 0)
# imgGray = cv2.GaussianBlur(img, (7, 7), 0)
# # Step 1: Create an empty skeleton
# size = np.size(img)
# skel = np.zeros(img.shape, np.uint8)

# # Get a Cross Shaped Kernel
# element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

# # Repeat steps 2-4
# while True:
#     #Step 2: Open the image
#     open = cv2.morphologyEx(img, cv2.MORPH_OPEN, element)
#     #Step 3: Substract open from the original image
#     temp = cv2.subtract(img, open)
#     #Step 4: Erode the original image and refine the skeleton
#     eroded = cv2.erode(img, element)
#     skel = cv2.bitwise_or(skel, temp)
#     img = eroded.copy()
#     # Step 5: If there are no white pixels left ie.. the image has been completely eroded, quit the loop
#     if cv2.countNonZero(img) == 0:
#         break
# # 
# print(img[0].tolist())
# cv2.imshow("center_line.svg", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# import svgwrite
# def generate_svg(contours, output_file_name):
#     def write(path):
#         dwg = svgwrite.Drawing(output_file_name)
#         dwg.add(dwg.polygon(points=path))
#         dwg.save()

#     # def contour_points(contour):
#     #     return [point[0].tolist() for point in contour]

#     # def generate_path():
#     #     writeTargetPoints = []
#     #     for contour in contours:
#     #         writeTargetPoints.extend(contour_points(contour))
#     #     return writeTargetPoints
#     # write(generate_path())

#     write(contours)

# generate_svg(img, "center_line.svg")


# # https://forum.opencv.org/t/detecting-the-center-of-a-curved-thick-line-in-python-using-opencv/1909