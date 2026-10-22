# Numbers you can tune
SLOW_TIME = 4.0       # how many seconds the Time Stone lasts
SLOW_FACTOR = 0.5     # barriers move at half speed while it is active


class PowerUp:
    def __init__(self):
        self.timer = 0.0        # seconds left on the effect
        self.active = False     # True while the effect is running

    def activate(self):
        """Call this when the Cloak collects the Time Stone."""
        self.timer = SLOW_TIME
        self.active = True

    def update(self, dt):
        """Call this every frame. dt is the time since the last frame."""
        if self.active:
            self.timer = self.timer - dt
            if self.timer <= 0:
                self.timer = 0
                self.active = False

    def speed_multiplier(self):
        """Multiply the barrier speed by this number."""
        if self.active:
            return SLOW_FACTOR
        return 1.0

    def reset(self):
        self.timer = 0.0
        self.active = False