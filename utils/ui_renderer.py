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

    def render_warning_message(self, message, color, font):
        surface = font.render(message, True, color)
        x = self.screen_width // 2 - surface.get_width() // 2
        y = self.screen_height - self.scaler.y(200)
        self.screen.blit(surface, (x, y))
