import cv2
from deepface import DeepFace
import matplotlib.pyplot as plt
from collections import Counter, deque
import time

# Setup deque for recent emotions
recent_emotions = deque(maxlen=30)
emotion_counts = Counter()

# Initialize plot
plt.ion()
fig, ax = plt.subplots()

def update_plot():
    ax.clear()
    common = emotion_counts.most_common()
    if common:
        emotions, counts = zip(*common)
        ax.bar(emotions, counts, color='skyblue')
        ax.set_title('Emotion Tracker')
        ax.set_ylabel('Frequency')
        plt.draw()
        plt.pause(0.001)

cap = cv2.VideoCapture(0)
last_analysis_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    cv2.imshow("Mood Tracker", frame)

    current_time = time.time()
    if current_time - last_analysis_time > 2:
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            # Handle result depending on DeepFace version (list vs dict)
            dominant_emotion = result[0]['dominant_emotion'] if isinstance(result, list) else result['dominant_emotion']
            recent_emotions.append(dominant_emotion)
            emotion_counts[dominant_emotion] += 1
            print(f"[INFO] Detected: {dominant_emotion}")
            update_plot()
            last_analysis_time = current_time
        except Exception as e:
            print(f"[ERROR] {e}")

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
plt.ioff()
plt.show()
