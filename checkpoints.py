from settings import *


class CheckpointManager:
    def __init__(self, every=CHECKPOINT_EVERY):
        self.every = every            # points between checkpoints
        self.reached = 0              # how many checkpoints this run has passed
        self.banner_timer = 0.0       # seconds the CHECKPOINT message still shows

    def reset(self):
        """Start of a new run."""
        self.reached = 0
        self.banner_timer = 0.0

    def check(self, score):
        """Returns True once, at the moment a new checkpoint is reached."""
        level = score // self.every
        if level > self.reached:
            self.reached = level
            self.banner_timer = CHECKPOINT_BANNER_TIME
            return True
        return False

    def update(self, dt):
        """Counts the banner timer down."""
        if self.banner_timer > 0:
            self.banner_timer = max(0.0, self.banner_timer - dt)