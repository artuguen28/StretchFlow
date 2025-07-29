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

# Button dimensions
button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 60)

# Initialize OpenCV
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
cap = cv2.VideoCapture(0)

# Game state
running = True
detection_started = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                detection_started = True

    # Capture video frame
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to match the screen dimensions
    frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Perform stretch detection if started
    if detection_started:
        # Convert the frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            print("Landmarks detected!")

            # Plot landmarks directly on the frame
            plot_landmarks(frame, results.pose_landmarks)

            # Detect stretches
            # detect_stretch(results.pose_landmarks, frame)
        else:
            print("No landmarks detected.")

    # Convert the frame to RGB for pygame
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.rotate(frame, -90)

    # Display video as background
    screen.blit(frame, (0, 0))

    # Display title and button if detection has not started
    if not detection_started:
        # Display title
        title_surface = font.render("StretchFlow", True, colors["WHITE"])
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 100))

        # Display button
        pygame.draw.rect(screen, colors["GREEN"], button_rect)
        button_text = button_font.render("Start", True, colors["BLACK"])
        screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2,
                                  button_rect.y + button_rect.height // 2 - button_text.get_height() // 2))

    pygame.display.flip()

cap.release()
pygame.quit()