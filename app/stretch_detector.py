import cv2
import mediapipe as mp

def detect_stretch(landmarks, frame):
    """Detects specific stretches based on pose landmarks and annotates the frame.
    Args:
        landmarks: Pose landmarks from MediaPipe.
        frame: The current video frame to annotate.
    """
    # Example: basic arm stretch detection (left wrist close to right elbow)
    lm = landmarks.landmark
    left_wrist = lm[mp.solutions.pose.PoseLandmark.LEFT_WRIST]
    right_elbow = lm[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW]

    dx = left_wrist.x - right_elbow.x
    dy = left_wrist.y - right_elbow.y
    dist = (dx**2 + dy**2) ** 0.5

    if dist < 0.1:
        cv2.putText(frame, "Arm Stretch Detected!", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        

def detect_upper_body(landmarks, mp_pose):
    """Check if upper body landmarks are detected."""
    upper_body_landmarks = [
        mp_pose.PoseLandmark.LEFT_SHOULDER,
        mp_pose.PoseLandmark.RIGHT_SHOULDER,
        mp_pose.PoseLandmark.LEFT_ELBOW,
        mp_pose.PoseLandmark.RIGHT_ELBOW,
        mp_pose.PoseLandmark.LEFT_HIP,
        mp_pose.PoseLandmark.RIGHT_HIP,
    ]
    return all(
        landmarks.landmark[landmark].visibility > 0.5 for landmark in upper_body_landmarks
    ) if landmarks else False
        

def plot_landmarks(frame, landmarks):
    """Draws pose landmarks on the frame."""
    for lm in landmarks.landmark:
        h, w, _ = frame.shape
        cx, cy = int(lm.x * w), int(lm.y * h)
        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
