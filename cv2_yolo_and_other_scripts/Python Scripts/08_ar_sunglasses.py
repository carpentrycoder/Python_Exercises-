import cv2
import mediapipe as mp
import numpy as np

# Load sunglasses PNG with alpha channel
sunglasses_img = cv2.imread("sunglasses.png", cv2.IMREAD_UNCHANGED)

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)

# Eye landmark indices
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]

# Webcam
cap = cv2.VideoCapture(0)

def overlay_transparent(background, overlay, x, y, overlay_size=None):
    if overlay_size:
        overlay = cv2.resize(overlay, overlay_size)

    h, w, _ = overlay.shape
    bg_h, bg_w, _ = background.shape

    if x + w > bg_w or y + h > bg_h or x < 0 or y < 0:
        return background

    alpha_s = overlay[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(3):
        background[y:y+h, x:x+w, c] = (
            alpha_s * overlay[:, :, c] +
            alpha_l * background[y:y+h, x:x+w, c]
        )

    return background

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        for landmarks in result.multi_face_landmarks:
            # Get eye coordinates
            left = landmarks.landmark[LEFT_EYE[0]]
            right = landmarks.landmark[RIGHT_EYE[1]]
            x1, y1 = int(left.x * w), int(left.y * h)
            x2, y2 = int(right.x * w), int(right.y * h)

            # Center between eyes
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            # Width and scale of sunglasses
            sunglasses_width = int(1.4 * abs(x2 - x1))
            overlay_h = int(sunglasses_width * sunglasses_img.shape[0] / sunglasses_img.shape[1])
            x_offset = cx - sunglasses_width // 2
            y_offset = cy - overlay_h // 2

            # Overlay sunglasses
            frame = overlay_transparent(frame, sunglasses_img, x_offset, y_offset, (sunglasses_width, overlay_h))

    cv2.imshow("AR Sunglasses Filter", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
