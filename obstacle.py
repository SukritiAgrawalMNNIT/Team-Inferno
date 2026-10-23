
import random
import pygame

from settings import WIDTH, HEIGHT


OBSTACLE_WIDTH = 75
SPAWN_GAP = 320


class Obstacle:
    def __init__(self, x, gap_size):
        self.x = float(x)
        self.gap_size = gap_size

        # Keep the gap away from the extreme top and bottom.
        margin = 70
        self.gap_y = random.randint(
            margin + gap_size // 2,
            HEIGHT - margin - gap_size // 2
        )

        self.passed = False

    def update(self, dt, speed):
        self.x -= speed * dt

    def get_rects(self):
        top_height = int(self.gap_y - self.gap_size // 2)
        bottom_y = int(self.gap_y + self.gap_size // 2)

        top = pygame.Rect(
            int(self.x), 0, OBSTACLE_WIDTH, top_height
        )
        bottom = pygame.Rect(
            int(self.x), bottom_y, OBSTACLE_WIDTH, HEIGHT - bottom_y
        )

        return top, bottom

    def collides_with(self, player_rect):
        top, bottom = self.get_rects()
        return player_rect.colliderect(top) or player_rect.colliderect(bottom)

    def draw(self, screen):
        top, bottom = self.get_rects()

        # Dark fantasy barrier styling
        fill = (38, 20, 55)
        outline = (145, 65, 185)

        pygame.draw.rect(screen, fill, top)
        pygame.draw.rect(screen, fill, bottom)

        pygame.draw.rect(screen, outline, top, 3)
        pygame.draw.rect(screen, outline, bottom, 3)

        # Magical bands near the gap
        pygame.draw.line(
            screen, (205, 140, 245),
            (int(self.x), top.bottom - 2),
            (int(self.x + OBSTACLE_WIDTH), top.bottom - 2), 3
        )
        pygame.draw.line(
            screen, (205, 140, 245),
            (int(self.x), bottom.top + 2),
            (int(self.x + OBSTACLE_WIDTH), bottom.top + 2), 3
        )

    def is_off_screen(self):
        return self.x + OBSTACLE_WIDTH < 0
