import cv2
import mediapipe as mp
import numpy as np
import random

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Game dimensions
w, h = 1280, 720
paddle_height = 150
paddle_width = 30
ball_radius = 20

# Initialize ball
ball_x, ball_y = w // 2, h // 2
ball_dx, ball_dy = 12 * random.choice([-1, 1]), 12 * random.choice([-1, 1])

# Score
score = 0

# Camera
cap = cv2.VideoCapture(0)
cap.set(3, w)
cap.set(4, h)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (w, h))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    # Default paddle position
    paddle_y = h // 2 - paddle_height // 2

    # Track hand
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get index finger tip
            lm = hand_landmarks.landmark[8]
            cx, cy = int(lm.x * w), int(lm.y * h)
            paddle_y = cy - paddle_height // 2

            # Draw hand landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Keep paddle within screen
    paddle_y = np.clip(paddle_y, 0, h - paddle_height)

    # Move ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Bounce on top and bottom
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= h:
        ball_dy *= -1

    # Bounce off paddle (left wall)
    if (0 <= ball_x - ball_radius <= paddle_width and
        paddle_y <= ball_y <= paddle_y + paddle_height):
        ball_dx *= -1
        score += 1
        ball_x = paddle_width + ball_radius + 1  # Push ball outside paddle to prevent sticking

    # Bounce off right wall (optional)
    if ball_x + ball_radius >= w:
        ball_dx *= -1
        ball_x = w - ball_radius - 1  # Push back inside

    # Missed ball (left wall)
    if ball_x + ball_radius < 0:
        ball_x, ball_y = w // 2, h // 2
        ball_dx = 12 * random.choice([-1, 1])
        ball_dy = 12 * random.choice([-1, 1])
        score = 0


    # Draw paddle
    cv2.rectangle(frame, (0, paddle_y), (paddle_width, paddle_y + paddle_height), (0, 255, 0), -1)

    # Draw ball
    cv2.circle(frame, (ball_x, ball_y), ball_radius, (255, 0, 0), -1)

    # Draw score
    cv2.putText(frame, f'Score: {score}', (1000, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 0), 3)

    # Show frame
    cv2.imshow("Hand Pong Game", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
