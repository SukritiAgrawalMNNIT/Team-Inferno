import random
import pygame
from settings import *


class Barrier:
    def __init__(self):
        self.x = float(WIDTH)
        self.gap = 200
        self.gap_y = 0            # y position of the top of the gap
        self.passed = False       # True once the Cloak has flown past it
        self.active = False       # False = resting in the pool, waiting to be reused
        self.top_rect = pygame.Rect(0, 0, 0, 0)
        self.bottom_rect = pygame.Rect(0, 0, 0, 0)

    def spawn(self, gap):
        """Put this barrier at the right edge with a random gap height."""
        self.x = float(WIDTH)
        self.gap = gap
        self.gap_y = random.randint(GAP_MARGIN, HEIGHT - GAP_MARGIN - gap)
        self.passed = False
        self.active = True
        self.update_rects()

    def update(self, dt, speed):
        """Move left. When fully off-screen, go back to the pool."""
        self.x -= speed * dt
        self.update_rects()
        if self.is_off_screen():
            self.active = False

    def update_rects(self):
        x = round(self.x)
        gap_bottom = self.gap_y + self.gap
        self.top_rect = pygame.Rect(x, 0, BARRIER_WIDTH, self.gap_y)
        self.bottom_rect = pygame.Rect(x, gap_bottom, BARRIER_WIDTH, HEIGHT - gap_bottom)

    def is_off_screen(self):
        return self.x + BARRIER_WIDTH < 0

    def collides(self, rect):
        """True if the given rectangle touches the top or bottom block."""
        return self.top_rect.colliderect(rect) or self.bottom_rect.colliderect(rect)

    def draw(self, screen):
        # Simple look for now. The UI person can restyle this.
        for block in (self.top_rect, self.bottom_rect):
            pygame.draw.rect(screen, BARRIER_COLOR, block)
            pygame.draw.rect(screen, BARRIER_EDGE, block, 3)