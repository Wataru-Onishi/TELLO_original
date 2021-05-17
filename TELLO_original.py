# coding: utf-8

import tello
import cv2
import time
import numpy as np

def main():
    drone = tello.Tello('',8889,command_timeout=0.01)
    
    while True:
        frame_BGR = drone.read()
        if frame_BGR is None or frame_BGR.size == 0:
            continue
        frame_BGR = cv2.resize( frame_BGR, (480, 360) )
        frame_RGB = cv2.cvtColor(frame_BGR,cv2.COLOR_BGR2RGB)
        cv2.imshow('Show image',frame_RGB)

        hsv = cv2.cvtColor(frame_BGR, cv2.COLOR_RGB2HSV)
        lower_orange = np.array([50,100,100])
        upper_orange = np.array([100,255,255])
        mask = cv2.inRange(hsv, lower_orange, upper_orange)
        res = cv2.bitwise_and(frame_RGB,frame_RGB, mask= mask)
        cv2.imshow('res',res)


        k = cv2.waitKey(1)
        if k == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()


