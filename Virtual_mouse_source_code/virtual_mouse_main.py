import cv2 as cv
import mediapipe as mp
import numpy as np
import pyautogui as pg


cam = cv.VideoCapture(0)

mphands = mp.solutions.hands
hands = mphands.Hands()
mpDraw = mp.solutions.drawing_utils

ujungid = [4, 8, 12, 16, 20]

screenWidth, screenHeight = pg.size()

frameR = 100

clk = 0

while True:
    succes, img = cam.read()

    img = cv.flip(img, 1)

    h, w, c = img.shape

    cv.rectangle(img, (frameR, frameR), (w-frameR, h-frameR), (0, 255, 0), 2)

    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if (results.multi_hand_landmarks):
        lmlist = []
        for handLms in results.multi_hand_landmarks:
            for id, landmarks in enumerate(handLms.landmark):
                cx, cy = int(landmarks.x*w), int(landmarks.y*h)
                lmlist.append([id, cx, cy])

        fingers = []
        if lmlist[ujungid[0]][1] < lmlist[ujungid[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if lmlist[ujungid[id]][2] < lmlist[ujungid[id]-1][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        if fingers == [0,1,1,0,0]:

            X = np.interp(lmlist[12][1], (frameR, w-frameR), (0, screenWidth))
            Y = np.interp(lmlist[12][2], (frameR, h - frameR), (0, screenHeight))

            pg.moveTo(X, Y, duration=0.11)
        if fingers == [0,0,1,0,0] and clk == 0:
            pg.click()
            clk = 1
        if fingers == [0, 0, 1, 0, 0] and clk == 1:
            clk = 0
        # elif fingers == [0,1,1,1,0]:
        #     pg.scroll()


    cv.imshow("Camera", img)

    if cv.waitKey(20) & 0xFF==ord('s'):
        break
cv.destroyWindow()
