import mediapipe as mp
import cv2
import numpy as np
import winsound
import threading
import time
import math

# Initialize MediaPipe hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,  # Allow both hands
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

class VirtualTheremin:
    def __init__(self):
        self.notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.frequencies = [261, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494]
        self.current_freq = 0
        self.is_playing = False
        self.volume_level = 0
        self.note_history = []
        self.colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (127, 255, 0), 
                      (0, 255, 0), (0, 255, 127), (0, 255, 255), (0, 127, 255),
                      (0, 0, 255), (127, 0, 255), (255, 0, 255), (255, 0, 127)]
        self.sound_thread = None
        self.stop_sound = False
        
    def play_beep(self, frequency, duration=100):
        """Play a beep using Windows system sounds"""
        if frequency > 0:
            try:
                winsound.Beep(int(frequency), duration)
            except:
                pass  # Ignore if beep fails
    
    def start_continuous_tone(self, frequency):
        """Start playing a continuous tone"""
        if self.sound_thread and self.sound_thread.is_alive():
            self.stop_sound = True
            self.sound_thread.join()
        
        self.stop_sound = False
        self.current_freq = frequency
        self.sound_thread = threading.Thread(target=self._play_continuous)
        self.sound_thread.start()
    
    def _play_continuous(self):
        """Play continuous tone in separate thread"""
        while not self.stop_sound and self.current_freq > 0:
            self.play_beep(self.current_freq, 200)
            time.sleep(0.1)
    
    def stop_tone(self):
        """Stop the continuous tone"""
        self.stop_sound = True
        if self.sound_thread and self.sound_thread.is_alive():
            self.sound_thread.join()

def calculate_hand_distance(landmarks):
    """Calculate distance between thumb and index finger"""
    thumb_tip = landmarks.landmark[4]
    index_tip = landmarks.landmark[8]
    
    distance = math.sqrt(
        (thumb_tip.x - index_tip.x)**2 + 
        (thumb_tip.y - index_tip.y)**2
    )
    return distance

def get_hand_center(landmarks):
    """Get center position of hand"""
    x_coords = [lm.x for lm in landmarks.landmark]
    y_coords = [lm.y for lm in landmarks.landmark]
    
    center_x = sum(x_coords) / len(x_coords)
    center_y = sum(y_coords) / len(y_coords)
    
    return center_x, center_y

def map_position_to_frequency(x_pos, y_pos, base_freq=200, max_freq=800):
    """Map hand position to frequency like a theremin"""
    # X position controls pitch
    frequency = base_freq + (x_pos * (max_freq - base_freq))
    
    # Y position controls volume (but we'll use it for pitch modulation)
    pitch_mod = 1.0 + (y_pos - 0.5) * 0.5  # ±25% pitch modulation
    
    return int(frequency * pitch_mod)

def draw_theremin_interface(image, theremin, hand_positions, frequencies):
    """Draw theremin-style interface"""
    height, width, _ = image.shape
    
    # Draw frequency spectrum background
    for i in range(width):
        freq_ratio = i / width
        color_intensity = int(255 * freq_ratio)
        cv2.line(image, (i, height-150), (i, height-100), 
                (0, color_intensity, 255-color_intensity), 1)
    
    # Draw hand positions and their effects
    for i, (pos, freq) in enumerate(zip(hand_positions, frequencies)):
        if pos:
            x, y = pos
            screen_x = int(x * width)
            screen_y = int(y * height)
            
            # Draw hand marker
            color = (0, 255, 0) if i == 0 else (255, 0, 0)  # Green for first hand, red for second
            cv2.circle(image, (screen_x, screen_y), 20, color, 3)
            
            # Draw frequency indicator
            freq_x = int((freq - 200) / 600 * width)  # Map freq to screen width
            if 0 <= freq_x < width:
                cv2.line(image, (freq_x, height-150), (freq_x, height-50), color, 5)
                cv2.putText(image, f"{freq}Hz", (freq_x-30, height-30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    return image

def draw_volume_bars(image, distances):
    """Draw volume level based on finger distances"""
    height, width, _ = image.shape
    
    for i, distance in enumerate(distances):
        if distance is not None:
            # Map distance to volume bar height (closer fingers = higher volume)
            volume = max(0, 1 - distance * 5)  # Invert distance
            bar_height = int(volume * 100)
            
            x_pos = 50 + i * 100
            bar_color = (0, int(255 * volume), int(255 * (1-volume)))
            
            # Draw volume bar
            cv2.rectangle(image, (x_pos, height-200), 
                         (x_pos + 30, height-200 + bar_height), bar_color, -1)
            
            # Draw volume percentage
            cv2.putText(image, f"{int(volume*100)}%", (x_pos-5, height-205), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    
    return image

def draw_instructions(image):
    """Draw instructions"""
    instructions = [
        "Virtual Theremin - Control sound with hand movements!",
        "Move hands left/right to change pitch, up/down for modulation",
        "Pinch thumb+index finger to control volume",
        "Press 'q' to quit, 's' to stop sound"
    ]
    
    y_offset = 30
    for instruction in instructions:
        cv2.putText(image, instruction, (10, y_offset), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        y_offset += 20
    
    return image

def main():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
    
    theremin = VirtualTheremin()
    last_play_time = 0
    
    print("Virtual Theremin Started!")
    print("Move your hands to control the sound like a theremin!")
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                continue

            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Convert BGR to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Process hand landmarks
            hand_positions = []
            frequencies = []
            distances = []
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    # Get hand center position
                    center_x, center_y = get_hand_center(hand_landmarks)
                    hand_positions.append((center_x, center_y))
                    
                    # Calculate frequency based on position
                    frequency = map_position_to_frequency(center_x, center_y)
                    frequencies.append(frequency)
                    
                    # Calculate finger distance for volume
                    distance = calculate_hand_distance(hand_landmarks)
                    distances.append(distance)
                
                # Play sound based on first hand (if present)
                if frequencies and distances:
                    current_time = time.time()
                    main_freq = frequencies[0]
                    main_distance = distances[0]
                    
                    # Only play if fingers are close enough (volume control)
                    if main_distance < 0.1 and current_time - last_play_time > 0.3:
                        theremin.play_beep(main_freq, 300)
                        last_play_time = current_time
            else:
                # No hands detected
                theremin.stop_tone()
            
            # Draw theremin interface
            image = draw_theremin_interface(image, theremin, hand_positions, frequencies)
            
            # Draw volume bars
            image = draw_volume_bars(image, distances)
            
            # Draw instructions
            image = draw_instructions(image)
            
            # Show the image
            cv2.imshow('Virtual Theremin', image)
            
            # Handle key presses
            key = cv2.waitKey(10) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                theremin.stop_tone()
                print("Sound stopped")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    finally:
        theremin.stop_tone()
        cap.release()
        cv2.destroyAllWindows()
        hands.close()

if __name__ == "__main__":
    main()