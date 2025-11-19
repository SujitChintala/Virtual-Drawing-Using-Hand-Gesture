# Virtual Drawing Application with Hand Gesture Recognition

A real-time virtual drawing application that uses your webcam and hand gestures to draw on a digital canvas. Control the application entirely with hand gestures - no mouse or keyboard needed!

## 🎨 Features

- **Camera-based Drawing**: Use your webcam to detect hand gestures in real-time
- **Gesture Recognition**: Three intuitive hand gestures for drawing:
  - ✏️ **Index Finger Up**: Drawing mode - draw on the canvas
  - 🖕 **Middle Finger Up**: Clear entire canvas instantly
  - 🧽 **Clenched Fist**: Eraser mode - erase your drawings
- **Side-by-Side Display**: See your camera feed and drawing canvas simultaneously
- **Save Drawings**: Press 'S' key to save your artwork as JPEG images with timestamps
- **Clean Interface**: Simple button-based interface with visual feedback
- **Manual Control**: Exit when you want with ESC key

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Webcam/Camera connected to your computer
- Windows, macOS, or Linux operating system

### Installation

1. **Clone the repository** (or download the files):
   ```bash
   git clone https://github.com/SujitChintala/Diabetes-Prediction.git
   cd Diabetes-Prediction
   ```

2. **Create a new environment and activate it**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

   The application requires:
   - `opencv-python` - For camera capture and image processing
   - `mediapipe` - For hand detection and gesture recognition
   - `numpy` - For numerical operations and array handling

### Running the Application

1. **Start the application**:
   ```bash
   python virtual_drawing_app.py
   ```

2. **Initial Screen**: A window will appear with a "Draw" button

3. **Click the Draw button** to start the camera and begin drawing

## 📖 How to Use

### Step-by-Step Guide

#### 1. Launch the Application
- Run the script using `python virtual_drawing_app.py`
- You'll see a window with a "Draw" button

#### 2. Start Drawing
- Click the **"Draw"** button
- Your camera will activate, and you'll see two panels:
  - **Left panel**: Live camera feed with hand tracking
  - **Right panel**: White canvas where your drawings appear

#### 3. Drawing Gestures

**✏️ Drawing Mode - Index Finger Up**
- Extend only your index finger (other fingers closed)
- Move your finger to draw on the canvas
- A green circle will appear on your fingertip in the camera view
- Red lines will appear on the canvas following your finger movement

**🖕 Clear Screen - Middle Finger Up**
- Extend only your middle finger (other fingers closed)
- The entire canvas will be cleared to white
- A red circle will appear on your middle fingertip in the camera view
- Perfect for starting fresh without exiting

**🧽 Eraser Mode - Clenched Fist**
- Make a fist with all fingers closed
- Move your fist to erase parts of your drawing
- A blue circle outline will appear on your hand in the camera view
- The eraser is larger than the pen for easier correction

#### 4. Save Your Drawing
- While drawing, press the **'S' key** at any time to save your current drawing
- The image will be saved in a `drawings` folder with a timestamp filename
- Format: `drawing_YYYYMMDD_HHMMSS.jpg`
- You can continue drawing after saving

#### 5. Exit the Application
- Press the **ESC** key at any time to exit
- Or close the window using the X button

## 🎯 Gesture Recognition Guide

### Index Finger Up (Drawing)
```
     👆
```
- **What to do**: Extend only your index finger, keep other fingers closed
- **Action**: Draws red lines on the canvas
- **Tips**: Keep your hand steady for smooth lines

### Middle Finger Up (Clear Screen)
```
     🖕
```
- **What to do**: Extend only your middle finger, keep other fingers closed
- **Action**: Clears the entire canvas to white
- **Tips**: Use this to start over completely

### Clenched Fist (Eraser)
```
    ✊
```
- **What to do**: Close all fingers into a tight fist
- **Action**: Erases drawings with a larger brush
- **Tips**: Move slowly for precise erasing

### Keyboard Controls
- **'S' Key**: Save your current drawing as JPEG
- **ESC Key**: Exit the application

## 🛠️ Technical Details

### Architecture

