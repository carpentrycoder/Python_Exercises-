import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import threading
import time
import os

class FaceDistanceEstimator:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        
        # Eye landmark indices (left and right eye corners)
        self.LEFT_EYE_CORNERS = [33, 133]  # Inner and outer corners
        self.RIGHT_EYE_CORNERS = [362, 263]  # Inner and outer corners
        
        # Distance thresholds (in cm)
        self.TOO_CLOSE_THRESHOLD = 30
        self.TOO_FAR_THRESHOLD = 100
        self.OPTIMAL_DISTANCE = 60
        
        # Average human eye distance in cm
        self.AVERAGE_EYE_DISTANCE_CM = 6.3
        
        # Voice feedback control
        self.last_voice_time = 0
        self.voice_cooldown = 3  # seconds
        
        # Frame saving
        self.save_frames = True
        self.frames_dir = "distance_frames"
        if self.save_frames and not os.path.exists(self.frames_dir):
            os.makedirs(self.frames_dir)
    
    def speak_async(self, text):
        """Speak text asynchronously to avoid blocking main thread"""
        current_time = time.time()
        if current_time - self.last_voice_time > self.voice_cooldown:
            self.last_voice_time = current_time
            threading.Thread(target=self._speak, args=(text,), daemon=True).start()
    
    def _speak(self, text):
        """Internal method to handle TTS"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except:
            pass
    
    def calculate_distance(self, landmarks, img_width, img_height):
        """Calculate distance between eyes in pixels and estimate real distance"""
        # Get eye corner landmarks
        left_eye_outer = landmarks[self.LEFT_EYE_CORNERS[1]]
        right_eye_outer = landmarks[self.RIGHT_EYE_CORNERS[1]]
        
        # Convert normalized coordinates to pixel coordinates
        left_x = int(left_eye_outer.x * img_width)
        left_y = int(left_eye_outer.y * img_height)
        right_x = int(right_eye_outer.x * img_width)
        right_y = int(right_eye_outer.y * img_height)
        
        # Calculate pixel distance between eyes
        pixel_distance = np.sqrt((right_x - left_x)**2 + (right_y - left_y)**2)
        
        # Estimate real-world distance using similar triangles
        # Distance = (Real_eye_distance * focal_length) / pixel_distance
        # Using approximated focal length for standard webcam
        focal_length = img_width  # Approximation for standard webcam
        estimated_distance_cm = (self.AVERAGE_EYE_DISTANCE_CM * focal_length) / pixel_distance
        
        return pixel_distance, estimated_distance_cm, (left_x, left_y), (right_x, right_y)
    
    def draw_distance_info(self, img, distance_cm, pixel_distance):
        """Draw distance information on the image"""
        # Background rectangle for text
        cv2.rectangle(img, (10, 10), (400, 120), (0, 0, 0), -1)
        cv2.rectangle(img, (10, 10), (400, 120), (255, 255, 255), 2)
        
        # Distance information
        cv2.putText(img, f"Distance: {distance_cm:.1f} cm", (20, 35), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(img, f"Pixel Distance: {pixel_distance:.1f}", (20, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Status based on distance
        if distance_cm < self.TOO_CLOSE_THRESHOLD:
            status = "TOO CLOSE!"
            color = (0, 0, 255)  # Red
            self.speak_async("You are too close to the camera")
        elif distance_cm > self.TOO_FAR_THRESHOLD:
            status = "TOO FAR!"
            color = (0, 165, 255)  # Orange
            self.speak_async("You are too far from the camera")
        else:
            status = "OPTIMAL DISTANCE"
            color = (0, 255, 0)  # Green
        
        cv2.putText(img, status, (20, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        return status
    
    def save_frame(self, img, status, distance):
        """Save frame if user is too close or too far"""
        if status in ["TOO CLOSE!", "TOO FAR!"] and self.save_frames:
            timestamp = int(time.time())
            filename = f"{self.frames_dir}/frame_{status.replace(' ', '_').replace('!', '')}_{distance:.1f}cm_{timestamp}.jpg"
            cv2.imwrite(filename, img)
    
    def run(self):
        """Main application loop"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        print("Face Distance Estimator Started!")
        print("Press 'q' to quit")
        print("Features:")
        print("- Real-time distance estimation")
        print("- Voice feedback for distance warnings")
        print("- Automatic frame saving for extreme distances")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process face mesh
            results = self.face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    h, w, _ = frame.shape
                    
                    # Calculate distance
                    pixel_dist, real_dist, left_eye, right_eye = self.calculate_distance(
                        face_landmarks.landmark, w, h
                    )
                    
                    # Draw eye points
                    cv2.circle(frame, left_eye, 5, (0, 255, 0), -1)
                    cv2.circle(frame, right_eye, 5, (0, 255, 0), -1)
                    cv2.line(frame, left_eye, right_eye, (255, 0, 0), 2)
                    
                    # Draw distance information
                    status = self.draw_distance_info(frame, real_dist, pixel_dist)
                    
                    # Save frame if needed
                    self.save_frame(frame, status, real_dist)
                    
                    # Draw face mesh (optional - can be commented out for cleaner view)
                    # self.mp_drawing.draw_landmarks(
                    #     frame, face_landmarks, self.mp_face_mesh.FACEMESH_CONTOURS,
                    #     None, self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                    # )
            
            else:
                # No face detected
                cv2.putText(frame, "No face detected", (50, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Display frame
            cv2.imshow('Face Distance Estimator', frame)
            
            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        self.tts_engine.stop()

if __name__ == "__main__":
    estimator = FaceDistanceEstimator()
    estimator.run()