import cv2
import mediapipe as mp
import numpy as np

# Corrected: Initialize MediaPipe Pose properly
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

CHEST_COLOR = (255, 0, 0)
SHOULDER_COLOR = (0, 255, 0)
BICEP_COLOR = (0, 0, 255)

cap = cv2.VideoCapture(0)

def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

while True:
    ret, frame = cap.read()  # Corrected: removed ':'
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark

        def get_point(index):
            return int(lm[index].x * w), int(lm[index].y * h)

        # Corrected: right shoulder and elbow indices
        l_shoulder = get_point(mp_pose.PoseLandmark.LEFT_SHOULDER)
        r_shoulder = get_point(mp_pose.PoseLandmark.RIGHT_SHOULDER)

        l_elbow = get_point(mp_pose.PoseLandmark.LEFT_ELBOW)
        r_elbow = get_point(mp_pose.PoseLandmark.RIGHT_ELBOW)

        l_wrist = get_point(mp_pose.PoseLandmark.LEFT_WRIST)
        r_wrist = get_point(mp_pose.PoseLandmark.RIGHT_WRIST)

        # Draw shoulders
        cv2.circle(frame, l_shoulder, 12, SHOULDER_COLOR, -1)
        cv2.circle(frame, r_shoulder, 12, SHOULDER_COLOR, -1)

        # Draw biceps (shoulder to elbow)
        cv2.line(frame, l_shoulder, l_elbow, BICEP_COLOR, 10)
        cv2.line(frame, r_shoulder, r_elbow, BICEP_COLOR, 10)

        # Draw chest line
        cv2.line(frame, l_shoulder, r_shoulder, CHEST_COLOR, 6)

        # Flex detection logic
        left_flex = l_elbow[1] < l_shoulder[1] and distance(l_wrist, l_shoulder) < 100
        right_flex = r_elbow[1] < r_shoulder[1] and distance(r_wrist, r_shoulder) < 100

        if left_flex or right_flex:
            cv2.putText(frame, "💪 FLEX DETECTED!", (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

        # Draw landmarks
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow("Muscle Pose Tracker", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
