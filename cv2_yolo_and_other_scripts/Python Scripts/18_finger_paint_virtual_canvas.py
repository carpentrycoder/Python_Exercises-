import cv2
import mediapipe as mp
import numpy as np
import time

class FingerPaintCanvas:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Canvas and Frame dimensions
        self.frame_width = 1280  # This will be the width of your video frame
        self.frame_height = 720 # This will be the height of your video frame
        
        self.ui_height = 80 # Height reserved for UI
        # The actual drawing canvas will be the frame height minus the UI height
        self.canvas_height = self.frame_height - self.ui_height 
        self.canvas_width = self.frame_width

        # Initialize the actual drawing canvas
        self.canvas = np.zeros((self.canvas_height, self.canvas_width, 3), dtype=np.uint8)
        
        # Drawing
        self.current_color = (255, 0, 0)
        self.brush_size = 5
        self.colors = {
            'blue': (255, 0, 0),
            'green': (0, 255, 0),
            'red': (0, 0, 255),
            'yellow': (0, 255, 255),
            'purple': (255, 0, 255)
        }
        
        self.prev_x, self.prev_y = None, None
        self.drawing = False
        
        self.gesture_cooldown = 1.0
        self.last_gesture_time = 0
        

    def get_landmark_position(self, landmarks, landmark_id, img_width, img_height):
        if 0 <= landmark_id < len(landmarks):
            x = int(landmarks[landmark_id].x * img_width)
            y = int(landmarks[landmark_id].y * img_height)
            return x, y
        return None, None

    def is_finger_up(self, landmarks, tip_id, pip_id):
        if tip_id < len(landmarks) and pip_id < len(landmarks):
            return landmarks[tip_id].y < landmarks[pip_id].y
        return False

    def count_extended_fingers(self, landmarks):
        finger_tips = [4, 8, 12, 16, 20]
        finger_pips = [3, 6, 10, 14, 18]
        extended = 0
        finger_states = []

        for i, (tip, pip) in enumerate(zip(finger_tips, finger_pips)):
            if i == 0:  # thumb
                # Simplified thumb check for right hand (assuming positive x for extended)
                # You might need to adjust this for left hand or more robust detection
                if landmarks[tip].x > landmarks[pip].x: 
                    extended += 1
                    finger_states.append(True)
                else:
                    finger_states.append(False)
            else:
                if self.is_finger_up(landmarks, tip, pip):
                    extended += 1
                    finger_states.append(True)
                else:
                    finger_states.append(False)

        return extended, finger_states

    def recognize_gesture(self, landmarks):
        count, states = self.count_extended_fingers(landmarks)
        if states[0] and not any(states[1:]):
            return "thumbs_up", "blue"
        elif states[1] and states[2] and not states[3] and not states[4]:
            return "peace", "green"
        elif states[1] and states[2] and states[3] and not states[4]:
            return "three_fingers", "red"
        elif not states[0] and all(states[1:]):
            return "four_fingers", "yellow"
        elif all(states):
            return "five_fingers", "purple"
        elif count == 0:
            return "fist", "clear"
        elif states[1] and not any([states[0], states[2], states[3], states[4]]):
            return "draw", "draw"
        return None, None

    def draw_ui(self, frame):
        # Draw the UI directly onto the frame, in the top section
        cv2.rectangle(frame, (0, 0), (self.frame_width, self.ui_height), (50, 50, 50), -1)
        cv2.rectangle(frame, (10, 10), (60, 60), self.current_color, -1)
        cv2.rectangle(frame, (10, 10), (60, 60), (255, 255, 255), 2)
        cv2.putText(frame, "Current", (5, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        x_offset = 80
        for name, color in self.colors.items():
            cv2.rectangle(frame, (x_offset, 15), (x_offset + 40, 55), color, -1)
            cv2.rectangle(frame, (x_offset, 15), (x_offset + 40, 55), (255, 255, 255), 1)
            x_offset += 50

    def process_hand(self, hand_landmarks, frame):
        h, w, _ = frame.shape
        index_x, index_y = self.get_landmark_position(hand_landmarks.landmark, 8, w, h)
        if index_x is None or index_y is None:
            return

        current_time = time.time()
        gesture, action = self.recognize_gesture(hand_landmarks.landmark)

        if gesture and current_time - self.last_gesture_time > self.gesture_cooldown:
            if action == "clear":
                # Clear the actual drawing canvas
                self.canvas = np.zeros((self.canvas_height, self.canvas_width, 3), dtype=np.uint8)
                print("Canvas cleared!")
            elif action in self.colors:
                self.current_color = self.colors[action]
                print(f"Color changed to {action}")
            self.last_gesture_time = current_time

        if gesture == "draw":
            # Adjust y-coordinate for drawing on the main canvas area (below UI)
            draw_y = index_y - self.ui_height 
            
            # Ensure drawing happens only within the bounds of the drawing canvas
            if draw_y >= 0 and draw_y < self.canvas_height:
                if self.prev_x is not None and self.prev_y is not None:
                    # Draw on the 'canvas' itself
                    cv2.line(self.canvas, (self.prev_x, self.prev_y), (index_x, draw_y), self.current_color, self.brush_size)
                self.prev_x, self.prev_y = index_x, draw_y
            else: # If finger is in UI area or outside canvas
                self.prev_x, self.prev_y = None, None
        else:
            self.prev_x, self.prev_y = None, None

        self.mp_drawing.draw_landmarks(
            frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
        )

        cv2.circle(frame, (index_x, index_y), 8, (0, 255, 255), -1)
        if gesture:
            cv2.putText(frame, f"Gesture: {gesture}", (index_x + 10, index_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.frame_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frame_height)

        if not cap.isOpened():
            print("Error: Camera not found.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)

            if results.multi_hand_landmarks:
                for hand in results.multi_hand_landmarks:
                    self.process_hand(hand, frame)
            else:
                self.prev_x, self.prev_y = None, None

            # Create a full-size canvas to blend, including space for UI
            # This canvas will be the same size as the 'frame'
            full_display_canvas = np.zeros_like(frame)
            
            # Copy the actual drawing canvas onto the lower part of full_display_canvas
            full_display_canvas[self.ui_height:, :] = self.canvas 

            # Blend the original frame with the full_display_canvas
            blended = cv2.addWeighted(frame, 0.3, full_display_canvas, 0.7, 0)
            
            # Draw the UI elements on top of the blended frame
            self.draw_ui(blended)

            cv2.imshow('Finger Paint Virtual Canvas', blended)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # When saving, save only the actual drawing canvas part
                filename = f"finger_paint_{int(time.time())}.jpg"
                cv2.imwrite(filename, self.canvas) 
                print(f"Canvas saved as {filename}")

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = FingerPaintCanvas()
    app.run()