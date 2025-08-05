import time

import argparse
import cv2
import mediapipe as mp
import pygame

from app.stretch_detector import PoseDetectors, StretchExercise
from utils.config import colors
from utils.ui_scaler import UIScaler
from utils.ui_renderer import UIRenderer


def init_pygame_window(width_ratio=0.5, height_ratio=0.666):
    pygame.init()
    info = pygame.display.Info()
    width = int(info.current_w * width_ratio)
    height = int(info.current_h * height_ratio)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("StretchFlow")
    return screen, width, height

def load_assets():
    layout_img = pygame.image.load("./resources/assets/upper_body_layout.png").convert_alpha()
    return layout_img

def create_fonts(scaler):
    return {
        "title": pygame.font.Font(None, scaler.font(150)),
        "warning": pygame.font.Font(None, scaler.font(70)),
        "button": pygame.font.Font(None, scaler.font(100)),
        "countdown": pygame.font.Font(None, scaler.font(200))
    }

def setup_mediapipe():
    mp_pose = mp.solutions.pose
    mp_hands = mp.solutions.hands
    return mp_pose, mp_pose.Pose(), mp_hands, mp_hands.Hands()

def create_exercise_list():
    return [
        StretchExercise("Left Bend Stretch", PoseDetectors.detect_bend_to_left, "Put your left arm over your head and lean your body to the left side.", "Nice stretch to the left!"),
        StretchExercise("Right Bend Stretch", PoseDetectors.detect_bend_to_right, "Put your right arm over your head and lean your body to the right side.", "Well done on that right bend!"),
        StretchExercise("Left Cross-Body Arm Stretch", PoseDetectors.detect_left_shoulder_extension, "Bring your left arm across your chest and hold it with your right hand.", "Great stretch!"),
        StretchExercise("Right Cross-Body Arm Stretch", PoseDetectors.detect_right_shoulder_extension, "Bring your right arm across your chest and hold it with your left hand.", "Awesome work!"),
        StretchExercise("Left Neck Tilt Stretch", PoseDetectors.detect_neck_tilt_left, "Gently tilt your head toward your left shoulder and hold it with your left hand.", "Good job relaxing that neck!"),
        StretchExercise("Right Neck Tilt Stretch", PoseDetectors.detect_neck_tilt_right, "Gently tilt your head toward your right shoulder and hold it with your right hand.", "Neck stretch complete!")
    ]

def run_game_loop(screen, width, height, pose, hands, mp_pose, mp_hands, upper_body_layout, exercises, timer):

    scaler = UIScaler(width, height)
    renderer = UIRenderer(screen, scaler)

    # Fonts
    title_font = pygame.font.Font(None, scaler.font(150))
    warning_font = pygame.font.Font(None, scaler.font(70))
    button_font = pygame.font.Font(None, scaler.font(100))
    countdown_font = pygame.font.Font(None, scaler.font(200))

    # Pre-rendered text surfaces
    title_surface = title_font.render("StretchFlow", True, colors["WHITE"])
    start_button_text = button_font.render("START", True, colors["GREEN"])
    home_button_text = button_font.render("HOME", True, colors["WHITE"])

    # UI Rects
    title_rect = pygame.Rect(scaler.x(width // 2 - 350), scaler.y(80), scaler.x(700), scaler.y(130))
    start_button_rect = pygame.Rect(scaler.x(width // 2 - 150), scaler.y(height // 2), scaler.x(300), scaler.y(100))
    home_button_rect = pygame.Rect(scaler.x(width // 2 - 150), scaler.y(height // 2 + 300), scaler.x(300), scaler.y(100))

    # State variables
    stretch_detection_started = False
    stretch_screen_active = False
    countdown_start_time = None
    current_exercise_index = 0
    running = True

    cap = cv2.VideoCapture(0)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (width, height))
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
                        colors,
                        timer
                    )
                    if finished:
                        current_exercise_index += 1
                elif current_exercise_index >= len(exercises):

                    if not countdown_start_time:
                        countdown_start_time = pygame.time.get_ticks()

                    elapsed_time = pygame.time.get_ticks() - countdown_start_time

                    if elapsed_time < 2000:
                        renderer.render_warning_message("Session Complete!", colors["BLACK"], warning_font, colors["GREEN"])
                    else:
                        renderer.render_warning_message("Use your index finger to go home!", colors["WHITE"], warning_font, colors["BLUE"])

                    hand_results = hands.process(frame)
                    if hand_results.multi_hand_landmarks:
                        for hand_landmarks in hand_results.multi_hand_landmarks:
                            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                            x, y = int(index_finger_tip.x * width), int(index_finger_tip.y * height)
                            if home_button_rect.collidepoint(x, y):
                                stretch_detection_started = False
                                stretch_screen_active = False
                                current_exercise_index = 0
                                countdown_start_time = None

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
                        renderer.render_warning_message("Step back or forward and try to match your posture with the pose shown!", colors["WHITE"], warning_font, colors["BLUE"])
                        renderer.render_image(upper_body_layout, position="center", scale=1)
        else:
            hand_results = hands.process(frame)
            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    x, y = int(index_finger_tip.x * width), int(index_finger_tip.y * height)
                    if start_button_rect.collidepoint(x, y):
                        stretch_detection_started = True
            else:
                renderer.render_home_warning_message("Use your index finger to touch the button!", colors["WHITE"], warning_font, colors["BLUE"])

            # Draw title and button
            pygame.draw.rect(screen, colors["BLACK"], title_rect, border_radius=15)
            screen.blit(title_surface, (
                width // 2 - title_surface.get_width() // 2,
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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="StretchFlow Exercise App")
    parser.add_argument("--timer", type=int, default=9, help="Time in seconds for each exercise")
    args = parser.parse_args()

    screen, width, height = init_pygame_window()
    scaler = UIScaler(width, height)
    renderer = UIRenderer(screen, scaler)

    upper_body_layout = load_assets()
    fonts = create_fonts(scaler)
    mp_pose, pose, mp_hands, hands = setup_mediapipe()
    exercises = create_exercise_list()

    run_game_loop(screen, width, height, pose, hands, mp_pose, mp_hands, upper_body_layout, exercises, args.timer)

