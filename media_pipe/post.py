import cv2
import mediapipe as mp

capture=cv2.VideoCapture(0)
mp_pose=mp.solutions.pose
pose=mp_pose.Pose()
mp_drawing=mp.solutions.drawing_utils

while True:
    success,frame=capture.read()
    
    results=pose.process(frame)

    if results.pose_landmarks:
      mp_drawing.draw_landmarks(frame,results.pose_landmarks,mp_pose.POSE_CONNECTIONS)


    cv2.imshow('video capture',frame)

    if cv2.waitKey(1) & 0xFF==27:
        break

capture.release()
cv2.destroyAllWindows()