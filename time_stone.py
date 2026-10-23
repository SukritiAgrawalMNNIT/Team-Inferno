import math
import random
import pygame
from settings import *


class TimeStone:
    def __init__(self):
        self.x = 0.0
        self.base_y = 0.0     # the height it floats around
        self.y = 0.0
        self.age = 0.0        # seconds since it appeared
        self.active = False   # False = not on screen
        self.rect = pygame.Rect(0, 0, 0, 0)

    def spawn(self, x):
        """Place the stone at x, at a random height."""
        self.x = float(x)
        self.base_y = random.randint(GAP_MARGIN, HEIGHT - GAP_MARGIN)
        self.y = float(self.base_y)
        self.age = 0.0
        self.active = True
        self.update_rect()

    def update(self, dt, speed):
        """Move left with the barriers and drift up and down."""
        if not self.active:
            return
        self.age += dt
        self.x -= speed * dt
        self.y = self.base_y + math.sin(self.age * 3) * 25   # gentle up-and-down drift
        self.update_rect()
        if self.x + STONE_RADIUS < 0:    # left the screen without being collected
            self.active = False

    def update_rect(self):
        size = STONE_RADIUS * 2
        self.rect = pygame.Rect(round(self.x - STONE_RADIUS), round(self.y - STONE_RADIUS), size, size)

    def collected(self, player_rect):
        """True if the Cloak is touching the stone."""
        return self.active and self.rect.colliderect(player_rect)

    def draw(self, screen):
        if not self.active:
            return
        cx, cy = round(self.x), round(self.y)
        pulse = math.sin(self.age * 6) * 3                       # glow that grows and shrinks
        pygame.draw.circle(screen, STONE_EDGE, (cx, cy), round(STONE_RADIUS + 6 + pulse), 2)
        diamond = [(cx, cy - STONE_RADIUS), (cx + STONE_RADIUS, cy),
                   (cx, cy + STONE_RADIUS), (cx - STONE_RADIUS, cy)]
        pygame.draw.polygon(screen, STONE_COLOR, diamond)
        pygame.draw.polygon(screen, STONE_EDGE, diamond, 2)