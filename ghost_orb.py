import math
import random
import pygame
from settings import *


class GhostOrb:
    """Yellow power-up: makes the Cloak invisible and untouchable for a few seconds."""

    def __init__(self):
        self.x = 0.0
        self.base_y = 0.0
        self.y = 0.0
        self.age = 0.0
        self.active = False
        self.rect = pygame.Rect(0, 0, 0, 0)

    def spawn(self, x):
        """Place the orb at x, at a random height."""
        self.x = float(x)
        self.base_y = random.randint(GAP_MARGIN, HEIGHT - GAP_MARGIN)
        self.y = float(self.base_y)
        self.age = 0.0
        self.active = True
        self.update_rect()

    def update(self, dt, speed):
        """Move left with the barriers and bob up and down."""
        if not self.active:
            return
        self.age += dt
        self.x -= speed * dt
        self.y = self.base_y + math.sin(self.age * 3.2) * 22
        self.update_rect()
        if self.x + GHOST_RADIUS < 0:
            self.active = False

    def update_rect(self):
        size = GHOST_RADIUS * 2
        self.rect = pygame.Rect(
            round(self.x - GHOST_RADIUS),
            round(self.y - GHOST_RADIUS),
            size, size
        )

    def collected(self, player_rect):
        return self.active and self.rect.colliderect(player_rect)

    def draw(self, screen):
        if not self.active:
            return

        cx, cy = round(self.x), round(self.y)
        r = GHOST_RADIUS
        pulse = (math.sin(self.age * 6.5) + 1) / 2

        # Pulsing golden aura
        pygame.draw.circle(
            screen, (110, 85, 10), (cx, cy), round(r + 8 + pulse * 4), 2
        )
        pygame.draw.circle(
            screen, GHOST_EDGE, (cx, cy), round(r + 3 + pulse * 2), 1
        )

        # Yellow gem
        pygame.draw.circle(screen, (95, 70, 5), (cx, cy), r)
        pygame.draw.circle(screen, GHOST_COLOR, (cx, cy), r - 3)
        pygame.draw.circle(screen, (255, 250, 200), (cx - 4, cy - 4), r // 3)

        # Gold ring
        pygame.draw.circle(screen, (221, 180, 103), (cx, cy), r, 2)

        # Little ghost mark in the middle
        pygame.draw.circle(screen, (120, 85, 0), (cx, cy - 2), 4)
        pygame.draw.rect(screen, (120, 85, 0), (cx - 4, cy - 2, 9, 6))
        pygame.draw.circle(screen, GHOST_COLOR, (cx - 2, cy - 2), 1)
        pygame.draw.circle(screen, GHOST_COLOR, (cx + 2, cy - 2), 1)

        # Orbiting sparks
        for i in range(3):
            angle = self.age * 2.4 + i * (2 * math.pi / 3)
            orbit = r + 8 + pulse * 2
            sx = round(cx + math.cos(angle) * orbit)
            sy = round(cy + math.sin(angle) * orbit)
            pygame.draw.circle(screen, (255, 220, 60), (sx, sy), 2)
            pygame.draw.circle(screen, (255, 255, 210), (sx, sy), 1)


class GhostEffect:
    """Tracks the 'invisible + invincible' timer (same style as TimeStoneEffect)."""

    def __init__(self, duration=GHOST_DURATION):
        self.duration = duration
        self.time_left = 0.0

    def activate(self):
        """Start (or restart) the effect. A second orb refreshes the timer, it does not stack."""
        self.time_left = self.duration

    def update(self, dt):
        if self.time_left > 0:
            self.time_left = max(0.0, self.time_left - dt)

    def reset(self):
        self.time_left = 0.0

    @property
    def active(self):
        return self.time_left > 0

    @property
    def alpha(self):
        """Fully invisible while active; reappears flickering in the last second as a warning."""
        if not self.active:
            return 255
        if self.time_left < GHOST_WARNING_TIME:
            blink = int(self.time_left * 10) % 2
            return 160 if blink else GHOST_ALPHA
        return GHOST_ALPHA