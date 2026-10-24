"""Time Stone (A3) and optional power-ups.

The Time Stone slows the barriers' speed ONLY (not gravity, not the Cloak) for a few seconds.
Everything here uses plain numbers/tuples, so it can be tested without opening a Pygame window.
"""
import random
from enum import Enum

TIME_STONE_SLOW_FACTOR = 0.5     # barriers move at half speed while the effect is active
TIME_STONE_DURATION = 4.0        # seconds
TIME_STONE_SPAWN_CHANCE = 0.15   # chance per barrier pair (tune after playtesting)
POWERUP_SIZE = 28                # pixels


class PowerUpType(Enum):
    TIME_STONE = "time_stone"
    INVINCIBILITY = "invincibility"
    BONUS_SCORE = "bonus_score"


class PowerUp:
    """A collectable item that drifts left together with the barriers."""

    def __init__(self, power_type, size=POWERUP_SIZE):
        self.type = power_type
        self.size = size
        self.x = 0.0
        self.y = 0.0
        self.active = False

    def spawn(self, x, y):
        self.x = x
        self.y = y
        self.active = True

    def update(self, dt, scroll_speed):
        """Move left at the same speed as the barriers. Deactivates once off screen."""
        if not self.active:
            return
        self.x -= scroll_speed * dt
        if self.x + self.size < 0:
            self.active = False

    @property
    def rect(self):
        """(x, y, width, height) - Anas can use this to draw the sprite."""
        return (self.x, self.y, self.size, self.size)

    def collides_with(self, rect):
        """rect is (x, y, w, h); a pygame.Rect also works because it unpacks to 4 numbers."""
        if not self.active:
            return False
        px, py, pw, ph = rect
        return (self.x < px + pw and self.x + self.size > px and
                self.y < py + ph and self.y + self.size > py)

    def collect(self):
        """Call when the Cloak picks it up. The item disappears."""
        self.active = False


class TimeStoneEffect:
    """Tracks the 'barriers are slowed' timer."""

    def __init__(self, duration=TIME_STONE_DURATION, slow_factor=TIME_STONE_SLOW_FACTOR):
        self.duration = duration
        self.slow_factor = slow_factor
        self.time_left = 0.0

    def activate(self):
        """Start (or restart) the effect. A second stone refreshes the timer, it does not stack."""
        self.time_left = self.duration

    def update(self, dt):
        """Call once per frame while the game is PLAYING (skip while paused, so the timer pauses too)."""
        if self.time_left > 0:
            self.time_left = max(0.0, self.time_left - dt)

    def reset(self):
        self.time_left = 0.0

    @property
    def active(self):
        return self.time_left > 0

    @property
    def multiplier(self):
        """Multiply the barrier speed by this: 0.5 while active, 1.0 otherwise."""
        return self.slow_factor if self.active else 1.0


def maybe_spawn_time_stone(x, y, rng=random):
    """Roll the dice when a new barrier pair spawns. Returns a spawned PowerUp or None."""
    if rng.random() < TIME_STONE_SPAWN_CHANCE:
        stone = PowerUp(PowerUpType.TIME_STONE)
        stone.spawn(x, y)
        return stone
    return None