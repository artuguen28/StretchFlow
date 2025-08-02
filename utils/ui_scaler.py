class UIScaler:
    def __init__(self, screen_width, screen_height, ref_width=1920, ref_height=1440):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scale_x = screen_width / ref_width
        self.scale_y = screen_height / ref_height
        self.scale_avg = (self.scale_x + self.scale_y) / 2

    def x(self, val):
        return int(val * self.scale_x)

    def y(self, val):
        return int(val * self.scale_y)

    def font(self, base_size):
        return int(base_size * self.scale_avg)