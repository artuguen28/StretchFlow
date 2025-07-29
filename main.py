import cv2
import mediapipe as mp
import pygame
from app.strech_detector import detect_stretch, plot_landmarks

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1440
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("StretchFlow")

# Fonts and colors
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

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

    # Flip the frame horizontally for a mirror effect
    frame = cv2.flip(frame, 1)

    # Store the original frame for processing
    original_frame = frame.copy()

    # Convert frame to RGB for pygame
    frame = cv2.resize(frame, (SCREEN_WIDTH, SCREEN_HEIGHT))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = pygame.surfarray.make_surface(frame)
    frame = pygame.transform.rotate(frame, -90)
    frame = pygame.transform.flip(frame, True, False)

    # Display video as background
    screen.blit(frame, (0, 0))

    if not detection_started:
        # Display title
        title_surface = font.render("StretchFlow", True, WHITE)
        screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 100))

        # Display button
        pygame.draw.rect(screen, GREEN, button_rect)
        button_text = button_font.render("Start", True, BLACK)
        screen.blit(button_text, (button_rect.x + button_rect.width // 2 - button_text.get_width() // 2,
                                  button_rect.y + button_rect.height // 2 - button_text.get_height() // 2))
    else:
        # Perform stretch detection using the original frame
        rgb = cv2.cvtColor(original_frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)

        if results.pose_landmarks:
            print("Landmarks detected!")

            # Resize the frame to match the screen dimensions
            resized_frame = cv2.resize(original_frame, (SCREEN_WIDTH, SCREEN_HEIGHT))

            # Plot landmarks on the resized frame
            plot_landmarks(resized_frame, results.pose_landmarks)

            # Convert the resized frame (with landmarks) for pygame display
            frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame)
            frame = pygame.transform.rotate(frame, -90)
            frame = pygame.transform.flip(frame, True, False)

            # Display video as background
            screen.blit(frame, (0, 0))
        else:
            print("No landmarks detected.")

    pygame.display.flip()

cap.release()
pygame.quit()