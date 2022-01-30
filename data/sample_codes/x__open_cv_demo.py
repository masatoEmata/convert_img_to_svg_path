import sys
import numpy as np
import cv2


def extruct_core_coordinates():
    # https://gist.github.com/TonyMooori/4cc29c94f7bdbade6ff6102fef45232e
    # 0 <= h <= 179 (色相)　OpenCVではmax=179なのでR:0(180),G:60,B:120となる
    # 0 <= s <= 255 (彩度)　黒や白の値が抽出されるときはこの閾値を大きくする
    # 0 <= v <= 255 (明度)　これが大きいと明るく，小さいと暗い
    # ここでは青色を抽出するので120±20を閾値とした
    LOW_COLOR = np.array([100, 75, 75])
    HIGH_COLOR = np.array([140, 255, 255])

    # 抽出する青色の塊のしきい値
    AREA_RATIO_THRESHOLD = 0.005

    def find_specific_color(frame,AREA_RATIO_THRESHOLD,LOW_COLOR,HIGH_COLOR):
        """
        指定した範囲の色の物体の座標を取得する関数
        frame: 画像
        AREA_RATIO_THRESHOLD: area_ratio未満の塊は無視する
        LOW_COLOR: 抽出する色の下限(h,s,v)
        HIGH_COLOR: 抽出する色の上限(h,s,v)
        """
        # 高さ，幅，チャンネル数
        h,w,c = frame.shape
        # print(f'[DEBUG] h,w,c: {h}, {w}, {c}')

        # hsv色空間に変換
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        # print(f'[DEBUG] hsv: {hsv}')
        # 色を抽出する
        ex_img = cv2.inRange(hsv,LOW_COLOR,HIGH_COLOR)

        # 輪郭抽出
        contours,hierarchy = cv2.findContours(ex_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        print(f'[DEBUG] contours,hierarchy: {contours}')
        
        # 面積を計算
        areas = np.array(list(map(cv2.contourArea,contours)))

        if len(areas) == 0 or np.max(areas) / (h*w) < AREA_RATIO_THRESHOLD:
            # 見つからなかったらNoneを返す
            print("the area is too small")
            return None
        else:
            # 面積が最大の塊の重心を計算し返す
            max_idx = np.argmax(areas)
            max_area = areas[max_idx]
            result = cv2.moments(contours[max_idx])
            x = int(result["m10"]/result["m00"])
            y = int(result["m01"]/result["m00"])
            return (x,y)

    def test():
        img = cv2.imread("letter_emata.png")

        # 位置を抽出
        pos = find_specific_color(
            img,
            AREA_RATIO_THRESHOLD,
            LOW_COLOR,
            HIGH_COLOR
        )

        if pos is not None:
            cv2.circle(img,pos,10,(0,0,255),-1)
        
        cv2.imwrite("result.jpg",img)

    def main():
        # webカメラを扱うオブジェクトを取得
        cap = cv2.VideoCapture(0)


        while True:
            ret,frame = cap.read()

            if ret is False:
                print("cannot read image")
                continue

            # 位置を抽出
            pos = find_specific_color(
                frame,
                AREA_RATIO_THRESHOLD,
                LOW_COLOR,
                HIGH_COLOR
            )

            if pos is not None:
                # 抽出した座標に丸を描く
                cv2.circle(frame,pos,10,(0,0,255),-1)
            
            # 画面に表示する
            cv2.imshow('frame',frame)

            # キーボード入力待ち
            key = cv2.waitKey(1) & 0xFF

            # qが押された場合は終了する
            if key == ord('q'):
                break

        cv2.destroyAllWindows()

    test()

def detect_charactors():
    #1---画像読込み
    im = cv2.imread('moji.jpg')
    #2---グレイスケールに変換して二値化
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    #3---輪郭抽出
    contours = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
    # print(contours)
    #4---抽出した数分処理
    for moji in contours:
        x, y, w, h = cv2.boundingRect(moji)
        if h < 20: continue
        red = (0, 0, 255)
        cv2.rectangle(im, (x, y), (x+w, y+h), red, 2)
    #5---保存
    cv2.imwrite('re-moji.png', im)

    # https://www.hobby-happymylife.com/%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0/python_opencv_ocr/


if __name__ == '__main__':
    extruct_core_coordinates()