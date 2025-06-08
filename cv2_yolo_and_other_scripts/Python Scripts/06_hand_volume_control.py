import cv2
import mediapipe as mp
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Audio setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()  # (-65.25, 0.0)
min_vol = vol_range[0]
max_vol = vol_range[1]

# Webcam
cap = cv2.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    lm_list = []

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            for id, lm in enumerate(handLms.landmark):
                h, w, _ = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            # Thumb tip: 4, Index tip: 8
            if lm_list:
                x1, y1 = lm_list[4][1], lm_list[4][2]
                x2, y2 = lm_list[8][1], lm_list[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(frame, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(frame, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)
                cv2.circle(frame, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

                length = math.hypot(x2 - x1, y2 - y1)

                # Convert to volume range
                vol = np.interp(length, [20, 180], [min_vol, max_vol])
                volume.SetMasterVolumeLevel(vol, None)

                # Volume bar
                vol_bar = np.interp(length, [20, 180], [400, 150])
                vol_perc = np.interp(length, [20, 180], [0, 100])
                cv2.rectangle(frame, (50, 150), (85, 400), (255, 0, 0), 3)
                cv2.rectangle(frame, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, f'{int(vol_perc)} %', (40, 430),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Volume Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
