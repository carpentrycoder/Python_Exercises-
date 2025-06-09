import cv2
import mediapipe as mp
import numpy as np

# Transparent PNG overlay helper
def overlay_transparent(background, overlay, x, y):
    bh, bw = background.shape[:2]
    h, w = overlay.shape[:2]

    if x < 0 or y < 0 or x + w > bw or y + h > bh:
        # Clip overlay to stay within frame
        x = max(0, x)
        y = max(0, y)
        w = min(w, bw - x)
        h = min(h, bh - y)
        overlay = overlay[0:h, 0:w]

    if overlay.shape[2] < 4:
        return background

    alpha_s = overlay[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(3):
        background[y:y+h, x:x+w, c] = (
            alpha_s * overlay[:, :, c] +
            alpha_l * background[y:y+h, x:x+w, c]
        )
    return background

# Load AR PNGs
glasses = cv2.imread("sunglasses.png", cv2.IMREAD_UNCHANGED)
moustache = cv2.imread("beard.png", cv2.IMREAD_UNCHANGED)
# Optional: Add forehead accessory
forehead_mark = cv2.imread("tilak.png", cv2.IMREAD_UNCHANGED)  # Optional PNG

# MediaPipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            lm = face_landmarks.landmark

            # Glasses
            left_eye = lm[33]
            right_eye = lm[263]
            eye_w = int((right_eye.x - left_eye.x) * w * 1.8)
            eye_h = int(eye_w * glasses.shape[0] / glasses.shape[1])
            eye_x = int(left_eye.x * w - 0.1 * eye_w)
            eye_y = int(left_eye.y * h - 0.5 * eye_h)
            resized_glasses = cv2.resize(glasses, (eye_w, eye_h))
            frame = overlay_transparent(frame, resized_glasses, eye_x, eye_y)

            # Moustache
            upper_lip = lm[13]
            lower_lip = lm[14]
            lip_x = int((upper_lip.x + lower_lip.x) / 2 * w)
            lip_y = int((upper_lip.y + lower_lip.y) / 2 * h)
            moustache_w = int(eye_w * 0.7)
            moustache_h = int(moustache_w * moustache.shape[0] / moustache.shape[1])
            resized_moustache = cv2.resize(moustache, (moustache_w, moustache_h))
            frame = overlay_transparent(
                frame, resized_moustache,
                lip_x - moustache_w // 2, lip_y
            )

            # Optional: Forehead marker (extrapolated above nose)
            nose = lm[1]
            forehead_x = int(nose.x * w)
            forehead_y = int(nose.y * h - 0.2 * h)  # approx 20% upward
            if forehead_mark is not None:
                forehead_w = int(eye_w * 0.3)
                forehead_h = int(forehead_w * forehead_mark.shape[0] / forehead_mark.shape[1])
                resized_forehead = cv2.resize(forehead_mark, (forehead_w, forehead_h))
                frame = overlay_transparent(
                    frame, resized_forehead,
                    forehead_x - forehead_w // 2, forehead_y
                )

    cv2.imshow("AR Face Mesh Filters", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
