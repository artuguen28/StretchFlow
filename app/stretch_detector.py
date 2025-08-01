
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

def detect_right_shoulder_extension(landmarks, mp_pose):
    """Detects if the right shoulder is correctly extended based on pose landmarks.
    Args:
        landmarks: Pose landmarks from MediaPipe.
        mp_pose: MediaPipe pose module for accessing landmark indices.
    Returns:
        bool: True if the right shoulder is correctly extended, False otherwise.
    """
    if not landmarks:
        return False

    lm = landmarks.landmark

    # Get key landmarks for shoulders, hips, and knees
    left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
    right_elbow = lm[mp_pose.PoseLandmark.RIGHT_ELBOW]
    left_wrist = lm[mp_pose.PoseLandmark.LEFT_WRIST]

    elbow_l_shoulder_dist = (((right_elbow.x - left_shoulder.x) ** 2) + ((right_elbow.y - left_shoulder.y) ** 2) ** 0.5)
    l_wirst_l_shoulder_dist = (((left_wrist.x - left_shoulder.x) ** 2) + ((left_wrist.y - left_shoulder.y) ** 2) ** 0.5)

    print(f"Elbow to shoulder: {elbow_l_shoulder_dist}")
    print(f"Wrist to shoulder: {l_wirst_l_shoulder_dist}")

    # Check if the left side landmarks are consistently more to the left (higher x value)
    if (
        elbow_l_shoulder_dist < 0.15 and l_wirst_l_shoulder_dist < 0.15
    ):
        return True
    return False

def detect_left_shoulder_extension(landmarks, mp_pose):
    """Detects if the left shoulder is correctly extended based on pose landmarks.
    Args:
        landmarks: Pose landmarks from MediaPipe.
        mp_pose: MediaPipe pose module for accessing landmark indices.
    Returns:
        bool: True if the left shoulder is correctly extended, False otherwise.
    """
    if not landmarks:
        return False

    lm = landmarks.landmark

    # Get key landmarks for shoulders, hips, and knees
    right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    left_elbow = lm[mp_pose.PoseLandmark.RIGHT_ELBOW]
    right_wrist = lm[mp_pose.PoseLandmark.LEFT_WRIST]

    elbow_r_shoulder_dist = (((left_elbow.x - right_shoulder.x) ** 2) + ((left_elbow.y - right_shoulder.y) ** 2)) ** 0.5
    r_wirst_r_shoulder_dist = (((right_wrist.x - right_shoulder.x) ** 2) + ((right_wrist.y - right_shoulder.y) ** 2)) ** 0.5

    print(f"Elbow to shoulder: {elbow_r_shoulder_dist}")
    print(f"Wrist to shoulder: {r_wirst_r_shoulder_dist}")
    
    if (
        elbow_r_shoulder_dist < 0.15 and r_wirst_r_shoulder_dist < 0.15
    ):
        return True
    return False