import cv2
import mediapipe as mp
import pygame
from app.strech_detector import detect_stretch, plot_landmarks
from utils.config import SCREEN_WIDTH, SCREEN_HEIGHT, colors

# Initialize pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("StretchFlow")

# Fonts and colors
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

title_surface = font.render("StretchFlow", True, colors["WHITE"])
button_text = button_font.render("Start", True, colors["BLACK"])

# Button dimensions
button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 60)

# Initialize OpenCV
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


cap = cv2.VideoCapture(0)

# Game state
running = True
detection_started = False

def detect_upper_body(results):
    if results.pose_landmarks is None:
        return False  # Return False if no pose landmarks are detected

    upper_body_landmarks = [
        mp_pose.PoseLandmark.LEFT_SHOULDER,
        mp_pose.PoseLandmark.RIGHT_SHOULDER,
        mp_pose.PoseLandmark.LEFT_ELBOW,
        mp_pose.PoseLandmark.RIGHT_ELBOW,
        mp_pose.PoseLandmark.LEFT_HIP,
        mp_pose.PoseLandmark.RIGHT_HIP,
    ]
    return all(
        results.pose_landmarks.landmark[landmark].visibility > 0.5
        for landmark in upper_body_landmarks
    )

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capture video frame
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to match the screen dimensions
    frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Convert the frame to RGB for MediaPipe
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert the frame to RGB for pygame and display it once
    pygame_frame = pygame.surfarray.make_surface(frame)
    pygame_frame = pygame.transform.rotate(pygame_frame, -90)
    screen.blit(pygame_frame, (0, 0))

    # Perform stretch detection if started
    if detection_started:
        results = pose.process(frame)

        # Check for upper body detection
        upper_body_detected = detect_upper_body(results)

        plot_landmarks(frame, results.pose_landmarks)
        
        if upper_body_detected:
            print("Upper body landmarks detected!")
            # Plot landmarks directly on the frame
        else:
            print("Upper body landmarks not detected!")
            # Display a message on the screen
            message_surface = font.render(
                "Upper body not detected!", True, colors["RED"]
            )
            screen.blit(
                message_surface,
                (SCREEN_WIDTH // 2 - message_surface.get_width() // 2, 100),
            )

    # Display title and button if detection has not started
    if not detection_started:
        hand_results = hands.process(frame)

        # Check for hand landmarks to interact with the button
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                # Get the coordinates of the index finger tip
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Convert normalized coordinates to screen coordinates
                x, y = int(index_finger_tip.x * SCREEN_WIDTH), int(index_finger_tip.y * SCREEN_HEIGHT)

                # Check if the index finger tip is over the button
                if button_rect.collidepoint(x, y):
                    detection_started = True

        else:
            print("No hand landmarks detected.")
            # Display a message on the screen
            message_surface = font.render(
                "No hand landmarks detected!", True, colors["RED"]
            )
            screen.blit(
                message_surface,
                (SCREEN_WIDTH // 2 - message_surface.get_width() // 2, 300),
            )

        # Display title
        screen.blit(
            title_surface,
            (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 100),
        )

        # Display button
        pygame.draw.rect(screen, colors["GREEN"], button_rect)
        screen.blit(
            button_text,
            (
                button_rect.x + button_rect.width // 2 - button_text.get_width() // 2,
                button_rect.y + button_rect.height // 2 - button_text.get_height() // 2,
            ),
        )

    pygame.display.flip()

cap.release()
pygame.quit()