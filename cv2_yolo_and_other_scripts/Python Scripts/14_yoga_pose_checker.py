import cv2
import mediapipe as mp
import numpy as np
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    """Calculates angle between 3 points."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

cap = cv2.VideoCapture(0)
pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.pose_landmarks:
        lm = results.pose_landmarks.landmark

        # Get required landmarks
        def get_landmark(name):
            pt = lm[mp_pose.PoseLandmark[name].value]
            return [pt.x * w, pt.y * h]

        # Arms
        left_shoulder = get_landmark("LEFT_SHOULDER")
        left_elbow = get_landmark("LEFT_ELBOW")
        left_wrist = get_landmark("LEFT_WRIST")

        right_shoulder = get_landmark("RIGHT_SHOULDER")
        right_elbow = get_landmark("RIGHT_ELBOW")
        right_wrist = get_landmark("RIGHT_WRIST")

        # Legs
        left_hip = get_landmark("LEFT_HIP")
        left_knee = get_landmark("LEFT_KNEE")
        left_ankle = get_landmark("LEFT_ANKLE")

        right_hip = get_landmark("RIGHT_HIP")
        right_knee = get_landmark("RIGHT_KNEE")
        right_ankle = get_landmark("RIGHT_ANKLE")

        # Angles
        left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        left_shoulder_angle = calculate_angle(left_elbow, left_shoulder, left_hip)
        right_shoulder_angle = calculate_angle(right_elbow, right_shoulder, right_hip)
        left_leg_angle = calculate_angle(left_hip, left_knee, left_ankle)
        right_leg_angle = calculate_angle(right_hip, right_knee, right_ankle)

        # Display angles
        cv2.putText(image, f'L Elbow: {int(left_arm_angle)}', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(image, f'R Elbow: {int(right_arm_angle)}', (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Pose logic
        pose_status = "Detecting..."
        color = (255, 255, 0)

        if 160 <= left_arm_angle <= 200 and 160 <= right_arm_angle <= 200 and \
           70 <= left_shoulder_angle <= 110 and 70 <= right_shoulder_angle <= 110:
            pose_status = "T-Pose ✔️"
            color = (0, 255, 0)

        elif 170 <= left_shoulder_angle <= 190 and 170 <= right_shoulder_angle <= 190:
            pose_status = "Hands-Up Pose 🙌"
            color = (0, 200, 255)

        elif 80 <= left_arm_angle <= 100:
            pose_status = "Warrior II Left 💪"
            color = (255, 100, 100)

        elif 80 <= right_arm_angle <= 100:
            pose_status = "Warrior II Right 💪"
            color = (255, 100, 100)

        elif 80 <= left_leg_angle <= 100 or 80 <= right_leg_angle <= 100:
            pose_status = "Tree Pose 🧘"
            color = (153, 0, 204)

        cv2.putText(image, pose_status, (10, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.1, color, 3)

        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow('Yoga Pose Checker', image)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
