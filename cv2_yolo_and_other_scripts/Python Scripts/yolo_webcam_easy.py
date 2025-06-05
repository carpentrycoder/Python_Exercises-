from ultralytics import YOLO
import cv2

# Load YOLOv8 model (you can also use "yolov8n.pt" for nano or "yolov8s.pt")
model = YOLO("yolov8n.pt")  # Tiny model, fast and lightweight

# Start webcam
cap = cv2.VideoCapture(0)

print("📦 YOLOv8 Object Detection running... Press ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLOv8 on the frame
    results = model(frame, stream=True)

    # Draw results
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0])
            conf = box.conf[0]

            label = f"{model.names[cls]} {conf:.2f}"
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Show result
    cv2.imshow("YOLOv8 - Webcam", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
