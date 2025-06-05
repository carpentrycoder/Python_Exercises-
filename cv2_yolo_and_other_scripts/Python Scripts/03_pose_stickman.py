import cv2
import mediapipe as mp

# Initialize Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Define your stickman connections
STICKMAN_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 7),  # Nose to ears
    (0, 4), (4, 5), (5, 6), (6, 8),
    (11, 12),  # Shoulders
    (11, 13), (13, 15),  # Left arm
    (12, 14), (14, 16),  # Right arm
    (11, 23), (12, 24),  # Spine
    (23, 24),  # Hip line
    (23, 25), (25, 27), (27, 31),  # Left leg
    (24, 26), (26, 28), (28, 32),  # Right leg
]

# Start webcam
cap = cv2.VideoCapture(0)

print("🕴️ Pose Stickman running... Press ESC to exit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    if result.pose_landmarks:
        landmarks = result.pose_landmarks.landmark
        h, w, _ = frame.shape

        # Convert to pixel coordinates
        points = []
        for lm in landmarks:
            x = int(lm.x * w)
            y = int(lm.y * h)
            points.append((x, y))

        # Draw connections manually
        for start_idx, end_idx in STICKMAN_CONNECTIONS:
            if start_idx < len(points) and end_idx < len(points):
                cv2.line(frame, points[start_idx], points[end_idx], (255, 0, 255), 3)

        # Optional: draw joints
        for idx in [0, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]:
            cv2.circle(frame, points[idx], 5, (0, 255, 0), -1)

    cv2.imshow("Pose Stickman - Press ESC to Quit", frame)

    if cv2.waitKey(10) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
