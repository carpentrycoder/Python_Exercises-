import cv2
import mediapipe as mp
import numpy as np
import time
from playsound import playsound
import threading
from collections import deque

# Alarm function in a separate thread
def play_alarm():
    playsound("alarm.wav")

# Initialize MediaPipe FaceMesh with refined landmarks for more accurate eye detection
mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
mp_draw = mp.solutions.drawing_utils

# Eye landmark indices
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

# EAR calculation
def eye_aspect_ratio(landmarks, eye_indices, w, h):
    p1 = np.array([landmarks[eye_indices[1]].x * w, landmarks[eye_indices[1]].y * h])
    p2 = np.array([landmarks[eye_indices[5]].x * w, landmarks[eye_indices[5]].y * h])
    p3 = np.array([landmarks[eye_indices[2]].x * w, landmarks[eye_indices[2]].y * h])
    p4 = np.array([landmarks[eye_indices[4]].x * w, landmarks[eye_indices[4]].y * h])
    p5 = np.array([landmarks[eye_indices[0]].x * w, landmarks[eye_indices[0]].y * h])
    p6 = np.array([landmarks[eye_indices[3]].x * w, landmarks[eye_indices[3]].y * h])

    vertical1 = np.linalg.norm(p2 - p4)
    vertical2 = np.linalg.norm(p3 - p5)
    horizontal = np.linalg.norm(p1 - p6)
    ear = (vertical1 + vertical2) / (2.0 * horizontal)
    return ear

# Parameters
EAR_THRESHOLD = 0.26  # More realistic default threshold
SLEEP_FRAMES = 40
MOVING_AVG_WINDOW = 5

ear_history = deque(maxlen=MOVING_AVG_WINDOW)
sleep_counter = 0
alarm_on = False

# Video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            left_ear = eye_aspect_ratio(face_landmarks.landmark, LEFT_EYE, w, h)
            right_ear = eye_aspect_ratio(face_landmarks.landmark, RIGHT_EYE, w, h)
            avg_ear = (left_ear + right_ear) / 2
            ear_history.append(avg_ear)

            # Smooth EAR with moving average
            smoothed_ear = np.mean(ear_history)

            # Display EAR value
            cv2.putText(frame, f'Smoothed EAR: {smoothed_ear:.3f}', (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

            # Drowsiness logic
            if smoothed_ear < EAR_THRESHOLD:
                sleep_counter += 1
                if sleep_counter >= SLEEP_FRAMES and not alarm_on:
                    alarm_on = True
                    threading.Thread(target=play_alarm).start()
                if alarm_on:
                    cv2.putText(frame, "DROWSINESS ALERT!", (100, 150),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 4)
            else:
                sleep_counter = 0
                alarm_on = False

            # Draw eye mesh (optional - light blue lines)
            mp_draw.draw_landmarks(
                frame,
                face_landmarks,
                mp_face.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_draw.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=0)
            )

    cv2.imshow("Drowsiness Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
