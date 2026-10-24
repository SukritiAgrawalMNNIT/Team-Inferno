
import math
import random
import pygame
from settings import *


class Barrier:
    def __init__(self):
        self.x = float(WIDTH)
        self.gap = 200
        self.gap_y = 0
        self.passed = False
        self.active = False
        self.top_rect = pygame.Rect(0, 0, 0, 0)
        self.bottom_rect = pygame.Rect(0, 0, 0, 0)

    def spawn(self, gap, prev_gap_y=None, max_shift=None):
        """Put this barrier at the right edge with a random gap height.
        If the previous gap height is given, the new gap stays within max_shift pixels of it."""
        self.x = float(WIDTH)
        self.gap = gap
        low = GAP_MARGIN                          # highest allowed gap position
        high = HEIGHT - GAP_MARGIN - gap          # lowest allowed gap position
        if prev_gap_y is not None and max_shift is not None:
            near_low = max(low, prev_gap_y - max_shift)
            near_high = min(high, prev_gap_y + max_shift)
            if near_low <= near_high:
                low, high = near_low, near_high
        self.gap_y = random.randint(low, high)
        self.passed = False
        self.active = True
        self.update_rects()
    def update(self, dt, speed):
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
        return (
            self.top_rect.colliderect(rect)
            or self.bottom_rect.colliderect(rect)
        )

    def draw(self, screen):
        VOID = (13, 9, 25)
        STONE = (34, 24, 48)
        STONE_LIGHT = (62, 43, 79)
        VIOLET = (125, 56, 185)
        PALE = (231, 204, 255)
        GOLD = (221, 180, 103)

        x = round(self.x)
        w = BARRIER_WIDTH

        # Dark stone pillars
        for rect in (self.top_rect, self.bottom_rect):
            if rect.height <= 0:
                continue

            pygame.draw.rect(screen, VOID, rect)
            pygame.draw.rect(screen, STONE, rect.inflate(-8, 0))

            # Stone bevels
            pygame.draw.line(
                screen, STONE_LIGHT,
                (x + 7, rect.top), (x + 7, rect.bottom), 3
            )
            pygame.draw.line(
                screen, VOID,
                (x + w - 7, rect.top), (x + w - 7, rect.bottom), 3
            )

            # Carved panels and diamond runes
            for y in range(rect.top + 28, rect.bottom - 12, 54):
                pygame.draw.line(
                    screen, STONE_LIGHT,
                    (x + 12, y), (x + w - 12, y), 2
                )
                pygame.draw.line(
                    screen, VOID,
                    (x + 15, y + 3), (x + w - 15, y + 3), 1
                )

                cx = x + w // 2
                points = [
                    (cx, y - 6),
                    (cx + 6, y),
                    (cx, y + 6),
                    (cx - 6, y)
                ]
                pygame.draw.polygon(screen, VIOLET, points, 2)
                pygame.draw.circle(screen, GOLD, (cx, y), 2)

            # Gold rivets
            for y in range(rect.top + 16, rect.bottom - 8, 65):
                for rx in (x + 5, x + w - 5):
                    pygame.draw.circle(screen, GOLD, (rx, y), 2)
                    pygame.draw.circle(screen, PALE, (rx, y), 1)

            # Violet frame
            pygame.draw.rect(screen, VIOLET, rect, 3)

            inner = rect.inflate(-12, 0)
            if inner.width > 0 and inner.height > 0:
                pygame.draw.rect(screen, STONE_LIGHT, inner, 1)

        # Ornate caps around the gap
        top_edge = self.top_rect.bottom
        bottom_edge = self.bottom_rect.top

        upper_cap = [
            (x, top_edge - 10),
            (x + 8, top_edge - 15),
            (x + w - 8, top_edge - 15),
            (x + w, top_edge - 10),
            (x + w - 6, top_edge + 5),
            (x + 6, top_edge + 5)
        ]

        lower_cap = [
            (x + 6, bottom_edge - 5),
            (x + w - 6, bottom_edge - 5),
            (x + w, bottom_edge + 10),
            (x + w - 8, bottom_edge + 15),
            (x + 8, bottom_edge + 15),
            (x, bottom_edge + 10)
        ]

        pygame.draw.polygon(screen, STONE_LIGHT, upper_cap)
        pygame.draw.polygon(screen, STONE_LIGHT, lower_cap)
        pygame.draw.polygon(screen, GOLD, upper_cap, 1)
        pygame.draw.polygon(screen, GOLD, lower_cap, 1)

        # Pulsing magical edges
        tick = pygame.time.get_ticks() * 0.006
        pulse = 0.5 + 0.5 * math.sin(tick)

        glow = (
            int(145 + 70 * pulse),
            int(75 + 45 * pulse),
            255
        )

        pygame.draw.line(
            screen, glow,
            (x, top_edge - 1), (x + w, top_edge - 1), 4
        )
        pygame.draw.line(
            screen, glow,
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

        # Only THREE floating magical particles in the gap
        gap_center = (top_edge + bottom_edge) // 2
        gap_size = bottom_edge - top_edge

        for i in range(3):
            mote_x = x + 12 + (
                (i * 23 + int(tick * 8)) % max(1, w - 24)
            )
            mote_y = int(
                gap_center
                + math.sin(tick + i * 2) * (gap_size * 0.3)
            )

            if top_edge + 8 < mote_y < bottom_edge - 8:
                pygame.draw.circle(
                    screen, (180, 115, 255), (mote_x, mote_y), 2
                )
                pygame.draw.circle(
                    screen, PALE, (mote_x, mote_y), 1
                )
