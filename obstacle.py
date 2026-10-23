
import math
import random
import pygame
from settings import WIDTH, HEIGHT


OBSTACLE_WIDTH = 75
SPAWN_GAP = 320

VOID = (13, 9, 25)
STONE = (34, 24, 48)
STONE_LIGHT = (62, 43, 79)
VIOLET = (125, 56, 185)
GLOW = (194, 119, 255)
PALE = (231, 204, 255)
GOLD = (221, 180, 103)


class Obstacle:
    def __init__(self, x, gap_size):
        self.x = float(x)
        self.gap_size = gap_size

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

        top = pygame.Rect(int(self.x), 0, OBSTACLE_WIDTH, top_height)
        bottom = pygame.Rect(
            int(self.x), bottom_y, OBSTACLE_WIDTH, HEIGHT - bottom_y
        )
        return top, bottom

    def collides_with(self, player_rect):
        top, bottom = self.get_rects()
        return (
            player_rect.colliderect(top)
            or player_rect.colliderect(bottom)
        )

    def draw(self, screen):
        top, bottom = self.get_rects()
        x = int(self.x)
        w = OBSTACLE_WIDTH

        for rect in (top, bottom):
            if rect.height <= 0:
                continue

            # Heavy dark stone body
            pygame.draw.rect(screen, VOID, rect)
            pygame.draw.rect(screen, STONE, rect.inflate(-8, 0))

            # Inner bevels
            pygame.draw.line(
                screen, STONE_LIGHT,
                (x + 8, rect.top), (x + 8, rect.bottom), 3
            )
            pygame.draw.line(
                screen, (22, 14, 34),
                (x + w - 8, rect.top), (x + w - 8, rect.bottom), 3
            )

            # Repeating carved stone panels
            for y in range(rect.top + 28, rect.bottom - 12, 54):
                pygame.draw.line(
                    screen, STONE_LIGHT,
                    (x + 12, y), (x + w - 12, y), 2
                )
                pygame.draw.line(
                    screen, VOID,
                    (x + 15, y + 3), (x + w - 15, y + 3), 1
                )

                # Diamond rune inset
                cx = x + w // 2
                points = [
                    (cx, y - 5),
                    (cx + 5, y),
                    (cx, y + 5),
                    (cx - 5, y)
                ]
                pygame.draw.polygon(screen, VIOLET, points, 1)
                pygame.draw.circle(screen, GOLD, (cx, y), 1)

            # Gold rivets on the stone edges
            for y in range(rect.top + 16, rect.bottom - 8, 65):
                for rivet_x in (x + 5, x + w - 5):
                    pygame.draw.circle(
                        screen, GOLD, (rivet_x, y), 2
                    )
                    pygame.draw.circle(
                        screen, PALE, (rivet_x, y), 1
                    )

            # Outer frame
            pygame.draw.rect(screen, VIOLET, rect, 3)
            inner_frame = rect.inflate(-12, 0)
            if inner_frame.width > 0 and inner_frame.height > 0:
                pygame.draw.rect(
                    screen, STONE_LIGHT, inner_frame, 1
                )

        # Ornate caps around the opening
        top_edge = top.bottom
        bottom_edge = bottom.top

        upper_cap = [
            (x, top_edge - 11),
            (x + 9, top_edge - 16),
            (x + w - 9, top_edge - 16),
            (x + w, top_edge - 11),
            (x + w - 7, top_edge + 5),
            (x + 7, top_edge + 5)
        ]
        lower_cap = [
            (x + 7, bottom_edge - 5),
            (x + w - 7, bottom_edge - 5),
            (x + w, bottom_edge + 11),
            (x + w - 9, bottom_edge + 16),
            (x + 9, bottom_edge + 16),
            (x, bottom_edge + 11)
        ]

        pygame.draw.polygon(screen, STONE_LIGHT, upper_cap)
        pygame.draw.polygon(screen, STONE_LIGHT, lower_cap)
        pygame.draw.polygon(screen, GOLD, upper_cap, 1)
        pygame.draw.polygon(screen, GOLD, lower_cap, 1)

        # Glowing energy at the gap boundaries
        tick = pygame.time.get_ticks() * 0.006
        pulse = 0.5 + 0.5 * math.sin(tick)
        glow_color = (
            int(145 + 70 * pulse),
            int(75 + 45 * pulse),
            255
        )

        pygame.draw.line(
            screen, glow_color,
            (x, top_edge - 1), (x + w, top_edge - 1), 4
        )
        pygame.draw.line(
            screen, glow_color,
            (x, bottom_edge + 1), (x + w, bottom_edge + 1), 4
        )
        pygame.draw.line(
            screen, PALE,
            (x + 12, top_edge), (x + w - 12, top_edge), 1
        )
        pygame.draw.line(
            screen, PALE,
            (x + 12, bottom_edge), (x + w - 12, bottom_edge), 1
        )

        # Floating magical motes in the gap
        for i in range(3):
            mote_x = x + 12 + ((i * 23 + int(tick * 8)) % 50)
            mote_y = int(
                self.gap_y + math.sin(tick + i * 2) * (self.gap_size * 0.3)
            )
            if top_edge + 8 < mote_y < bottom_edge - 8:
                pygame.draw.circle(
                    screen, (180, 115, 255), (mote_x, mote_y), 2
                )

    def is_off_screen(self):
        return self.x + OBSTACLE_WIDTH < 0
