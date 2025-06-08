import cv2
import mediapipe as mp
from deepface import DeepFace
import numpy as np
import time
import csv

# Initialize MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
mp_drawing = mp.solutions.drawing_utils

# Emotion → Color mapping (with emojis)
emotion_colors = {
    'happy': (0, 255, 127),
    'sad': (0, 128, 255),
    'angry': (0, 0, 255),
    'surprise': (255, 255, 0),
    'neutral': (150, 150, 150),
    'fear': (128, 0, 128),
    'disgust': (0, 255, 255)
}

emotion_emojis = {
    'happy': '😄',
    'sad': '😢',
    'angry': '😠',
    'surprise': '😲',
    'neutral': '😐',
    'fear': '😱',
    'disgust': '🤢'
}

# Video capture
cap = cv2.VideoCapture(0)

# Logging
log_file = open("emotion_log.csv", mode='w', newline='')
log_writer = csv.writer(log_file)
log_writer.writerow(['Time', 'Emotion', 'Confidence'])

last_emotion = "neutral"
last_confidence = 0
last_detection_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))  # speed optimization
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)

            x_coords = [int(lm.x * w) for lm in face_landmarks.landmark]
            y_coords = [int(lm.y * h) for lm in face_landmarks.landmark]
            x_min, x_max = max(min(x_coords) - 20, 0), min(max(x_coords) + 20, w)
            y_min, y_max = max(min(y_coords) - 20, 0), min(max(y_coords) + 20, h)

            face_crop = frame[y_min:y_max, x_min:x_max]

            if time.time() - last_detection_time > 2 and face_crop.size > 0:
                try:
                    face_resized = cv2.resize(face_crop, (224, 224))
                    face_rgb = cv2.cvtColor(face_resized, cv2.COLOR_BGR2RGB)

                    face_yuv = cv2.cvtColor(face_rgb, cv2.COLOR_RGB2YUV)
                    face_yuv[:, :, 0] = cv2.equalizeHist(face_yuv[:, :, 0])
                    face_enhanced = cv2.cvtColor(face_yuv, cv2.COLOR_YUV2RGB)

                    result = DeepFace.analyze(face_enhanced, actions=['emotion'], enforce_detection=False)
                    emotion = result[0]['dominant_emotion']
                    confidence = result[0]['emotion'][emotion]
                    last_emotion = emotion
                    last_confidence = confidence
                    last_detection_time = time.time()

                    log_writer.writerow([time.strftime("%H:%M:%S"), emotion, confidence])
                except Exception as e:
                    print("Emotion detection error:", e)

    # Draw UI
    color = emotion_colors.get(last_emotion, (255, 255, 255))
    emoji = emotion_emojis.get(last_emotion, '')
    label = f'{last_emotion.upper()} {emoji} ({last_confidence:.2f}%)'

    cv2.rectangle(frame, (0, 0), (w, 40), color, -1)
    cv2.putText(frame, label, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    cv2.imshow("Enhanced Emotion Detector", frame)
    if cv2.waitKey(10) & 0xFF == 27:  # ESC to exit
        break

cap.release()
log_file.close()
cv2.destroyAllWindows()
