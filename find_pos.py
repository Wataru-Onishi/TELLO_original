# coding: utf-8

import cv2
import numpy as np
import tello
import time
from kbhit import *     


LOW_COLOR = np.array([0, 220, 30])
HIGH_COLOR = np.array([15, 255, 255])

# 抽出する塊のしきい値
AREA_RATIO_THRESHOLD = 0.005

def find_specific_color(frame_BGR,AREA_RATIO_THRESHOLD,LOW_COLOR,HIGH_COLOR):
    """
    指定した範囲の色の物体の座標を取得する関数
    frame: 画像
    AREA_RATIO_THRESHOLD: area_ratio未満の塊は無視する
    LOW_COLOR: 抽出する色の下限(h,s,v)
    HIGH_COLOR: 抽出する色の上限(h,s,v)
    """
    # 高さ，幅，チャンネル数
    h,w,c = frame_BGR.shape

    # hsv色空間に変換
    frame_hsv = cv2.cvtColor(frame_BGR,cv2.COLOR_BGR2HSV)
    
    # 色を抽出する
    ex_img = cv2.inRange(frame_hsv,LOW_COLOR,HIGH_COLOR)

    # 輪郭抽出
    _,contours,hierarchy = cv2.findContours(ex_img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    # 面積を計算
    areas = np.array(list(map(cv2.contourArea,contours)))

    if len(areas) == 0 or np.max(areas) / (h*w) < AREA_RATIO_THRESHOLD:
        # 見つからなかったらNoneを返す
        print("the area is too small")
        x = -1
        y = -1
        return (x,y) 
    else:
        # 面積が最大の塊の重心を計算し返す
        max_idx = np.argmax(areas)
        max_area = areas[max_idx]
        result = cv2.moments(contours[max_idx])
        x = int(result["m10"]/result["m00"])
        y = int(result["m01"]/result["m00"])
        return (x,y)



def main():
    drone = tello.Tello('',8889,command_timeout=0.01)
    atexit.register(set_normal_term)
    set_curses_term()
    
    while True:
        if kbhit():
            key = getch()
            if key == 't':
                drone.takeoff()
            if key == 'l':
                drone.land()
            if key == 's':
                try :
                    while True :
        
                        frame_BGR = drone.read()
                        if frame_BGR is None or frame_BGR.size == 0:
                            continue
                        frame_BGR = cv2.resize( frame_BGR, (480, 360) )
                        frame_RGB = cv2.cvtColor(frame_BGR,cv2.COLOR_BGR2RGB)
                        pos = find_specific_color(
                            frame_RGB,
                            AREA_RATIO_THRESHOLD,
                            LOW_COLOR,
                            HIGH_COLOR
                        )
                        x = pos[0]
                        y = pos[1]

                        if pos is not None:
                            # 抽出した座標に丸を描く
                            cv2.circle(frame_RGB,pos,10,(0,0,255),-1)

                        # 画面に表示する
                        cv2.imshow('frame',frame_RGB)

                        if x < 230 :
                            drone.rotate_ccw(20)
                            time.sleep(0.5)
                        if x > 250 :
                            drone.rotate_cw(20)
                            time.sleep(0.5)
                        if x < 0 :
                            time.sleep(0.5)
                            continue

                        k = cv2.waitKey(1)
                        if k == ord('q'):
                            break

                except KeyboardInterrupt:
                        break

        k = cv2.waitKey(1)
        if k == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
