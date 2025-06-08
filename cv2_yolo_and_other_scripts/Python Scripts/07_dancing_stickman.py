import cv2
import mediapipe as mp
import numpy as np

# MediaPipe Pose setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Define connections for stickman (simplified)
STICKMAN_CONNECTIONS = [
    # Face
    (0, 1), (1, 2), (2, 3), (3, 7),    # Face outline
    (0, 4), (4, 5), (5, 6), (6, 8),    # Face outline
    (9, 10),                            # Mouth
    
    # Arms
    (11, 12),                           # Shoulders
    (11, 13), (13, 15),                 # Left arm
    (15, 17), (17, 19), (19, 15),      # Left hand
    (15, 21),                           # Left wrist to thumb
    (12, 14), (14, 16),                 # Right arm
    (16, 18), (18, 20), (20, 16),      # Right hand  
    (16, 22),                           # Right wrist to thumb
    
    # Torso
    (11, 23), (12, 24),                 # Shoulders to hips
    (23, 24),                           # Hips
    
    # Legs
    (23, 25), (25, 27),                 # Left leg
    (27, 29), (27, 31),                 # Left foot
    (24, 26), (26, 28),                 # Right leg
    (28, 30), (28, 32),                 # Right foot
    
    # Core stability
    (11, 24), (12, 23),                 # Cross-body connections

]

# Start webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    h, w, _ = frame.shape

    if result.pose_landmarks:
        landmarks = result.pose_landmarks.landmark

        # Draw stickman
        for connection in STICKMAN_CONNECTIONS:
            start_idx, end_idx = connection
            x1, y1 = int(landmarks[start_idx].x * w), int(landmarks[start_idx].y * h)
            x2, y2 = int(landmarks[end_idx].x * w), int(landmarks[end_idx].y * h)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 255), 4)

        # Draw joints
        for idx in [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]:
            x, y = int(landmarks[idx].x * w), int(landmarks[idx].y * h)
            cv2.circle(frame, (x, y), 6, (255, 0, 0), cv2.FILLED)

        # Optional: Draw central head point
        head_x = int(landmarks[0].x * w)
        head_y = int(landmarks[0].y * h)
        cv2.circle(frame, (head_x, head_y), 10, (0, 0, 255), 3)

    cv2.imshow("Dancing Stickman", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
