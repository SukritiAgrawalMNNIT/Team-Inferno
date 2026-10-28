import math
import random
import pygame
from settings import *


class BonusOrb:
    """Red power-up: collecting it gives BONUS_POINTS extra score."""

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
        self.y = self.base_y + math.sin(self.age * 3.5) * 20
        self.update_rect()
        if self.x + BONUS_RADIUS < 0:
            self.active = False

    def update_rect(self):
        size = BONUS_RADIUS * 2
        self.rect = pygame.Rect(
            round(self.x - BONUS_RADIUS),
            round(self.y - BONUS_RADIUS),
            size, size
        )

    def collected(self, player_rect):
        return self.active and self.rect.colliderect(player_rect)

    def draw(self, screen):
        if not self.active:
            return

        cx, cy = round(self.x), round(self.y)
        r = BONUS_RADIUS
        pulse = (math.sin(self.age * 7) + 1) / 2

        # Pulsing blood-red aura
        pygame.draw.circle(
            screen, (90, 10, 20), (cx, cy), round(r + 8 + pulse * 4), 2
        )
        pygame.draw.circle(
            screen, (170, 25, 40), (cx, cy), round(r + 3 + pulse * 2), 1
        )

        # Red gem
        pygame.draw.circle(screen, (60, 5, 12), (cx, cy), r)
        pygame.draw.circle(screen, (200, 30, 45), (cx, cy), r - 3)
        pygame.draw.circle(screen, (255, 90, 90), (cx - 4, cy - 4), r // 3)

        # Gold ring
        pygame.draw.circle(screen, (221, 180, 103), (cx, cy), r, 2)

        # Little "+" mark in the middle
        pygame.draw.line(screen, (255, 225, 225), (cx - 5, cy), (cx + 5, cy), 2)
        pygame.draw.line(screen, (255, 225, 225), (cx, cy - 5), (cx, cy + 5), 2)

        # Orbiting sparks
        for i in range(3):
            angle = self.age * 2.2 + i * (2 * math.pi / 3)
            orbit = r + 8 + pulse * 2
            sx = round(cx + math.cos(angle) * orbit)
            sy = round(cy + math.sin(angle) * orbit)
            pygame.draw.circle(screen, (255, 70, 70), (sx, sy), 2)
            pygame.draw.circle(screen, (255, 210, 210), (sx, sy), 1)