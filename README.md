# StrechVision - Real-time micro-stretch guidance with computer vision
StretchVision is a real-time pose analysis system that detects and tracks stretching movements using MediaPipe and OpenCV. Designed for fitness, wellness, and ergonomic use cases, StretchVision provides immediate visual feedback to help users perform stretches correctly and safely.

## Features  
- **Real-Time Pose Detection**: Tracks your posture live using MediaPipe's landmark-based model  
- **Webcam-Powered Interaction**: Control the interface with intuitive hand gestures — no mouse or keyboard needed  
- **Guided Stretching Sessions**: Follow along with step-by-step upper-body stretch routines  
- **Custom Timer**: Set how long each stretch should be held with the --timer flag  
- **Posture Feedback**: Align yourself with visual pose overlays for proper form  
- **Reference Visuals**: On-screen guidance helps you mirror each stretch correctly  
- **Camera View Integration**: See yourself on-screen while stretching for better self-correction  
- **Modular Architecture**: Designed with SOLID principles for easy extensibility  
- **Lightweight & Offline**: Runs entirely on your local machine — no internet required  

## Tech Stack
- **Language**: Python 3.11  
- **Framework**: Pygame (GUI & interaction)  
- **Computer Vision**: OpenCV  
- **Pose Estimation**: MediaPipe  
- **Timers & Scheduling**: Python time module  
- **Architecture**: Follows SOLID principles & modular design  
- **CLI Interface**: argparse for runtime flags  
- **Data Persistence**: In-memory (real-time processing, no external DB)  
- **Dependencies**: Managed via requirements.txt  
- **Environment Management**: Conda  

## Instalation

### Option 1: Local Setup with Conda

#### 1. Create and Activate Conda

```bash
conda create -n stretchvision python=3.11 -y
conda activate stretchvision
```

Navigate to the project directory (where the `requirements.txt` is located) and install the dependencies:

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### 3. Run the App (with optional timer)
```bash
python stretchvision.py --timer 10
```
🕒 Use the --timer flag to define the number of seconds each stretch should be held. Default is 9 seconds if not provided.


## How to use StretchVision

StretchVision is an interactive stretch assistant that uses your webcam to guide and monitor your posture during a short set of upper-body stretching exercises. Follow the steps below to get started.

<!-- ![Start Screen](media/start_screen.png) -->

### ✅ Getting Started

1. Ensure your webcam is connected and facing you.
2. Launch the application — a window will appear with the title "StretchVision".
3. On the home screen, raise your index finger and point it at the green Start button to begin the session.
4. Align your upper body with the reference image shown on the screen.
5. Once you're correctly positioned, the app will count down and begin the exercise sequence.

### 💪 Exercise Sequence
StretchVision will guide you through the following exercises:

**Left Bend Stretch**  
Instruction: Lean your upper body to the left side.  
Goal: Stretch your right-side torso.  
Cue: "Lean your upper body to the left side."  

**Right Bend Stretch**  
Instruction: Lean your upper body to the right side.  
Goal: Stretch your left-side torso.  
Cue: "Lean your upper body to the right side."  

**Left Cross-Body Arm Stretch**  
Instruction: Bring your left arm across your chest and hold it with your right hand.  
Goal: Stretch the left shoulder and upper back.  
Cue: "Bring your left arm across your chest and hold it with your right hand."  

**Right Cross-Body Arm Stretch**  
Instruction: Bring your right arm across your chest and hold it with your left hand.  
Goal: Stretch the right shoulder and upper back.  
Cue: "Bring your right arm across your chest and hold it with your left hand."  

**Left Neck Tilt Stretch**  
Instruction: Gently tilt your head to the left, toward your left shoulder.  
Goal: Stretch the right side of your neck.  
Cue: "Gently tilt your head toward your left shoulder."  

**Right Neck Tilt Stretch**  
Instruction: Gently tilt your head to the right, toward your right shoulder.  
Goal: Stretch the left side of your neck.  
Cue: "Gently tilt your head toward your right shoulder."  

### Exercise Screen

<!-- ![Exercise Screen](media/exercise_screen.png) -->

### 🏁 Completing the Session
Once all exercises are completed, you'll see a "Session Complete!" message.

To return to the home screen, raise your index finger and point it at the Home button.

### 💡 Tips
- Wear comfortable clothes that allow free movement.
- Keep your upper body fully visible in the camera frame.
- Perform movements slowly and with control.
- If the app doesn’t detect your pose, adjust your position or lighting.



## 🧠 How MediaPipe Tracks Your Movements

<!-- ![MediaPipe Landmark Demo](media/landmarks_demo.gif) -->

> The animated image above illustrates how StretchVision leverages MediaPipe’s pose estimation to detect and track key body landmarks in real time, enabling accurate posture recognition and feedback throughout each stretching exercise.


## 🎉 Enjoy your stretch session and keep your body moving! Your well-being starts with small steps. 💪

