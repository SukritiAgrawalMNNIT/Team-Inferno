
import math
import pygame
from settings import *


class Player:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, *PLAYER_SIZE)
        self.trail_positions = []
        self.reset()

    def reset(self):
        self.rect.center = (PLAYER_X, HEIGHT // 2)
        self.y = float(self.rect.y)
        self.vy = 0.0
        self.time = 0.0
        self.trail_positions.clear()

    def thrust(self):
        self.vy = THRUST

    def update(self, dt):
        self.time += dt
        self.vy = min(
            self.vy + GRAVITY * dt,
            MAX_FALL_SPEED
        )
        self.y += self.vy * dt
        self.rect.y = round(self.y)

        self.trail_positions.append(self.rect.centery)

        if len(self.trail_positions) > 12:
            self.trail_positions.pop(0)

    def hits_bounds(self):
        return (
            self.rect.top <= 0
            or self.rect.bottom >= HEIGHT
        )

    def draw(self, screen):
        # --------------------------------------------------
        # 1. Subtle purple motion trail
        # --------------------------------------------------
        trail_surface = pygame.Surface(
            (WIDTH, HEIGHT), pygame.SRCALPHA
        )

        total = len(self.trail_positions)

        for i, y in enumerate(self.trail_positions):
            progress = (i + 1) / max(1, total)
            x = self.rect.centerx - (total - i) * 9
            alpha = int(3 + progress * 30)

            points = [
                (x - 18, y),
                (x - 9, y - 5),
                (x + 3, y - 3),
                (x + 12, y),
                (x + 3, y + 3),
                (x - 9, y + 5),
            ]

            pygame.draw.polygon(
                trail_surface,
                (165, 120, 255, alpha),
                points
            )

        screen.blit(trail_surface, (0, 0))

        # --------------------------------------------------
        # 2. Sharp, tapered cloak
        # --------------------------------------------------
        size = 160
        c = size // 2
        surf = pygame.Surface(
            (size, size), pygame.SRCALPHA
        )

        scale = 0.72
        flutter = math.sin(self.time * 7) * 2
        flutter2 = math.sin(self.time * 7 + 1) * 2

        def pt(x, y):
            return (
                round(c + x * scale),
                round(c + y * scale)
            )

        def curve(p0, p1, p2, p3, steps=12):
            points = []

            for i in range(steps + 1):
                t = i / steps
                u = 1 - t

                x = (
                    u**3 * p0[0]
                    + 3 * u**2 * t * p1[0]
                    + 3 * u * t**2 * p2[0]
                    + t**3 * p3[0]
                )

                y = (
                    u**3 * p0[1]
                    + 3 * u**2 * t * p1[1]
                    + 3 * u * t**2 * p2[1]
                    + t**3 * p3[1]
                )

                points.append(pt(x, y))

            return points

        # Rear edge: starts at a sharp tip and widens
        # slightly near the shoulder.
        upper = curve(
            (-112, 18 + flutter),
            (-90, 11),
            (-60, -15),
            (-30, -15)
        )

        upper += curve(
            (-30, -15),
            (-12, -18),
            (7, -10),
            (22, -7)
        )[1:]

        # Front underside narrows back toward a point.
        lower = curve(
            (34, -2),
            (18, 5),
            (-10, 19 + flutter2),
            (-43, 18 + flutter)
        )

        lower += curve(
            (-43, 18 + flutter),
            (-70, 18),
            (-98, 25 + flutter2),
            (-112, 18 + flutter)
        )[1:]

        body = upper + [
            pt(29, -7),
            pt(34, -2)
        ] + lower

        # Opaque royal-purple fabric.
        pygame.draw.polygon(
            surf, (48, 32, 68, 255), body
        )

        # Thin silver outline emphasizes the sharp shape.
        pygame.draw.lines(
            surf, (190, 180, 215, 255),
            True, body, 2
        )

        # Inner panel is also tapered, not oval.
        inner_top = curve(
            (-104, 17 + flutter),
            (-77, 8),
            (-48, -9),
            (-25, -9)
        )

        inner_bottom = curve(
            (-25, -9),
            (-42, 0),
            (-67, 15 + flutter2),
            (-96, 21 + flutter)
        )

        inner = inner_top + inner_bottom

        pygame.draw.polygon(
            surf, (89, 60, 125, 255), inner
        )

        # Long, narrow fabric folds.
        fold1 = curve(
            (-101, 17 + flutter),
            (-73, 8),
            (-46, -3),
            (-25, -8)
        )

        fold2 = curve(
            (-96, 21 + flutter2),
            (-68, 14),
            (-39, 4),
            (-14, -5)
        )

        fold3 = curve(
            (-80, 22 + flutter),
            (-54, 17),
            (-29, 9),
            (-8, 1)
        )

        pygame.draw.lines(
            surf, (211, 201, 229, 255),
            False, fold1, 1
        )

        pygame.draw.lines(
            surf, (48, 32, 70, 255),
            False, fold2, 2
        )

        pygame.draw.lines(
            surf, (169, 153, 199, 255),
            False, fold3, 1
        )

        # --------------------------------------------------
        # 3. Hood facing right
        # --------------------------------------------------
        hood = [
            pt(-3, -13),
            pt(5, -21),
            pt(17, -22),
            pt(28, -16),
            pt(35, -7),
            pt(33, 1),
            pt(24, 6),
            pt(12, 4),
            pt(4, -2),
        ]

        pygame.draw.polygon(
            surf, (139, 121, 171, 255), hood
        )

        pygame.draw.lines(
            surf, (224, 217, 239, 255),
            True, hood, 1
        )

        # Dark face opening.
        face = [
            pt(18, -16),
            pt(29, -10),
            pt(27, -3),
            pt(17, -4),
            pt(13, -9),
        ]

        pygame.draw.polygon(
            surf, (12, 10, 23, 255), face
        )

        # Cyan eye.
        pygame.draw.line(
            surf, (115, 220, 255, 255),
            pt(20, -9),
            pt(27, -8),
            2
        )


        # Silver clasp.
        pygame.draw.circle(
            surf, (183, 170, 211, 255),
            pt(-4, 0), 3
        )

        pygame.draw.circle(
            surf, (240, 233, 250, 255),
            pt(-4, 0), 1
        )

        # Tilt with vertical movement.
        angle = max(
            -18, min(18, -self.vy * 0.025)
        )

        surf = pygame.transform.rotate(surf, angle)

        screen.blit(
            surf,
            surf.get_rect(center=self.rect.center)
        )
