import time

import argparse
import cv2
import mediapipe as mp
import pygame

from app.stretch_detector import PoseDetectors, StretchExercise
from utils.config import colors
from utils.ui_scaler import UIScaler
from utils.ui_renderer import UIRenderer


class StretchFlowApp:
    def __init__(self, timer):
        self.timer = timer
        self.screen, self.width, self.height = init_pygame_window()
        self.scaler = UIScaler(self.width, self.height)
        self.renderer = UIRenderer(self.screen, self.scaler)
        self.upper_body_layout = load_assets()
        self.fonts = create_fonts(self.scaler)
        self.mp_pose, self.pose, self.mp_hands, self.hands = setup_mediapipe()
        self.exercises = create_exercise_list()
        self.timer = timer

        self.scaler = UIScaler(self.width, self.height)
        self.renderer = UIRenderer(self.screen, self.scaler)

        self.title_font = pygame.font.Font(None, self.scaler.font(150))
        self.warning_font = pygame.font.Font(None, self.scaler.font(70))
        self.button_font = pygame.font.Font(None, self.scaler.font(100))
        self.countdown_font = pygame.font.Font(None, self.scaler.font(200))

        self.title_surface = self.title_font.render("StretchFlow", True, colors["WHITE"])
        self.start_button_text = self.button_font.render("START", True, colors["GREEN"])
        self.home_button_text = self.button_font.render("HOME", True, colors["WHITE"])

        self.title_rect = pygame.Rect(self.scaler.x(self.width // 2 - 350), self.scaler.y(80), self.scaler.x(700), self.scaler.y(130))
        self.start_button_rect = pygame.Rect(self.scaler.x(self.width // 2 - 150), self.scaler.y(self.height // 2), self.scaler.x(300), self.scaler.y(100))
        self.home_button_rect = pygame.Rect(self.scaler.x(self.width // 2 - 150), self.scaler.y(self.height // 2 + 300), self.scaler.x(300), self.scaler.y(100))

        self.stretch_detection_started = False
        self.stretch_screen_active = False
        self.countdown_start_time = None
        self.current_exercise_index = 0
        self.running = True
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            ret, frame = self.cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (self.width, self.height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            pygame_frame = pygame.surfarray.make_surface(frame)
            pygame_frame = pygame.transform.rotate(pygame_frame, -90)
            self.screen.blit(pygame_frame, (0, 0))

            results = self.pose.process(frame)

            if self.stretch_detection_started:
                if self.stretch_screen_active:
                    self.handle_exercise_screen(results, frame)
                else:
                    self.handle_pose_alignment_screen(results)
            else:
                self.handle_home_screen(frame)

            pygame.display.flip()

        self.cap.release()
        pygame.quit()

    def handle_exercise_screen(self, results, frame):
        if results.pose_landmarks and self.current_exercise_index < len(self.exercises):
            current_exercise = self.exercises[self.current_exercise_index]
            finished = current_exercise.update(
                results.pose_landmarks,
                self.mp_pose,
                self.renderer,
                self.warning_font,
                self.countdown_font,
                colors,
                self.timer
            )
            if finished:
                self.current_exercise_index += 1
        elif self.current_exercise_index >= len(self.exercises):
            if not self.countdown_start_time:
                self.countdown_start_time = pygame.time.get_ticks()

            elapsed_time = pygame.time.get_ticks() - self.countdown_start_time

            if elapsed_time < 2000:
                self.renderer.render_warning_message("Session Complete!", colors["BLACK"], self.warning_font, colors["GREEN"])
            else:
                self.renderer.render_warning_message("Use your index finger to go home!", colors["WHITE"], self.warning_font, colors["BLUE"])

            hand_results = self.hands.process(frame)
            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    x, y = int(index_finger_tip.x * self.width), int(index_finger_tip.y * self.height)
                    if self.home_button_rect.collidepoint(x, y):
                        self.reset_state()

            pygame.draw.rect(self.screen, colors["BLUE"], self.home_button_rect, border_radius=15)
            self.screen.blit(self.home_button_text, (
                self.home_button_rect.x + self.home_button_rect.width // 2 - self.home_button_text.get_width() // 2,
                self.home_button_rect.y + self.home_button_text.get_height() // 4,
            ))

    def handle_pose_alignment_screen(self, results):
        if results.pose_landmarks:
            upper_body_detected = PoseDetectors.detect_upper_body(results.pose_landmarks, self.mp_pose)

            if upper_body_detected:
                if not self.countdown_start_time:
                    self.countdown_start_time = pygame.time.get_ticks()

                elapsed_time = pygame.time.get_ticks() - self.countdown_start_time

                if elapsed_time < 2000:
                    self.renderer.render_warning_message("Good Job! Let's start your stretch session!", colors["BLACK"], self.warning_font, colors["GREEN"])
                else:
                    countdown_value = 3 - (elapsed_time - 2000) // 1000
                    if countdown_value > 0:
                        self.renderer.render_centered_text(str(countdown_value), colors["WHITE"], self.countdown_font)
                    else:
                        self.countdown_start_time = None
                        self.stretch_screen_active = True
            else:
                self.renderer.render_warning_message("Step back or forward and try to match your posture with the pose shown!", colors["WHITE"], self.warning_font, colors["BLUE"])
                self.renderer.render_image(self.upper_body_layout, position="center", scale=1)

    def handle_home_screen(self, frame):
        hand_results = self.hands.process(frame)
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                x, y = int(index_finger_tip.x * self.width), int(index_finger_tip.y * self.height)
                if self.start_button_rect.collidepoint(x, y):
                    self.stretch_detection_started = True
        else:
            self.renderer.render_home_warning_message("Use your index finger to touch the button!", colors["WHITE"], self.warning_font, colors["BLUE"])

        pygame.draw.rect(self.screen, colors["BLACK"], self.title_rect, border_radius=15)
        self.screen.blit(self.title_surface, (
            self.width // 2 - self.title_surface.get_width() // 2,
            self.scaler.y(100)
        ))

        pygame.draw.rect(self.screen, colors["WHITE"], self.start_button_rect, border_radius=10)
        self.screen.blit(self.start_button_text, (
            self.start_button_rect.x + self.start_button_rect.width // 2 - self.start_button_text.get_width() // 2,
            self.start_button_rect.y + self.start_button_text.get_height() // 4,
        ))

    def reset_state(self):
        self.stretch_detection_started = False
        self.stretch_screen_active = False
        self.current_exercise_index = 0
        self.countdown_start_time = None


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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="StretchFlow Exercise App")
    parser.add_argument("--timer", type=int, default=9, help="Time in seconds for each exercise")
    args = parser.parse_args()

    app = StretchFlowApp(timer=args.timer)
    app.run()