The application is built using:
- **OpenCV**: Camera capture and image processing
- **MediaPipe**: Google's hand tracking solution for real-time gesture recognition
- **NumPy**: Array operations for canvas manipulation

### Key Components

1. **Hand Detection**: Uses MediaPipe Hands model with:
   - Single hand tracking for better performance
   - 70% detection confidence threshold
   - 50% tracking confidence threshold

2. **Gesture Classification**:
   - Analyzes 21 hand landmarks
   - Compares fingertip and joint positions
   - Determines finger states (up/down)

3. **Drawing Engine**:
   - Real-time canvas updates
   - Smooth line interpolation
   - Separate brush and eraser tools

### Customization Options

You can modify these parameters in the code:

```python
# Drawing parameters
self.drawing_color = (0, 0, 255)  # BGR color (Red by default)
self.brush_thickness = 8           # Drawing line thickness
self.eraser_thickness = 80         # Eraser size

# Canvas size
self.canvas_width = 640
self.canvas_height = 480

# Detection confidence
min_detection_confidence = 0.7       # Hand detection threshold
min_tracking_confidence = 0.6        # Hand tracking threshold
```

## 📁 File Structure

```
Diabetes_Prediction_Project/
├── virtual_drawing_app.py    # Main application file
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── drawings/                  # Created automatically
    └── drawing_*.jpg          # Your saved drawings
```

## 🐛 Troubleshooting

### Camera Not Opening
- **Issue**: Camera fails to start or shows black screen
- **Solution**: 
  - Check if another application is using the camera
  - Try changing camera index in code: `cv2.VideoCapture(1)` instead of `0`
  - Grant camera permissions in your OS settings

### Hand Not Detected
- **Issue**: Gestures not recognized
- **Solution**:
  - Ensure good lighting conditions
  - Keep your hand within camera view
  - Adjust detection confidence in code (lower the threshold)
  - Make sure your entire hand is visible

### Gestures Not Working Properly
- **Issue**: Wrong gesture detected or no gesture detected
- **Solution**:
  - Make gestures more pronounced and clear
  - Keep hand perpendicular to the camera
  - Ensure fingers are fully extended or fully closed
  - Avoid partial gestures

### Cannot Save Drawing
- **Issue**: Pressing 'S' doesn't save the drawing
- **Solution**:
  - Make sure the camera window is in focus (click on it)
  - Check file system permissions
  - Ensure enough disk space
  - Verify the `drawings` folder can be created

### Drawing is Laggy
- **Issue**: Slow performance or delayed drawing
- **Solution**:
  - Close other applications to free up CPU/RAM
  - Reduce camera resolution in code
  - Use a more powerful computer
  - Update your graphics drivers

## 💡 Tips for Best Results

1. **Lighting**: Use good lighting for better hand detection
2. **Background**: Plain backgrounds work better than cluttered ones
3. **Distance**: Keep your hand 1-2 feet from the camera
4. **Stability**: Rest your elbow on the desk for steadier drawing
5. **Practice**: Spend a few minutes getting familiar with the gestures
6. **Clean Gestures**: Make distinct, clear gestures for better recognition
7. **Save Often**: Press 'S' regularly to save your progress

## 🔮 Future Enhancements

Potential features for future versions:
- [ ] Color palette selection
- [ ] Multiple brush sizes
- [ ] Shape tools (circle, rectangle, line)
- [ ] Undo/Redo functionality
- [ ] Save/Load drawing sessions
- [ ] PNG format with transparency
- [ ] Two-hand gestures for advanced controls
- [ ] Drawing templates and backgrounds
- [ ] Text insertion capability

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation


## 🙏 Acknowledgments

- **MediaPipe**: Google's open-source framework for hand tracking
- **OpenCV**: Open-source computer vision library
- Built with Python 3.x


**Saai Sujit Chintala**
- GitHub: [SujitChintala](https://github.com/SujitChintala)
- LinkedIn: [Saai Sujit Chintala](https://www.linkedin.com/in/sujitchintala/)
- Email: sujitchintala@gmail.com

---

<div align="center">

**Enjoy drawing with your hands! 🎨✨**     
**⭐ Star this repository if you find it helpful! ⭐**

</div>