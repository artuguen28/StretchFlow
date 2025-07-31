import cv2
import mediapipe as mp
import pygame
from app.strech_detector import detect_stretch, plot_landmarks
from utils.config import SCREEN_WIDTH, SCREEN_HEIGHT, colors
import time  # Add this import for the countdown

# Initialize pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("StretchFlow")

# Fonts and colors
title_font = pygame.font.Font(None, 150)
warning_font = pygame.font.Font(None, 90)
button_font = pygame.font.Font(None, 50)
countdown_font = pygame.font.Font(None, 200)  # Adjust the size as needed


title_surface = title_font.render("StretchFlow", True, colors["WHITE"])
start_button_text = button_font.render("Start", True, colors["BLACK"])
# exit_button_text = button_font.render("X", True, colors["BLACK"])

# Button dimensions
start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 60)
# exit_button_rect = pygame.Rect(SCREEN_WIDTH - 300, 100, 200, 60)


# Initialize OpenCV
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()


cap = cv2.VideoCapture(0)

# Game state
running = True
detection_started = False
countdown_start_time = None  # Initialize the countdown start time

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
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert the frame to RGB for pygame and display it once
    pygame_frame = pygame.surfarray.make_surface(frame)
    pygame_frame = pygame.transform.rotate(pygame_frame, -90)
    screen.blit(pygame_frame, (0, 0))


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
                if start_button_rect.collidepoint(x, y):
                    detection_started = True

                # if exit_button_rect.collidepoint(x, y):
                #     running = False

        else:
            print("No hand landmarks detected.")
            # Display a message on the screen
            message_surface = warning_font.render(
                "Use your index finger to start!", True, colors["BLUE"]
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

        # Display start button
        pygame.draw.rect(screen, colors["GREEN"], start_button_rect)
        screen.blit(
            start_button_text,
            (
                start_button_rect.x + start_button_rect.width // 2 - start_button_text.get_width() // 2,
                start_button_rect.y + start_button_rect.height // 2 - start_button_text.get_height() // 2,
            ),
        )

        # # Display exit button
        # pygame.draw.rect(screen, colors["RED"], exit_button_rect)
        # screen.blit(
        #     exit_button_text,
        #     (
        #         exit_button_rect.x + exit_button_rect.width // 2 - exit_button_text.get_width() // 2,
        #         exit_button_rect.y + exit_button_rect.height // 2 - exit_button_text.get_height() // 2,
        #     ),
        # )

    # Perform stretch detection if started
    if detection_started:
        results = pose.process(frame)

        # Check for upper body detection
        upper_body_detected = detect_upper_body(results)

        # Only plot landmarks if they exist
        if results.pose_landmarks:
            plot_landmarks(frame, results.pose_landmarks)

        if upper_body_detected:
            if not countdown_start_time:
                countdown_start_time = pygame.time.get_ticks()  # Record the start time

            elapsed_time = pygame.time.get_ticks() - countdown_start_time

            if elapsed_time < 2000:  # Display the message for 2 seconds
                message_surface = warning_font.render(
                    "Good Job! Let's start your stretch session!", True, colors["GREEN"]
                )
                screen.blit(
                    message_surface,
                    (SCREEN_WIDTH // 2 - message_surface.get_width() // 2, 100),
                )
            else:
                # Start the countdown
                countdown_value = 3 - (elapsed_time - 2000) // 1000
                if countdown_value > 0:
                    countdown_surface = countdown_font.render(str(countdown_value), True, colors["WHITE"])
                    screen.blit(
                        countdown_surface,
                        (SCREEN_WIDTH // 2 - countdown_surface.get_width() // 2, SCREEN_HEIGHT // 2),
                    )
                else:
                    print("Starting stretch session!")
                    detection_started = False  # Reset detection if needed
                    countdown_start_time = None  # Reset the timer
        else:
            print("Upper body landmarks not detected!")
            # Display a message on the screen
            message_surface = warning_font.render(
                "Place your upper body in the correct position!", True, colors["BLUE"]
            )
            screen.blit(
                message_surface,
                (SCREEN_WIDTH // 2 - message_surface.get_width() // 2, 100),
            )

    pygame.display.flip()

cap.release()
pygame.quit()