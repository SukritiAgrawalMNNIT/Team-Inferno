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
        r = STONE_RADIUS

        # Dark fantasy palette

        # Emerald green crystal palette
        void = (8, 20, 16)
        violet_dark = (12, 65, 45)
        violet = (25, 150, 95)
        glow = (65, 255, 170)
        pale = (200, 255, 225)
        gold = (221, 180, 103)


        # Gentle pulsing aura
        pulse = (math.sin(self.age * 6) + 1) / 2
        aura_radius = round(r + 7 + pulse * 4)

        pygame.draw.circle(
            screen, (55, 25, 85),
            (cx, cy), aura_radius, 2
        )
        pygame.draw.circle(
            screen, violet,
            (cx, cy), round(r + 3 + pulse * 2), 1
        )

        # Crystal diamond
        diamond = [
            (cx, cy - r),
            (cx + r, cy),
            (cx, cy + r),
            (cx - r, cy)
        ]

        pygame.draw.polygon(screen, void, diamond)
        pygame.draw.polygon(screen, violet_dark, [
            (cx, cy - r + 4),
            (cx + r - 4, cy),
            (cx, cy + r - 4),
            (cx - r + 4, cy)
        ])

        # Faceted crystal highlights
        pygame.draw.polygon(screen, violet, [
            (cx, cy - r + 4),
            (cx - r + 5, cy),
            (cx, cy + 2)
        ])

        pygame.draw.polygon(screen, (90, 40, 140), [
            (cx, cy - r + 4),
            (cx + r - 5, cy),
            (cx, cy + 2)
        ])

        pygame.draw.line(
            screen, glow,
            (cx, cy - r + 4), (cx, cy + r - 4), 1
        )

        # Gold crystal outline
        pygame.draw.polygon(screen, gold, diamond, 2)

        # Inner glowing rune
        rune = [
            (cx, cy - r // 2),
            (cx + r // 3, cy),
            (cx, cy + r // 2),
            (cx - r // 3, cy)
        ]
        pygame.draw.polygon(screen, pale, rune, 1)
        pygame.draw.circle(screen, gold, (cx, cy), 2)

        # Small animated sparkles around the crystal
        for i in range(3):
            angle = self.age * 1.8 + i * (2 * math.pi / 3)
            orbit = r + 7 + pulse * 2

            sx = round(cx + math.cos(angle) * orbit)
            sy = round(cy + math.sin(angle) * orbit)

            pygame.draw.circle(screen, glow, (sx, sy), 2)
            pygame.draw.circle(screen, pale, (sx, sy), 1)
