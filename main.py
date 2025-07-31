import cv2
import mediapipe as mp
import pygame
from app.stretch_detector import detect_bend_to_left, detect_bend_to_right, detect_test_stretch, detect_upper_body
from utils.config import SCREEN_WIDTH, SCREEN_HEIGHT, colors
import time

from utils.renders import render_warning_message  # Add this import for the countdown

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
stretch_detection_started = False
countdown_start_time = None  # Initialize the countdown start time
stretch_screen_active = False  # New state to manage the stretch detection screen


# Initialize Pygame Mixer
# pygame.mixer.init()

# # Load sound files
# countdown_sound = pygame.mixer.Sound("./resources/audio/countdown-beep.mp3")  # Replace with your sound file path
# start_sound = pygame.mixer.Sound("./resources/audio/countdown-beep.mp3")  # Sound to play when the countdown ends

# upper_body_hint_img = pygame.image.load("./resources/graphics/body_layout.png")
# upper_body_hint_img = pygame.transform.scale(upper_body_hint_img, (400, 300))  # Resize as needed



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

    # Always process the frame for pose detection

    # Perform stretch detection if started
    if stretch_detection_started:

        results = pose.process(frame)

        if stretch_screen_active:
            # Call the stretch detection function as a new screen

            print("Stretch detection screen active")
            if results.pose_landmarks:
                print("Pose landmarks detected")
                if detect_bend_to_left(results.pose_landmarks, mp_pose):
                    print("Stretch detected!")

                    render_warning_message(
                        "Stretch Detected! Hold this position..", colors["GREEN"], screen, warning_font
                    )

                else:
                    print("No stretch detected.")

                    render_warning_message(
                        "Do the stretching!", colors["BLUE"], screen, warning_font
                    )

        else:
            # Check for upper body detection
            upper_body_detected = detect_upper_body(results.pose_landmarks, mp_pose)

            if upper_body_detected:
                if not countdown_start_time:
                    countdown_start_time = pygame.time.get_ticks()  # Record the start time

                elapsed_time = pygame.time.get_ticks() - countdown_start_time

                if elapsed_time < 2000:  # Display the message for 2 seconds

                    render_warning_message(
                        "Good Job! Let's start your stretch session!", colors["GREEN"], screen, warning_font
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
                        countdown_start_time = None  # Reset the timer
                        stretch_screen_active = True  # Activate the stretch detection screen
            else:
                print("Upper body landmarks not detected!")
                # Center the image
                # screen.blit(upper_body_hint_img, (
                #     SCREEN_WIDTH // 2 - upper_body_hint_img.get_width() // 2,
                #     SCREEN_HEIGHT // 2 - upper_body_hint_img.get_height() // 2
                # ))

                # Optional: Add a warning message under or above the image
                render_warning_message(
                    "Align your upper body like the image!", colors["BLUE"], screen, warning_font
                )

    # Display title and button if detection has not started
    if not stretch_detection_started:
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
                    stretch_detection_started = True

        else:
            print("No hand landmarks detected.")
            # Display a message on the screen

            render_warning_message(
                "Use your index finger to start!", colors["BLUE"], screen, warning_font
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

    pygame.display.flip()

cap.release()
pygame.quit()