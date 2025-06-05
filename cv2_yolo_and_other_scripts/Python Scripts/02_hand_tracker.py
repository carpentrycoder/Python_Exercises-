import cv2
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Finger tip landmark IDs
finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

cap = cv2.VideoCapture(0)

print("🖐️ Hand Tracking started... Press ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for mirror view and convert color
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            h, w, _ = frame.shape

            finger_count = 0

            # Thumb (special case: compare x-coordinates)
            if lm[finger_tips[0]].x < lm[finger_tips[0] - 1].x:
                finger_count += 1

            # Other fingers
            for tip in finger_tips[1:]:
                if lm[tip].y < lm[tip - 2].y:  # Tip above the PIP joint
                    finger_count += 1

            # Draw landmarks
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Display finger count
            cv2.putText(frame, f'Fingers: {finger_count}', (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Hand Tracker - Press ESC to Quit", frame)

    if cv2.waitKey(10) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
