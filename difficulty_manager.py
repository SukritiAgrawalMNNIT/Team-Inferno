
BASE_SPEED = 180
MAX_SPEED = 420
BASE_GAP = 180
MIN_GAP = 120

POINTS_PER_LEVEL = 5
SPEED_PER_LEVEL = 15
GAP_SHRINK_PER_LEVEL = 6


class DifficultyManager:
    def __init__(self):
        self.level = 0

    def reset(self):
        self.level = 0

    def on_score(self, score):
        """Call whenever the score changes."""
        self.level = score // POINTS_PER_LEVEL

    @property
    def speed(self):
        return min(
            MAX_SPEED,
            BASE_SPEED + self.level * SPEED_PER_LEVEL
        )

    @property
    def gap_size(self):
        return max(
            MIN_GAP,
            BASE_GAP - self.level * GAP_SHRINK_PER_LEVEL
        )
