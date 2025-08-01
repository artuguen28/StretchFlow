import cv2
import mediapipe as mp
import pygame
from app.stretch_detector import detect_bend_to_left, detect_bend_to_right, detect_right_shoulder_extension, detect_left_shoulder_extension, detect_upper_body
from utils.config import SCREEN_WIDTH, SCREEN_HEIGHT, colors
import time
from utils.renders import render_warning_message  # For countdown and messages

# Initialize pygame
pygame.init()

# Screen dimensions
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("StretchFlow")

# Fonts and colors
title_font = pygame.font.Font(None, 150)
warning_font = pygame.font.Font(None, 90)
button_font = pygame.font.Font(None, 50)
countdown_font = pygame.font.Font(None, 200)

title_surface = title_font.render("StretchFlow", True, colors["WHITE"])
start_button_text = button_font.render("Start", True, colors["BLACK"])
start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 60)

# Initialize OpenCV
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

test_stretch = True
running = True
countdown_start_time = None

stretch_detection_started = test_stretch
stretch_screen_active = test_stretch

stretch_exercise = 0
num_exercises = 2  # Total number of exercises
stretch_completed_flags = [False] * num_exercises

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

    if stretch_detection_started:
        results = pose.process(frame)

        if stretch_screen_active:
            if results.pose_landmarks:
                match stretch_exercise:
                    case 0:
                        if not stretch_completed_flags[0]:
                            if detect_bend_to_left(results.pose_landmarks, mp_pose):
                                if not countdown_start_time:
                                    countdown_start_time = pygame.time.get_ticks()

                                elapsed_time = pygame.time.get_ticks() - countdown_start_time

                                if elapsed_time < 1000:
                                    render_warning_message("Stretch Detected! Hold this position..", colors["GREEN"], screen, warning_font)
                                else:
                                    countdown_value = 8 - (elapsed_time - 2000) // 1000
                                    if countdown_value > 0:
                                        countdown_surface = countdown_font.render(str(countdown_value), True, colors["WHITE"])
                                        screen.blit(countdown_surface, (
                                            SCREEN_WIDTH // 2 - countdown_surface.get_width() // 2,
                                            SCREEN_HEIGHT // 2,
                                        ))
                                    else:
                                        stretch_completed_flags[0] = True
                                        countdown_start_time = None
                                       
                            else:
                                countdown_start_time = None
                                render_warning_message("Right shoulder extension!", colors["BLUE"], screen, warning_font)
                        else:
                            if not countdown_start_time:
                                countdown_start_time = pygame.time.get_ticks()

                            elapsed_time = pygame.time.get_ticks() - countdown_start_time

                            if elapsed_time < 2000:
                                render_warning_message("Good Job", colors["GREEN"], screen, warning_font)
                            else:
                                countdown_start_time = None
                                stretch_exercise += 1

                    case 1:
                        if not stretch_completed_flags[1]:
                            if detect_bend_to_right(results.pose_landmarks, mp_pose):
                                if not countdown_start_time:
                                    countdown_start_time = pygame.time.get_ticks()

                                elapsed_time = pygame.time.get_ticks() - countdown_start_time

                                if elapsed_time < 1000:
                                    render_warning_message("Stretch Detected! Hold this position..", colors["GREEN"], screen, warning_font)
                                else:
                                    countdown_value = 8 - (elapsed_time - 2000) // 1000
                                    if countdown_value > 0:
                                        countdown_surface = countdown_font.render(str(countdown_value), True, colors["WHITE"])
                                        screen.blit(countdown_surface, (
                                            SCREEN_WIDTH // 2 - countdown_surface.get_width() // 2,
                                            SCREEN_HEIGHT // 2,
                                        ))
                                    else:
                                        stretch_completed_flags[1] = True
                                        countdown_start_time = None
                                        
                            else:
                                countdown_start_time = None
                                render_warning_message("Left shoulder extension!", colors["BLUE"], screen, warning_font)
                        else:
                            if not countdown_start_time:
                                countdown_start_time = pygame.time.get_ticks()

                            elapsed_time = pygame.time.get_ticks() - countdown_start_time

                            if elapsed_time < 2000:
                                render_warning_message("Good Job", colors["GREEN"], screen, warning_font)
                            else:
                                countdown_start_time = None
                                stretch_exercise += 1

                if stretch_exercise >= num_exercises:
                    render_warning_message("Session Complete!", colors["GREEN"], screen, warning_font)
        else:
            if results.pose_landmarks:
                upper_body_detected = detect_upper_body(results.pose_landmarks, mp_pose)

                if upper_body_detected:
                    if not countdown_start_time:
                        countdown_start_time = pygame.time.get_ticks()

                    elapsed_time = pygame.time.get_ticks() - countdown_start_time

                    if elapsed_time < 2000:
                        render_warning_message("Good Job! Let's start your stretch session!", colors["GREEN"], screen, warning_font)
                    else:
                        countdown_value = 3 - (elapsed_time - 2000) // 1000
                        if countdown_value > 0:
                            countdown_surface = countdown_font.render(str(countdown_value), True, colors["WHITE"])
                            screen.blit(countdown_surface, (
                                SCREEN_WIDTH // 2 - countdown_surface.get_width() // 2,
                                SCREEN_HEIGHT // 2,
                            ))
                        else:
                            print("Starting stretch session!")
                            countdown_start_time = None
                            stretch_screen_active = True
                else:
                    render_warning_message("Align your upper body like the image!", colors["BLUE"], screen, warning_font)
    else:
        hand_results = hands.process(frame)

        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x, y = int(index_finger_tip.x * SCREEN_WIDTH), int(index_finger_tip.y * SCREEN_HEIGHT)

                if start_button_rect.collidepoint(x, y):
                    stretch_detection_started = True
        else:
            render_warning_message("Use your index finger to start!", colors["BLUE"], screen, warning_font)

        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 100))

        pygame.draw.rect(screen, colors["GREEN"], start_button_rect)
        screen.blit(start_button_text, (
            start_button_rect.x + start_button_rect.width // 2 - start_button_text.get_width() // 2,
            start_button_rect.y + start_button_text.get_height() // 4,
        ))

    pygame.display.flip()

cap.release()
pygame.quit()
