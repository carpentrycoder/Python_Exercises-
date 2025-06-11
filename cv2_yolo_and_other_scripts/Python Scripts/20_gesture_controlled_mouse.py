import sys
print("Python Executable in Use:", sys.executable)

import pyautogui
print("PyAutoGUI Version:", pyautogui.__version__)

import cv2
import mediapipe as mp
import numpy as np
import math

# Screen size
screen_width, screen_height = pyautogui.size()

# MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

click_down = False  # state of click

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    h, w, _ = img.shape

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            if len(lm_list) >= 9:
                index_tip = lm_list[8]
                thumb_tip = lm_list[4]

                # Draw landmarks
                mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

                # Move mouse
                x = np.interp(index_tip[0], [0, w], [0, screen_width])
                y = np.interp(index_tip[1], [0, h], [0, screen_height])
                pyautogui.moveTo(x, y, duration=0.01)

                # Click gesture
                pinch_distance = distance(index_tip, thumb_tip)
                if pinch_distance < 40:
                    if not click_down:
                        pyautogui.click()
                        click_down = True
                        cv2.putText(img, "CLICK", (10, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                else:
                    click_down = False

    cv2.imshow("Gesture Mouse", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
