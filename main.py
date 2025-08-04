import time
import cv2
import mediapipe as mp
import pygame

from app.stretch_detector import PoseDetectors, StretchExercise
from utils.config import SCREEN_WIDTH, SCREEN_HEIGHT, colors
from utils.ui_scaler import UIScaler
from utils.ui_renderer import UIRenderer

# Initialize pygame
pygame.init()

# Set up the display
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

WINDOW_WIDTH = int(screen_width * 0.5)
WINDOW_HEIGHT = int(screen_height * 0.666)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Load resources
upper_body_layourt = pygame.image.load("./resources/assets/upper_body_layout.png").convert_alpha()

# Set the window title
pygame.display.set_caption("StretchFlow")

# Initialize scaler and renderer
scaler = UIScaler(SCREEN_WIDTH, SCREEN_HEIGHT)
renderer = UIRenderer(screen, scaler)

# Fonts
title_font = pygame.font.Font(None, scaler.font(150))
warning_font = pygame.font.Font(None, scaler.font(70))
button_font = pygame.font.Font(None, scaler.font(100))
countdown_font = pygame.font.Font(None, scaler.font(200))

# Text Surfaces
title_surface = title_font.render("StretchFlow", True, colors["WHITE"])
start_button_text = button_font.render("START", True, colors["GREEN"])
home_button_text = button_font.render("HOME", True, colors["WHITE"])

# UI Rects
title_rect = pygame.Rect(scaler.x(SCREEN_WIDTH // 2 - 350), scaler.y(80), scaler.x(700), scaler.y(130))
start_button_rect = pygame.Rect(scaler.x(SCREEN_WIDTH // 2 - 150), scaler.y(SCREEN_HEIGHT // 2), scaler.x(300), scaler.y(100))
home_button_rect = pygame.Rect(scaler.x(SCREEN_WIDTH // 2 - 150), scaler.y(SCREEN_HEIGHT // 2 + 300), scaler.x(300), scaler.y(100))

# MediaPipe setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

# State variables
stretch_detection_started = False
stretch_screen_active = False
countdown_start_time = None

# Exercise list
exercises = [
    StretchExercise(
        name="Left Bend Stretch",
        detect_func=PoseDetectors.detect_bend_to_left,
        prompt_msg="Lean your upper body to the left side.",
        success_msg="Nice stretch to the left!"
    ),
    StretchExercise(
        name="Right Bend Stretch",
        detect_func=PoseDetectors.detect_bend_to_right,
        prompt_msg="Lean your upper body to the right side.",
        success_msg="Well done on that right bend!"
    ),
    StretchExercise(
        name="Left Cross-Body Arm Stretch",
        detect_func=PoseDetectors.detect_left_shoulder_extension,
        prompt_msg="Bring your left arm across your chest and hold it with your right hand.",
        success_msg="Great stretch!"
    ),
    StretchExercise(
        name="Right Cross-Body Arm Stretch",
        detect_func=PoseDetectors.detect_right_shoulder_extension,
        prompt_msg="Bring your right arm across your chest and hold it with your left hand.",
        success_msg="Awesome work!"
    ),
    StretchExercise(
        name="Left Neck Tilt Stretch",
        detect_func=PoseDetectors.detect_neck_tilt_left,
        prompt_msg="Gently tilt your head toward your left shoulder.",
        success_msg="Good job relaxing that neck!"
    ),
    StretchExercise(
        name="Right Neck Tilt Stretch",
        detect_func=PoseDetectors.detect_neck_tilt_right,
        prompt_msg="Gently tilt your head toward your right shoulder.",
        success_msg="Neck stretch complete!"
    )
]

current_exercise_index = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    pygame_frame = pygame.surfarray.make_surface(frame)
    pygame_frame = pygame.transform.rotate(pygame_frame, -90)
    screen.blit(pygame_frame, (0, 0))

    results = pose.process(frame)

    if stretch_detection_started:
        if stretch_screen_active:
            if results.pose_landmarks and current_exercise_index < len(exercises):
                current_exercise = exercises[current_exercise_index]
                finished = current_exercise.update(
                    results.pose_landmarks,
                    mp_pose,
                    renderer,
                    warning_font,
                    countdown_font,
                    colors
                )
                if finished:
                    current_exercise_index += 1
            elif current_exercise_index >= len(exercises):
                renderer.render_warning_message("Session Complete!", colors["BLACK"], warning_font, colors["GREEN"])

                hand_results = hands.process(frame)
                if hand_results.multi_hand_landmarks:
                    for hand_landmarks in hand_results.multi_hand_landmarks:
                        index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        x, y = int(index_finger_tip.x * SCREEN_WIDTH), int(index_finger_tip.y * SCREEN_HEIGHT)
                        if home_button_rect.collidepoint(x, y):
                            stretch_detection_started = False
                            stretch_screen_active = False
                            current_exercise_index = 0
                            countdown_start_time = None
                else:
                    renderer.render_warning_message("Use your index finger to go home!", colors["WHITE"], warning_font, colors["BLUE"])

                pygame.draw.rect(screen, colors["BLUE"], home_button_rect, border_radius=15)
                screen.blit(home_button_text, (
                    home_button_rect.x + home_button_rect.width // 2 - home_button_text.get_width() // 2,
                    home_button_rect.y + home_button_text.get_height() // 4,
                ))
        else:
            if results.pose_landmarks:
                upper_body_detected = PoseDetectors.detect_upper_body(results.pose_landmarks, mp_pose)

                if upper_body_detected:
                    if not countdown_start_time:
                        countdown_start_time = pygame.time.get_ticks()

                    elapsed_time = pygame.time.get_ticks() - countdown_start_time

                    if elapsed_time < 2000:
                        renderer.render_warning_message("Good Job! Let's start your stretch session!", colors["BLACK"], warning_font, colors["GREEN"])
                    else:
                        countdown_value = 3 - (elapsed_time - 2000) // 1000
                        if countdown_value > 0:
                            renderer.render_centered_text(str(countdown_value), colors["WHITE"], countdown_font)
                        else:
                            countdown_start_time = None
                            stretch_screen_active = True
                else:
                    renderer.render_warning_message("Align your upper body like the image!", colors["WHITE"], warning_font, colors["BLUE"])
                    renderer.render_image(upper_body_layourt, position="center", scale=1)
    else:
        hand_results = hands.process(frame)
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x, y = int(index_finger_tip.x * SCREEN_WIDTH), int(index_finger_tip.y * SCREEN_HEIGHT)
                if start_button_rect.collidepoint(x, y):
                    stretch_detection_started = True
        else:
            renderer.render_home_warning_message("Use your index finger to touch the button!", colors["WHITE"], warning_font, colors["BLUE"])

        # Draw title and button
        pygame.draw.rect(screen, colors["BLACK"], title_rect, border_radius=15)
        screen.blit(title_surface, (
            SCREEN_WIDTH // 2 - title_surface.get_width() // 2,
            scaler.y(100)
        ))

        pygame.draw.rect(screen, colors["WHITE"], start_button_rect, border_radius=10)
        screen.blit(start_button_text, (
            start_button_rect.x + start_button_rect.width // 2 - start_button_text.get_width() // 2,
            start_button_rect.y + start_button_text.get_height() // 4,
        ))

    pygame.display.flip()

cap.release()
pygame.quit()
