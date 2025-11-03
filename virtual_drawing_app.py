import cv2
import numpy as np
import mediapipe as mp
from datetime import datetime
import os

class VirtualDrawingApp:
    def __init__(self):
        # Initialize MediaPipe Hand Detection
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.85,
            min_tracking_confidence=0.75
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Canvas setup
        self.canvas = None
        self.canvas_width = 640
        self.canvas_height = 480
        
        # Drawing parameters
        self.prev_x, self.prev_y = 0, 0
        self.drawing_color = (0, 0, 255)  # Red color (BGR)
        self.brush_thickness = 8
        self.eraser_thickness = 80
        
        # Application state
        self.camera_active = False
        self.cap = None
        self.show_download_button = False
        
    def is_index_finger_up(self, hand_landmarks):
        """Check if only index finger is up (drawing mode)"""
        # Get landmark positions
        landmarks = hand_landmarks.landmark
        
        # Index finger tip and PIP
        index_tip = landmarks[8].y
        index_pip = landmarks[6].y
        
        # Other fingers
        middle_tip = landmarks[12].y
        middle_pip = landmarks[10].y
        ring_tip = landmarks[16].y
        ring_pip = landmarks[14].y
        pinky_tip = landmarks[20].y
        pinky_pip = landmarks[18].y
        
        # Thumb
        thumb_tip = landmarks[4].x
        thumb_mcp = landmarks[2].x
        
        # Check if index is up and others are down
        index_up = index_tip < index_pip
        middle_down = middle_tip > middle_pip
        ring_down = ring_tip > ring_pip
        pinky_down = pinky_tip > pinky_pip
        
        return index_up and middle_down and ring_down and pinky_down
    
    def is_fist(self, hand_landmarks):
        """Check if hand is in fist position (eraser mode)"""
        landmarks = hand_landmarks.landmark
        
        # Check if all fingertips are below their PIP joints
        index_down = landmarks[8].y > landmarks[6].y
        middle_down = landmarks[12].y > landmarks[10].y
        ring_down = landmarks[16].y > landmarks[14].y
        pinky_down = landmarks[20].y > landmarks[18].y
        
        return index_down and middle_down and ring_down and pinky_down
    
    def is_thumbs_up(self, hand_landmarks):
        """Check if hand is showing thumbs up (stop camera)"""
        landmarks = hand_landmarks.landmark
        
        # Thumb tip should be above thumb IP
        thumb_up = landmarks[4].y < landmarks[3].y
        
        # Other fingers should be down (curled)
        index_down = landmarks[8].y > landmarks[6].y
        middle_down = landmarks[12].y > landmarks[10].y
        ring_down = landmarks[16].y > landmarks[14].y
        pinky_down = landmarks[20].y > landmarks[18].y
        
        return thumb_up and index_down and middle_down and ring_down and pinky_down
    
    def is_middle_finger_up(self, hand_landmarks):
        """Check if only middle finger is up (clear screen)"""
        landmarks = hand_landmarks.landmark
        
        # Middle finger tip and PIP
        middle_tip = landmarks[12].y
        middle_pip = landmarks[10].y
        
        # Other fingers
        index_tip = landmarks[8].y
        index_pip = landmarks[6].y
        ring_tip = landmarks[16].y
        ring_pip = landmarks[14].y
        pinky_tip = landmarks[20].y
        pinky_pip = landmarks[18].y
        
        # Check if middle is up and others are down
        middle_up = middle_tip < middle_pip
        index_down = index_tip > index_pip
        ring_down = ring_tip > ring_pip
        pinky_down = pinky_tip > pinky_pip
        
        return middle_up and index_down and ring_down and pinky_down
    
    def draw_button(self, img, text, position, size=(200, 60), color=(100, 100, 100)):
        """Draw a button on the image"""
        x, y = position
        w, h = size
        
        # Draw button rectangle
        cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 2)
        
        # Draw text
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font, 0.7, 2)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(img, text, (text_x, text_y), font, 0.7, (255, 255, 255), 2)
        
        return (x, y, x + w, y + h)
    
    def is_point_in_button(self, x, y, button_coords):
        """Check if point is inside button"""
        x1, y1, x2, y2 = button_coords
        return x1 <= x <= x2 and y1 <= y <= y2
    
    def process_hand_gestures(self, frame):
        """Process hand gestures and perform actions"""
        # Convert frame to RGB for MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        
        gesture_text = "No hand detected"
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on frame
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
                
                # Get index finger tip position
                h, w, c = frame.shape
                index_tip = hand_landmarks.landmark[8]
                x, y = int(index_tip.x * self.canvas_width), int(index_tip.y * self.canvas_height)
                
                # Check gestures
                if self.is_middle_finger_up(hand_landmarks):
                    gesture_text = "Clear Screen!"
                    # Clear the entire canvas
                    self.canvas = np.ones((self.canvas_height, self.canvas_width, 3), dtype=np.uint8) * 255
                    self.prev_x, self.prev_y = 0, 0
                    
                    # Show middle finger indicator on camera
                    middle_tip = hand_landmarks.landmark[12]
                    cv2.circle(frame, (int(middle_tip.x * w), int(middle_tip.y * h)),
                             15, (0, 0, 255), -1)
                
                elif self.is_index_finger_up(hand_landmarks):
                    gesture_text = "Drawing Mode"
                    # Draw on canvas
                    if self.prev_x == 0 and self.prev_y == 0:
                        self.prev_x, self.prev_y = x, y
                    
                    cv2.line(self.canvas, (self.prev_x, self.prev_y), (x, y),
                            self.drawing_color, self.brush_thickness)
                    self.prev_x, self.prev_y = x, y
                    
                    # Show drawing point on camera
                    cv2.circle(frame, (int(index_tip.x * w), int(index_tip.y * h)),
                             10, (0, 255, 0), -1)
                
                elif self.is_fist(hand_landmarks):
                    gesture_text = "Eraser Mode"
                    # Erase on canvas
                    if self.prev_x == 0 and self.prev_y == 0:
                        self.prev_x, self.prev_y = x, y
                    
                    cv2.line(self.canvas, (self.prev_x, self.prev_y), (x, y),
                            (255, 255, 255), self.eraser_thickness)
                    self.prev_x, self.prev_y = x, y
                    
                    # Show eraser point on camera
                    cv2.circle(frame, (int(index_tip.x * w), int(index_tip.y * h)),
                             20, (255, 0, 0), 2)
                
                else:
                    gesture_text = "Unknown Gesture"
                    self.prev_x, self.prev_y = 0, 0
        else:
            self.prev_x, self.prev_y = 0, 0
        
        # Display gesture text
        cv2.putText(frame, gesture_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                   1, (0, 255, 0), 2)
        
        return frame, gesture_text, False
    
    def start_camera(self):
        """Initialize camera and canvas"""
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        # Create white canvas
        self.canvas = np.ones((self.canvas_height, self.canvas_width, 3), dtype=np.uint8) * 255
        
        self.camera_active = True
        self.show_download_button = False
        self.prev_x, self.prev_y = 0, 0
        
        print("Camera started! Use gestures to draw:")
        print("- Index finger up: Draw")
        print("- Middle finger up: Clear entire screen")
        print("- Fist: Erase")
        print("- Press 'S' key to save drawing")
        print("- Press ESC key to exit")
    
    def stop_camera(self):
        """Stop camera and show download button"""
        if self.cap:
            self.cap.release()
        self.camera_active = False
        self.show_download_button = True
        cv2.destroyWindow('Camera Feed')
    
    def save_canvas(self):
        """Save canvas as JPEG image"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"drawing_{timestamp}.jpg"
        
        # Create drawings folder if it doesn't exist
        if not os.path.exists('drawings'):
            os.makedirs('drawings')
        
        filepath = os.path.join('drawings', filename)
        cv2.imwrite(filepath, self.canvas)
        print(f"Drawing saved as: {filepath}")
        return filepath
    
    def run(self):
        """Main application loop"""
        # Create main window with Draw button
        main_window = np.ones((200, 400, 3), dtype=np.uint8) * 50
        
        while True:
            if not self.camera_active and not self.show_download_button:
                # Show Draw button
                display = main_window.copy()
                draw_btn_coords = self.draw_button(display, "Draw", (100, 70))
                cv2.imshow('Virtual Drawing App', display)
                
                # Mouse callback for Draw button
                def mouse_callback(event, x, y, flags, param):
                    if event == cv2.EVENT_LBUTTONDOWN:
                        if self.is_point_in_button(x, y, draw_btn_coords):
                            self.start_camera()
                
                cv2.setMouseCallback('Virtual Drawing App', mouse_callback)
                
            elif self.camera_active:
                # Camera and drawing mode
                ret, frame = self.cap.read()
                if not ret:
                    print("Failed to grab frame")
                    break
                
                frame = cv2.flip(frame, 1)  # Mirror the frame
                
                # Process hand gestures
                frame, gesture_text, should_stop = self.process_hand_gestures(frame)
                
                # Display camera and canvas side by side
                combined = np.hstack((frame, self.canvas))
                
                # Add instructions overlay
                cv2.putText(combined, "Press 'S' to Save | ESC to Exit", 
                           (10, combined.shape[0] - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                cv2.imshow('Camera Feed & Drawing Canvas', combined)
                
            elif self.show_download_button:
                # Show canvas with Download button
                display = self.canvas.copy()
                download_btn_coords = self.draw_button(
                    display, "Download JPEG", (220, 400), color=(0, 150, 0)
                )
                cv2.imshow('Drawing Canvas - Click to Download', display)
                
                # Mouse callback for Download button
                def download_callback(event, x, y, flags, param):
                    if event == cv2.EVENT_LBUTTONDOWN:
                        if self.is_point_in_button(x, y, download_btn_coords):
                            filepath = self.save_canvas()
                            # Reset to main menu
                            self.show_download_button = False
                            cv2.destroyWindow('Drawing Canvas - Click to Download')
                
                cv2.setMouseCallback('Drawing Canvas - Click to Download', download_callback)
            
            # Check for ESC key to exit
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC key
                break
            elif key == ord('s') or key == ord('S'):  # S key to save
                if self.camera_active and self.canvas is not None:
                    filepath = self.save_canvas()
                    print(f"Drawing saved! Press ESC to exit or continue drawing.")
        
        # Cleanup
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = VirtualDrawingApp()
    app.run()
