import cv2 
import mediapipe as mp
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
 


cap=cv2.VideoCapture(0)
mpHands= mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
while True:
    success, img=cap.read()
    
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
   #print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        vol =  0
        for handLms in results.multi_hand_landmarks:
            lmList = []
            for id,lm in enumerate( handLms.landmark):
                #print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id,cx,cy)
                lmList.append([id,cx,cy])
            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
            #print(lmList)
            if lmList:
                #print(lmList[4])
                x1, x2 = lmList[4][1], lmList[4][2]
                y1, y2 = lmList[8][1], lmList[8][2]
                cv2.circle(img, (x1,x2), 10, (255,0,9), cv2.FILLED)
                cv2.circle(img, (y1,y2), 10, (255,0,9), cv2.FILLED)
                cv2.line(img,(x1,x2),(y1,y2),(23,45,123),3)
                length = math.hypot(y1-x1,y2-x2)
                #print(length)
                if length<50:
                  z1=(x1+y1)//2
                  z2=(x2+y2)//2
                  cv2.circle(img, (z1,z2), 10, (255,234,9), cv2.FILLED)

            volRange=volume.GetVolumeRange()
            minVol=volRange[0]
            maxVol=volRange[1]
            vol=np.interp(length , [50,300] , [minVol,maxVol])
            volBar=np.interp(length, [50,400],[400,150])
            volPer=np.interp(length,[50,400],[0,100])
            #print(int(vol))
            volume.SetMasterVolumeLevel(vol, None)  
            cv2.rectangle(img,(50,200),(65,400),(0,223,23),3)    
            cv2.rectangle(img,(50,int(volBar)),(75,400),(0,233,43),cv2.FILLED)
            cv2.putText(img,str(int(volPer)),(40,450),cv2.FONT_HERSHEY_COMPLEX_SMALL,2,(0,2,234),2)
            #volume.SetMasterVolumeLevel(0.0, None)    


    cv2.imshow("Image",img)
    cv2.waitKey(1)  
    #cv2.destroyAllWindows()


