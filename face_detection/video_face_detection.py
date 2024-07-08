import cv2

cap = cv2.VideoCapture(0)
face_cascade=cv2.CascadeClassifier('/home/fasna/Music/bdmay/face_detection/data/haarcascade_frontalface_default.xml')
eye_cascade=cv2.CascadeClassifier('/home/fasna/Music/bdmay/face_detection/data/haarcascade_eye.xml')

while True:
    success,frame = cap.read()

    
    faces=face_cascade.detectMultiScale(frame)
    eyes=eye_cascade.detectMultiScale(frame)
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),color=(0,255,0),thickness=3)
    for(x,y,w,h) in eyes:
        cv2.rectangle(frame,(x,y),(x+w,y+h),color=(200,200,0),thickness=3)



    cv2.imshow('video capture',frame)
    if cv2.waitKey(1) & 0XFF==27:
        break
cap.release()
cv2.destroyAllWindows()

