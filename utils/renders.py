from utils.config import SCREEN_WIDTH

def render_warning_message( message, color, screen, warning_font):
    """Renders a warning message on the screen."""
    message_surface = warning_font.render(message, True, color)
    screen.blit(
        message_surface,
        (SCREEN_WIDTH // 2 - message_surface.get_width() // 2, 250),
    )