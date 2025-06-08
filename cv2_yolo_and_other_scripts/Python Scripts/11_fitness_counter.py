import cv2
import mediapipe as mp
import numpy as np

# Pose setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

stage = None
counter = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark

        # Get hip and knee positions
        l_hip = lm[mp_pose.PoseLandmark.LEFT_HIP].y
        l_knee = lm[mp_pose.PoseLandmark.LEFT_KNEE].y
        l_ankle = lm[mp_pose.PoseLandmark.LEFT_ANKLE].y

        # Calculate knee angle (approximate)
        knee_angle = np.degrees(np.arccos(
            ((l_hip - l_knee) * (l_knee - l_ankle)) /
            (np.linalg.norm([l_hip - l_knee]) * np.linalg.norm([l_knee - l_ankle]) + 1e-5)
        ))

        # Rep logic
        if knee_angle < 100:
            stage = "down"
        if knee_angle > 160 and stage == "down":
            stage = "up"
            counter += 1
            print(f"Reps: {counter}")

        # Show count
        cv2.putText(frame, f'Reps: {counter}', (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        # Draw pose
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow("Fitness Counter - Squats", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
