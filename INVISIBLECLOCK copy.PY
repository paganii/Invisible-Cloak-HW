import cv2, os, time
import numpy as np

rawvideo = cv2.VideoCapture(0)
time.sleep = 1
count = 0
background = 0

for i in range(60):
    ret, frame = rawvideo.read() #start capturing frames
    print(ret, frame)
    if not ret:
        continue #if not able to capture current frame, move to next
frame = np.flip(frame, axis=1)
while rawvideo.isOpened():
    print()
    ret, img = rawvideo.read()
    print(ret)
    if not ret:
        break
    img = np.flip(img, axis=1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowerred = np.array([15, 80, 80])
    upperred = np.array([25, 255, 255])
    mask1 = cv2.inRange(hsv, lowerred, upperred)
    lowerred = np.array([25, 100, 100])
    upperred = np.array([35, 255, 255])
    mask2 = cv2.inRange(hsv, lowerred, upperred)
    # loweryellow = np.array([20, 100, 100])
    #upperyellow = np.array([35, 255, 255])
    #maskyellow = cv2.inRange(hsv, loweryellow, upperyellow)
    mask1 = mask1 + mask2
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3), np.uint8), iterations = 2)
    mask1 = cv2.dilate(mask1, np.ones((3,3), np.uint8), iterations = 2)
    mask2 = cv2.bitwise_not(mask1)
    res1 = cv2.bitwise_and(frame, frame, mask = mask1)
    res2 = cv2.bitwise_and(img, img, mask2)
    finaloutput = cv2.addWeighted(res1, 1, res2, 1, 0) #transparency no added
    cv2.imshow("Invisible Area", finaloutput)
    k = cv2.waitKey(10)
    if k == 27:
        break