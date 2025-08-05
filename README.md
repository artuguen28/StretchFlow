# StrechFlow
StretchFlow is a real-time pose analysis system that detects and tracks stretching movements using MediaPipe and OpenCV. Designed for fitness, wellness, and ergonomic use cases, StretchFlow provides immediate visual feedback to help users perform stretches correctly and safely.

## Instalation

### Option 1: Local Setup with Conda

#### 1. Create and Activate Conda

```bash
conda create -n stretchflow python=3.11 -y
conda activate stretchflow
```

Navigate to the project directory (where the `requirements.txt` is located) and install the dependencies:

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### 3. Run the App (with optional timer)
```bash
python main.py --timer 10
```
🕒 Use the --timer flag to define the number of seconds each stretch should be held. Default is 9 seconds if not provided.


## How to use StretchFlow

StretchFlow is an interactive stretch assistant that uses your webcam to guide and monitor your posture during a short set of upper-body stretching exercises. Follow the steps below to get started.

### ✅ Getting Started

1. Ensure your webcam is connected and facing you.
2. Launch the application — a window will appear with the title "StretchFlow".
3. On the home screen, raise your index finger and point it at the green Start button to begin the session.
4. Align your upper body with the reference image shown on the screen.
5. Once you're correctly positioned, the app will count down and begin the exercise sequence.

### 💪 Exercise Sequence
StretchFlow will guide you through the following exercises:

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

### 🏁 Completing the Session
Once all exercises are completed, you'll see a "Session Complete!" message.

To return to the home screen, raise your index finger and point it at the Home button.

### 💡 Tips
- Wear comfortable clothes that allow free movement.
- Keep your upper body fully visible in the camera frame.
- Perform movements slowly and with control.
- If the app doesn’t detect your pose, adjust your position or lighting.



## 🎉 Enjoy your stretch session and keep your body moving! Your well-being starts with small steps. 💪








