import cv2
import matplotlib.pyplot as plt
import HandTrackingModule as htm
import numpy as np

detector=htm.handDetector()
draw_clr=(0,0,255)
img_canvas=np.zeros((720,1280,3),np.uint8) #Creating image canvas(height,width,channel-rgb)

cap=cv2.VideoCapture(0)
while (True):
    success,frame=cap.read()
    frame=cv2.resize(frame,(1280,720))
    frame=cv2.flip(frame,1)
#Draw Rectangles
    rect_imgx=cv2.rectangle(frame,pt1=(10,1),pt2=(250,100),color=(0,0,255),thickness=-1)
    rect_imgx=cv2.rectangle(frame,pt1=(260,1),pt2=(500,100),color=(0,255,0),thickness=-1)
    rect_imgx=cv2.rectangle(frame,pt1=(510,1),pt2=(750,100),color=(255,0,0),thickness=-1)
    rect_imgx=cv2.rectangle(frame,pt1=(760,1),pt2=(1000,100),color=(0,255,255),thickness=-1)
    rect_imgx=cv2.rectangle(frame,pt1=(1010,1),pt2=(1270,100),color=(255,255,255),thickness=-1)
    txt_img=cv2.putText(
                frame,
                text='Eraser',
                org=(1070,60),
                fontFace=cv2.FONT_HERSHEY_COMPLEX,
                fontScale=1,
                color=(0,0,0),
                thickness=2
                )

#Detect Hands
    frame=detector.findHands(frame)
#Finding Position by returning landmark list(lm list)
    lmList=detector.findPosition(frame)

    if(len(lmList)!=0):
        x1,y1=lmList[8][1],lmList[8][2] #Index finger tip coordinates
        #print(x1,y1)
        x2,y2=lmList[12][1],lmList[12][2] #Middle finger tip coordinates
        #print(x2,y2)

    #Detect if fingers are up
        fingers=detector.fingersUp()
        #print(fingers)

    #Check whether two fingers are up===>Selection Mode
        if fingers[1] and fingers[2]:
            #print('Selection Mode')
            xp,yp=0,0 #x_previous,y_previous(to activate drawing mode)
            if y1 < 100:
                if 10 <= x1 <= 250:
                    print('red')
                    draw_clr=(0,0,255)
                elif 260 <= x1 <= 500:
                    print('green')
                    draw_clr=(0,255,0)
                elif 510 <= x1 <= 750:
                    print('blue')
                    draw_clr=(255,0,0)
                elif 760 <= x1 <= 1000:
                    print('yellow')
                    draw_clr=(0,255,255)
                elif 1010 <= x1 <= 1270:
                    print('eraser')
                    draw_clr=(0,0,0)
                

            cv2.rectangle(frame,(x1,y1),(x2,y2),color=draw_clr,thickness=-1)
 #Check if index finger is up ===> Drawing Mode
        if fingers[1] and not fingers[2]:
            #print('Drawing Mode')
            cv2.circle(frame,(x1,y1),15,color=draw_clr,thickness=-1)

            if xp==0 and yp==0:
                xp=x1
                yp=y1
            #Colors
            if draw_clr==(0,0,0):
                cv2.line(frame,(xp,yp),(x1,y1),color=draw_clr,thickness=50)
                cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_clr,thickness=50)
                
            else:
                cv2.line(frame,(xp,yp),(x1,y1),color=draw_clr,thickness=20)
                cv2.line(img_canvas,(xp,yp),(x1,y1),color=draw_clr,thickness=20)
            
            xp,yp=x1,y1

#To combine two windows(canvas and cam window)
    img_grey=cv2.cvtColor(img_canvas,cv2.COLOR_BGR2GRAY)
    _,img_inverse=cv2.threshold(img_grey,20,225,cv2.THRESH_BINARY_INV) #applying threshold
    img_inverse=cv2.cvtColor(img_inverse,cv2.COLOR_GRAY2BGR)

    frame=cv2.bitwise_and(frame,img_inverse)
    frame=cv2.bitwise_or(frame,img_canvas)
    
    frame=cv2.addWeighted(frame,1,img_canvas,0.5,0)



    cv2.imshow('video capture',frame)
    #cv2.imshow('video canvas capture',img_canvas) ===>remove this to combine windows
    if cv2.waitKey(1) & 0xFF==27:
        break
cap.release
cv2.destroyAllWindows()