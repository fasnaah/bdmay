import cv2
import mediapipe as mp

capture=cv2.VideoCapture(0)
mp_hands=mp.solutions.hands
hands=mp_hands.Hands(min_detection_confidence=0.3)
mp_drawing=mp.solutions.drawing_utils

while True:
    success,frame=capture.read()
    
    results=hands.process(frame)

    if results.multi_hand_landmarks:
        for hand_no,hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=hand_landmarks,
                connections=mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow('video capture',frame)

    if cv2.waitKey(1) & 0xFF==27:
        break

capture.release()
cv2.destroyAllWindows()