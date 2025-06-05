import cv2
import mediapipe as mp
import numpy as np

# Setup MediaPipe
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose()
hands = mp_hands.Hands(max_num_hands=2)
face = mp_face.FaceMesh(refine_landmarks=True)

# Webcam
cap = cv2.VideoCapture(0)

print("🪞 NPC AR Mirror running... Press ESC to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pose_result = pose.process(rgb)
    hands_result = hands.process(rgb)
    face_result = face.process(rgb)

    # ========== 1. Draw user's real face mesh ==========
    if face_result.multi_face_landmarks:
        for landmarks in face_result.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                frame, landmarks, mp_face.FACEMESH_CONTOURS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=1, circle_radius=1),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=1)
            )

    # ========== 2. Draw user's hand landmarks ==========
    if hands_result.multi_hand_landmarks:
        for landmarks in hands_result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )

    # ========== 3. NPC Pose Drawing (stickman) ==========
    if pose_result.pose_landmarks:
        landmarks = pose_result.pose_landmarks.landmark
        points = []
        for lm in landmarks:
            x = int(lm.x * w) - 250  # Offset NPC to the left
            y = int(lm.y * h)
            points.append((x, y))

        # Draw stickman body
        connections = [
            (11, 13), (13, 15),  # Left arm
            (12, 14), (14, 16),  # Right arm
            (11, 12),            # Shoulders
            (11, 23), (12, 24),  # Torso
            (23, 25), (25, 27), (27, 31),  # Left leg
            (24, 26), (26, 28), (28, 32),  # Right leg
        ]
        for start, end in connections:
            if start < len(points) and end < len(points):
                cv2.line(frame, points[start], points[end], (0, 255, 255), 3)

        # Draw head as a circle
        head_x, head_y = points[0]
        cv2.circle(frame, (head_x, head_y), 20, (255, 255, 0), 3)

    # Optional: Glow Filter
    blurred = cv2.GaussianBlur(frame, (15, 15), 0)
    frame = cv2.addWeighted(frame, 0.8, blurred, 0.2, 0)

    # Display
    cv2.imshow("NPC AR Mirror", frame)

    if cv2.waitKey(10) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
