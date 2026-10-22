# Numbers you can tune
START_SPEED = 250       # how fast barriers move at the start (pixels per second)
MAX_SPEED = 500         # barriers never go faster than this
START_GAP = 200         # size of the gap at the start (pixels)
MIN_GAP = 120           # the gap never gets smaller than this
SPEED_INCREASE = 8      # speed gained for every point scored
GAP_DECREASE = 3        # gap lost for every point scored


class DifficultyManager:
    def __init__(self):
        self.speed = START_SPEED
        self.gap = START_GAP

    def update(self, score):
        """Call this whenever the score changes. Makes the game harder."""
        new_speed = START_SPEED + score * SPEED_INCREASE
        if new_speed > MAX_SPEED:
            new_speed = MAX_SPEED
        self.speed = new_speed

        new_gap = START_GAP - score * GAP_DECREASE
        if new_gap < MIN_GAP:
            new_gap = MIN_GAP
        self.gap = new_gap

    def get_speed(self):
        return self.speed

    def get_gap(self):
        return self.gap

    def reset(self):
        """Go back to the easy settings for a new run."""
        self.speed = START_SPEED
        self.gap = START_GAP