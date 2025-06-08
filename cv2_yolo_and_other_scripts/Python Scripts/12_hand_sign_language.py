import cv2
import mediapipe as mp
import pyttsx3

# Setup TTS
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Define finger tip landmarks
tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

# Text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Webcam
cap = cv2.VideoCapture(0)
prev_sign = ''

def detect_sign(fingers):
    # Match finger combinations
    if fingers == [1, 1, 1, 1, 1]:
        return "Hello"
    elif fingers == [1, 1, 0, 0, 1]:
        return "Love"
    elif fingers == [1, 0, 0, 0, 0]:
        return "Yes"
    elif fingers == [0, 0, 0, 0, 0]:
        return "No"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Peace"
    elif fingers == [1, 1, 1, 1, 1]:  # Same as Hello
        return "Stop"
    return "Unknown"

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(handLms.landmark):
                h, w, _ = frame.shape
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            fingers = []

            # Thumb
            fingers.append(1 if lm_list[tip_ids[0]][0] > lm_list[tip_ids[0] - 1][0] else 0)

            # Fingers (index to pinky)
            for id in range(1, 5):
                fingers.append(1 if lm_list[tip_ids[id]][1] < lm_list[tip_ids[id] - 2][1] else 0)

            # Detect sign
            sign = detect_sign(fingers)
            cv2.putText(frame, f'Sign: {sign}', (30, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 0, 255), 3)

            # Speak only when new sign appears
            if sign != prev_sign and sign != "Unknown":
                speak(sign)
                print(sign)
                prev_sign = sign

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Sign Language Detector", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
