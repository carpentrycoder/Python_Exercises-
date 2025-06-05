import cv2
import mediapipe as mp
import streamlit as st
import numpy as np
from deepface import DeepFace
import time

st.set_page_config(page_title="Real-time Face Mesh & Emotion", layout="wide")

# Title
st.title("💠 Real-time Face Mesh with Emotion & Gesture Detection")

# Webcam switch
run = st.checkbox("▶️ Start Webcam")

# Streamlit layout
video_col, info_col = st.columns([3, 1])
FRAME_WINDOW = video_col.image([])

# Initialize
mp_fm = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
face_mesh = mp_fm.FaceMesh(refine_landmarks=True, max_num_faces=1)

cap = cv2.VideoCapture(0)
prev_time = 0

def get_emotion(frame):
    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        return analysis[0]['dominant_emotion'], analysis[0]['emotion']
    except:
        return "No face", {}

def is_mouth_open(landmarks, img_w, img_h):
    top_lip = landmarks[13]
    bottom_lip = landmarks[14]
    y1 = int(top_lip.y * img_h)
    y2 = int(bottom_lip.y * img_h)
    return abs(y2 - y1) > 15

# Streamlit placeholders
emotion_text = info_col.empty()
gesture_text = info_col.empty()
fps_text = info_col.empty()
emotion_scores = info_col.empty()

while run:
    ret, frame = cap.read()
    if not ret:
        st.error("❌ Failed to access webcam.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, _ = frame.shape

    # Detect facial mesh
    results = face_mesh.process(rgb_frame)
    mouth_status = "Not Detected"

    if results.multi_face_landmarks:
        for landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=rgb_frame,
                landmark_list=landmarks,
                connections=mp_fm.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec,
            )
            # Check gesture
            mouth_status = "Mouth Open" if is_mouth_open(landmarks.landmark, w, h) else "Mouth Closed"

    # Emotion detection
    emotion, emotion_data = get_emotion(frame)

    # FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time + 1e-5)
    prev_time = curr_time

    # Display in UI (not on frame)
    gesture_text.markdown(f"### 🤖 Gesture: `{mouth_status}`")
    emotion_text.markdown(f"### 😊 Emotion: `{emotion}`")
    fps_text.markdown(f"### ⏱️ FPS: `{int(fps)}`")

    # Show emotion confidence scores
    if emotion_data:
        emotion_scores.markdown("### 📊 Emotion Confidence")
        for emo, score in emotion_data.items():
            info_col.progress(min(int(score), 100), text=f"{emo.capitalize()}: {int(score)}%")

    # Update image
    FRAME_WINDOW.image(rgb_frame)

cap.release()
