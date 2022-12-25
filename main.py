import HandTrackingModule as htm
import cv2 as cv
import numpy as np
import autopy
import mouse

# setting cam size
wCam , hCam = 640,480
# get screen size as the size is different for each lcd
wScr , hScr =autopy.screen.size()

# framerate is set to 150 can be change to desired value it is used to provide smooth motion of cursor without jumpping one point to another
frameR = 150
smootheing = 5
# nouse cursor points
plocX , plocY = 0, 0
clocX , clocY = 0,0

# getting camera
cap = cv.VideoCapture(0)
# setting width and height of camera
cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.HandDetector(maxHand=1)

while True:
    sucess, img = cap.read()
    img = cv.flip(img, 1)
    # img = Mouse(img)
    # finding hands
    detector.findhands(img)
    lmlist, bbox = detector.findPosition(img)

    cv.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

    if len(lmlist) != 0:
        Xindex, Yindex = lmlist[8][1], lmlist[8][2]
        fingers = detector.fingersUp()

        # apply condition when only one finger index is up
        if fingers[1] == 1 and fingers[2] == 0  and fingers[2] == 0 and fingers[3] == 0:
            # setting mouse point with respect to screen size
            xMOUSE = np.interp(Xindex, (frameR, wCam - frameR), (0, wScr))
            yMOUSE = np.interp(Yindex, (frameR, hCam - frameR), (0, hScr))
            # setting mouse points
            clocX = plocX + (xMOUSE - plocX) / smootheing
            clocY = plocY + (yMOUSE - plocY) / smootheing
            # move mouse cursor
            autopy.mouse.move(clocX, clocY)
            cv.circle(img, (Xindex, Yindex), 15, (20, 180, 90), cv.FILLED)
            plocY, plocX = clocY, clocX

        # when index finger and middle fingers are together
        if fingers[1] == 1 and fingers[2] == 1:
            length, bbox = detector.findDistance(8, 12, img)
            if length < 40:
                autopy.mouse.click()

        if fingers[4] == 1:
            length, bbox = detector.findDistance(4,8, img)

            if length <= 70:
                mouse.right_click()
    cv.imshow("Mouse | press ESC key to exit ", img)
    key = cv.waitKey(1)
    if key == 27:
        print('esc is pressed closing all windows')
        cv.destroyAllWindows()
        break
cap.release()
