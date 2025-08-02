import pygame


class UIRenderer:
    def __init__(self, screen, scaler):
        self.screen = screen
        self.scaler = scaler
        self.screen_width = scaler.screen_width
        self.screen_height = scaler.screen_height

    def render_centered_text(self, text, color, font, y_offset=0):
        surface = font.render(text, True, color)
        x = self.screen_width // 2 - surface.get_width() // 2
        y = self.screen_height // 2 + y_offset
        self.screen.blit(surface, (x, y))

    def render_warning_message(self, message, text_color, font, background_color=(0, 0, 0), padding=20):
        """
        Render warning message at top with background rectangle.
        """
        surface = font.render(message, True, text_color)
        text_rect = surface.get_rect()
        text_rect.centerx = self.screen_width // 2
        text_rect.top = self.scaler.y(150)

        bg_rect = pygame.Rect(
            text_rect.left - padding,
            text_rect.top - padding // 2,
            text_rect.width + padding * 2,
            text_rect.height + padding
        )

        pygame.draw.rect(self.screen, background_color, bg_rect, border_radius=10)
        self.screen.blit(surface, text_rect)

    def render_home_warning_message(self, message, text_color, font, background_color=(0, 0, 0), padding=20):
        """
        Render warning message at bottom with background rectangle.
        """
        surface = font.render(message, True, text_color)
        text_rect = surface.get_rect()
        text_rect.centerx = self.screen_width // 2
        text_rect.bottom = self.screen_height - self.scaler.y(150)

        bg_rect = pygame.Rect(
            text_rect.left - padding,
            text_rect.top - padding // 2,
            text_rect.width + padding * 2,
            text_rect.height + padding
        )

        pygame.draw.rect(self.screen, background_color, bg_rect, border_radius=10)
        self.screen.blit(surface, text_rect)

    def render_image(self, image_surface, position="bottom_center", scale=1.0):
        img = image_surface
        if scale != 1.0:
            width = int(img.get_width() * scale)
            height = int(img.get_height() * scale)
            img = pygame.transform.scale(img, (width, height))

        if position == "bottom_center":
            x = self.screen_width // 2 - img.get_width() // 2
            y = self.screen_height - img.get_height() - self.scaler.y(300)
        elif position == "center":
            x = self.screen_width // 2 - img.get_width() // 2
            y = self.screen_height // 2 - img.get_height() // 2
        else:
            x, y = position  # custom (x, y)

        self.screen.blit(img, (x, y))
