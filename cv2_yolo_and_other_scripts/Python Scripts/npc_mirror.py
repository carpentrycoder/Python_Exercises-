import cv2
import mediapipe as mp
import numpy as np
import math

class NPCMirror:
    def __init__(self):
        # Initialize MediaPipe
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.mp_hands = mp.solutions.hands
        self.mp_face = mp.solutions.face_mesh
        
        # Initialize pose, hands, and face detection
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.face_mesh = self.mp_face.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # NPC offset and styling
        # NPC configuration: list of dicts with individual styles and offsets
        self.npc_configs = [
            {"offset": (500, 0), "color": (255, 0, 0), "thickness": 4},     # Red NPC (right)
            {"offset": (-500, 0), "color": (0, 255, 255), "thickness": 4},  # Cyan NPC (left)
            {"offset": (200, 0), "color": (255, 255, 0), "thickness": 4},   # Yellow NPC (lower)
            {"offset": (-200, 0), "color": (255, 0, 255), "thickness": 4},  # Magenta NPC (upper)
        ]

        # Color for user's real landmarks
        self.user_color = (0, 255, 0)  # Green

        
    def calculate_npc_position(self, landmarks, frame_width, frame_height, offset):
        """Calculate NPC position with offset"""
        npc_landmarks = []
        x_offset, y_offset = offset
        
        for landmark in landmarks:
            # Convert normalized coordinates to pixel coordinates
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            
            # Apply horizontal offset for NPC (move to the left)
            npc_x = max(0, min(frame_width - 6, x + x_offset))
            npc_y = max(0, min(frame_width - 6, y + y_offset))
            
            npc_landmarks.append((npc_x , npc_y))
        
        return npc_landmarks
    
    def draw_stick_figure(self, frame, pose_landmarks,offset , color , thickness):
        """Draw NPC stick figure from pose landmarks"""
        if not pose_landmarks:
            return
        
        h, w = frame.shape[:2]
        npc_points = self.calculate_npc_position(pose_landmarks.landmark, w, h , offset)
        
        # Define body connections for stick figure
        # Improved stick figure using MediaPipe Pose Landmarks
        connections = [
            # Head and face
            (0, 1), (1, 2), (2, 3), (3, 7),  # nose to left eye to left ear
            (0, 4), (4, 5), (5, 6), (6, 8),  # nose to right eye to right ear
            (1, 4),  # connect eyes
            (7, 8),  # connect ears

            # Neck and shoulders
            (0, 11), (0, 12),  # nose to shoulders
            (11, 12),          # shoulder line

            # Spine and torso
            (11, 23), (12, 24),  # shoulders to hips
            (23, 24),            # hip line
            (11, 24), (12, 23),  # diagonal torso stability
            (11, 24), (12, 23),  # criss-cross support

            # Arms
            (11, 13), (13, 15),  # left shoulder → elbow → wrist
            (12, 14), (14, 16),  # right shoulder → elbow → wrist
            (15, 17), (16, 18),  # left/right wrist → pinky
            (15, 19), (16, 20),  # left/right wrist → index
            (15, 21), (16, 22),  # left/right wrist → thumb

            # Legs
            (23, 25), (25, 27), (27, 31),  # left hip → knee → ankle → foot
            (24, 26), (26, 28), (28, 32),  # right hip → knee → ankle → foot
            (31, 32),                      # connect feet for base line
        ]

        # Draw connections
        for start_idx, end_idx in connections:
            if start_idx < len(npc_points) and end_idx < len(npc_points):
                start_point = npc_points[start_idx]
                end_point = npc_points[end_idx]
                cv2.line(frame, start_point, end_point, color, thickness)

        for idx in [0, 11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]:
            if idx < len(npc_points):
                cv2.circle(frame, npc_points[idx], 5, color, -1)

        if len(npc_points) > 0:
            cv2.circle(frame, npc_points[0], 20, color, thickness)
    
    def draw_npc_hands(self, frame, hand_landmarks_list, offset, color, thickness):
        """Draw NPC hand landmarks with custom offset and color"""
        if not hand_landmarks_list:
            return

        h, w = frame.shape[:2]

        for hand_landmarks in hand_landmarks_list:
            npc_hand_points = self.calculate_npc_position(hand_landmarks.landmark, w, h, offset)

            # Draw hand connections
            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4),       # Thumb
                (0, 5), (5, 6), (6, 7), (7, 8),       # Index finger
                (5, 9), (9, 10), (10, 11), (11, 12),  # Middle finger
                (9, 13), (13, 14), (14, 15), (15, 16),# Ring finger
                (13, 17), (17, 18), (18, 19), (19, 20),# Pinky
                (17, 0)  # Close palm base
            ]

            for start_idx, end_idx in connections:
                if start_idx < len(npc_hand_points) and end_idx < len(npc_hand_points):
                    start_point = npc_hand_points[start_idx]
                    end_point = npc_hand_points[end_idx]
                    cv2.line(frame, start_point, end_point, color, thickness)

            # Draw fingertips
            fingertip_indices = [4, 8, 12, 16, 20]
            for idx in fingertip_indices:
                if idx < len(npc_hand_points):
                    cv2.circle(frame, npc_hand_points[idx], 5, color, -1)


    
    def draw_npc_face(self, frame, face_landmarks, offset, color, thickness):
        """Draw simplified NPC face outline with custom offset and color"""
        if not face_landmarks:
            return
        
        h, w = frame.shape[:2]
        npc_face_points = self.calculate_npc_position(face_landmarks.landmark, w, h, offset)
        
        # Face outline
        face_outline_indices = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
                                397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136,
                                172, 58, 132, 93, 234, 127, 162, 21, 54, 103, 67, 109]
        
        if len(npc_face_points) > max(face_outline_indices):
            face_points = [npc_face_points[i] for i in face_outline_indices]
            face_contour = np.array(face_points, np.int32)
            cv2.polylines(frame, [face_contour], True, color, thickness)
        
        # Eyes
        left_eye_idx = 33
        right_eye_idx = 263
        if len(npc_face_points) > max(left_eye_idx, right_eye_idx):
            cv2.circle(frame, npc_face_points[left_eye_idx], 3, color, -1)
            cv2.circle(frame, npc_face_points[right_eye_idx], 3, color, -1)

    
    def add_glow_effect(self, frame):
        """Add a subtle glow effect to the entire frame"""
        glow = cv2.GaussianBlur(frame, (15, 15), 0)
        return cv2.addWeighted(frame, 0.8, glow, 0.2, 0)
    
    def draw_ui_info(self, frame):
        """Draw UI information on frame"""
        cv2.putText(frame, "NPC Mirror - Press ESC to exit", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Green: You | Cyan: NPC", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    def run(self):
        """Main execution loop"""
        cap = cv2.VideoCapture(0)

        # Set camera properties for better performance
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FPS, 30)

        print("Starting NPC Mirror...")
        print("Press ESC to exit")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            # Flip frame horizontally for selfie-view
            frame = cv2.flip(frame, 1)

            # Convert BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process with MediaPipe
            pose_results = self.pose.process(rgb_frame)
            hands_results = self.hands.process(rgb_frame)
            face_results = self.face_mesh.process(rgb_frame)

            # Draw user's landmarks in green
            if pose_results.pose_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, pose_results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=self.user_color, thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=self.user_color, thickness=2)
                )

            if hands_results.multi_hand_landmarks:
                for hand_landmarks in hands_results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing.DrawingSpec(color=self.user_color, thickness=2, circle_radius=2),
                        self.mp_drawing.DrawingSpec(color=self.user_color, thickness=2)
                    )

            # 🧠 Draw each configured NPC
            for npc in self.npc_configs:
                if pose_results.pose_landmarks:
                    self.draw_stick_figure(
                        frame,
                        pose_results.pose_landmarks,
                        offset=npc["offset"],
                        color=npc["color"],
                        thickness=npc["thickness"]
                    )

                if hands_results.multi_hand_landmarks:
                    self.draw_npc_hands(
                        frame,
                        hands_results.multi_hand_landmarks,
                        offset=npc["offset"],
                        color=npc["color"],
                        thickness=2
                    )

                if face_results.multi_face_landmarks:
                    for face_landmarks in face_results.multi_face_landmarks:
                        self.draw_npc_face(
                            frame,
                            face_landmarks,
                            offset=npc["offset"],
                            color=npc["color"],
                            thickness=2
                        )

            # Add glow effect
            frame = self.add_glow_effect(frame)

            # Draw UI information
            self.draw_ui_info(frame)

            # Display frame
            cv2.imshow('NPC Mirror', frame)

            # Check for exit
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                break

        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("NPC Mirror stopped")



def main():
    """Entry point"""
    try:
        npc_mirror = NPCMirror()
        npc_mirror.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have OpenCV and MediaPipe installed:")
        print("pip install opencv-python mediapipe numpy")

if __name__ == "__main__":
    main()