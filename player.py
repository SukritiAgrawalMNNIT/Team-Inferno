import math
import pygame
from settings import *


class Player:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, *PLAYER_SIZE)
        self.reset()

    def reset(self):
        self.rect.center = (PLAYER_X, HEIGHT // 2)
        self.y = float(self.rect.y)
        self.vy = 0.0
        self.time = 0.0

    def thrust(self):
        self.vy = THRUST

    def update(self, dt):
        self.time += dt
        self.vy = min(self.vy + GRAVITY * dt, MAX_FALL_SPEED)
        self.y += self.vy * dt
        self.rect.y = round(self.y)

    def hits_bounds(self):
        return self.rect.top <= 0 or self.rect.bottom >= HEIGHT

    def draw(self, screen):
        size = 140
        c = size // 2
        s = CLOAK_SCALE
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        # Hem flutters a little, more while rising
        strength = 4 if self.vy < 0 else 2
        f = math.sin(self.time * 14) * strength

        def pt(x, y):
            return (c + x * s, c + y * s)

        # Outer cloak, following the sketch:
        # narrow collar with notches on top, shoulder step, flared body, flat hem
        outer = [
            pt(-14, -22),            # collar top-left
            pt(12, -24),             # collar top-right
            pt(7, -12),              # notch on the right
            pt(20, -9),              # right shoulder
            pt(26 + f * 0.3, 22 + f),    # hem right corner
            pt(-24 - f * 0.3, 24 - f),   # hem left corner
            pt(-26, -6),             # left side
            pt(-9, -13),             # notch on the left
        ]
        pygame.draw.polygon(surf, CLOAK_RED, outer)

        # Darker inner lining
        lining = [
            pt(-9, -9), pt(8, -8),
            pt(16 + f * 0.2, 17 + f * 0.8),
            pt(-17 - f * 0.2, 19 - f * 0.8),
        ]
        pygame.draw.polygon(surf, CLOAK_DARK, lining)

        # Outline, like the pen lines in the sketch
        pygame.draw.polygon(surf, CLOAK_OUTLINE, outer, 2)

        # Gold clasp at the collar
        pygame.draw.circle(surf, CLOAK_GOLD, pt(2, -16), 4)
        pygame.draw.circle(surf, (255, 255, 255), pt(2, -16), 1.5)

        # Tilt up when rising, down when falling
        angle = max(-20, min(20, -self.vy * 0.04))
        surf = pygame.transform.rotate(surf, angle)
        screen.blit(surf, surf.get_rect(center=self.rect.center))