from math import hypot

import pygame


class StretchExercise:
    def __init__(self, name, detect_func, prompt_msg, success_msg):
        self.name = name
        self.detect_func = detect_func
        self.prompt_msg = prompt_msg
        self.success_msg = success_msg
        self.completed = False
        self.countdown_start_time = None

    def update(self, pose_landmarks, mp_pose, renderer, warning_font, countdown_font, colors, timer_duration):
        if self.completed:
            if not self.countdown_start_time:
                self.countdown_start_time = pygame.time.get_ticks()

            elapsed_time = pygame.time.get_ticks() - self.countdown_start_time
            if elapsed_time < 2000:  # 2 seconds to show success message
                renderer.render_warning_message(self.success_msg, colors["BLACK"], warning_font, colors["GREEN"])
                return False
            else:
                self.countdown_start_time = None
                return True

        if self.detect_func(pose_landmarks, mp_pose):
            if not self.countdown_start_time:
                self.countdown_start_time = pygame.time.get_ticks()

            elapsed_time = pygame.time.get_ticks() - self.countdown_start_time

            if elapsed_time < 1000:
                renderer.render_warning_message("Stretch Detected! Hold this position...", colors["BLACK"], warning_font, colors["GREEN"])
            else:
                hold_time_ms = timer_duration * 1000
                countdown_value = timer_duration - (elapsed_time - 1000) // 1000  # starts after 1s delay
                if countdown_value > 0:
                    renderer.render_centered_text(str(countdown_value), colors["WHITE"], countdown_font)
                else:
                    self.completed = True
                    self.countdown_start_time = None
        else:
            self.countdown_start_time = None
            renderer.render_warning_message(self.prompt_msg, colors["WHITE"], warning_font, colors["BLUE"])

        return False
    


class PoseDetectors:

    @staticmethod
    def detect_upper_body(landmarks, mp_pose):
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

    @staticmethod
    def detect_bend_to_right(landmarks, mp_pose):
        if not landmarks:
            return False
        lm = landmarks.landmark
        left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_hip = lm[mp_pose.PoseLandmark.LEFT_HIP]
        left_wrist = lm[mp_pose.PoseLandmark.LEFT_WRIST]
        nose = lm[mp_pose.PoseLandmark.NOSE]
        return (
            left_shoulder.x < left_hip.x and
            left_wrist.x < right_shoulder.x and
            left_wrist.y < nose.y
        )

    @staticmethod
    def detect_bend_to_left(landmarks, mp_pose):
        if not landmarks:
            return False
        lm = landmarks.landmark
        left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_hip = lm[mp_pose.PoseLandmark.RIGHT_HIP]
        right_wrist = lm[mp_pose.PoseLandmark.RIGHT_WRIST]
        nose = lm[mp_pose.PoseLandmark.NOSE]
        return (
            right_shoulder.x > right_hip.x
            and right_wrist.x > left_shoulder.x
            and right_wrist.y < nose.y
        )

    @staticmethod
    def detect_right_shoulder_extension(landmarks, mp_pose):
        if not landmarks:
            return False
        lm = landmarks.landmark
        left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_elbow = lm[mp_pose.PoseLandmark.RIGHT_ELBOW]
        left_wrist = lm[mp_pose.PoseLandmark.LEFT_WRIST]

        elbow_dist = hypot(right_elbow.x - left_shoulder.x, right_elbow.y - left_shoulder.y)
        wrist_dist = hypot(left_wrist.x - left_shoulder.x, left_wrist.y - left_shoulder.y)

        return elbow_dist < 0.15 and wrist_dist < 0.15

    @staticmethod
    def detect_left_shoulder_extension(landmarks, mp_pose):
        if not landmarks:
            return False
        lm = landmarks.landmark
        right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_elbow = lm[mp_pose.PoseLandmark.LEFT_ELBOW]
        right_wrist = lm[mp_pose.PoseLandmark.RIGHT_WRIST]

        elbow_dist = hypot(left_elbow.x - right_shoulder.x, left_elbow.y - right_shoulder.y)
        wrist_dist = hypot(right_wrist.x - right_shoulder.x, right_wrist.y - right_shoulder.y)

        return elbow_dist < 0.15 and wrist_dist < 0.15

    
    @staticmethod
    def detect_neck_tilt_left(landmarks, mp_pose):
        if not landmarks:
            return False
        lm = landmarks.landmark
        nose = lm[mp_pose.PoseLandmark.NOSE]
        left_shoulder = lm[mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_wrist = lm[mp_pose.PoseLandmark.LEFT_WRIST]
        wrist_nose_distance = hypot(left_wrist.x - nose.x, left_wrist.y - nose.y)

        return abs(nose.x - left_shoulder.x) < 0.08 and wrist_nose_distance < 0.15

    @staticmethod
    def detect_neck_tilt_right(landmarks, mp_pose):
        if not landmarks:
            return False
        lm = landmarks.landmark
        nose = lm[mp_pose.PoseLandmark.NOSE]
        right_shoulder = lm[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_wrist = lm[mp_pose.PoseLandmark.RIGHT_WRIST]
        wrist_nose_distance = hypot(right_wrist.x - nose.x, right_wrist.y - nose.y)

        return abs(nose.x - right_shoulder.x) < 0.08 and wrist_nose_distance < 0.15