import cv2
import mediapipe as mp

def detect_test_stretch(landmarks):
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
        return True
    else:
        return False
        

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


def detect_bend_to_right(landmarks, mp_pose):
    """Detects if the body is bending to the right based on pose landmarks.
    Args:
        landmarks: Pose landmarks from MediaPipe.
        mp_pose: MediaPipe pose module for accessing landmark indices.
    Returns:
        bool: True if the body is bending to the right, False otherwise.
    """
    if not landmarks:
        return False

    lm = landmarks.landmark

    # Get key landmarks for shoulders, hips, and knees
    left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_hip = lm[mp_pose.PoseLandmark.LEFT_HIP]
    left_wrist = lm[mp_pose.PoseLandmark.LEFT_WRIST]
    nose = lm[mp_pose.PoseLandmark.NOSE]


    # Check if the right side landmarks are consistently more to the right (lower x value)
    if (
        left_shoulder.x < left_hip.x and 
        left_wrist.x < right_shoulder.x and 
        left_wrist.y < nose.y
    ):
        return True
    return False

def detect_bend_to_left(landmarks, mp_pose):
    """Detects if the body is bending to the left based on pose landmarks.
    Args:
        landmarks: Pose landmarks from MediaPipe.
        mp_pose: MediaPipe pose module for accessing landmark indices.
    Returns:
        bool: True if the body is bending to the left, False otherwise.
    """
    if not landmarks:
        return False

    lm = landmarks.landmark

    # Get key landmarks for shoulders, hips, and knees
    left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    right_hip = lm[mp_pose.PoseLandmark.RIGHT_HIP]
    right_wrist = lm[mp_pose.PoseLandmark.RIGHT_WRIST]
    nose = lm[mp_pose.PoseLandmark.NOSE]

    # Check if the left side landmarks are consistently more to the left (higher x value)
    if (
        right_shoulder.x > right_hip.x and 
        right_wrist.x > left_shoulder.x  and 
        right_wrist.y < nose.y
    ):
        return True
    return False
