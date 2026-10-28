import math
import pygame
from settings import *


class Player:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, *PLAYER_SIZE)
        self.trail_positions = []
        self.alpha = 255          # 255 = normal, lower = see-through (Ghost Orb)
        self.reset()

    def reset(self):
        self.rect.center = (PLAYER_X, HEIGHT // 2)
        self.y = float(self.rect.y)
        self.vy = 0.0
        self.time = 0.0
        self.trail_positions.clear()
        self.alpha = 255

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

        if self.alpha >= 255:
            screen.blit(trail_surface, (0, 0))

        # --------------------------------------------------
        # 2. Flared, fluttering cloak (wider toward the tail)
        # --------------------------------------------------
        size = 240                      # bigger canvas for the larger cloak
        c = size // 2
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        head_scale = 0.62               # hood / face size
        cloak_scale = 0.77              # cloak size

        def pt(x, y):
            return (round(c + x * head_scale), round(c + y * head_scale))

        def cpt(x, y):
            return (round(c + x * cloak_scale), round(c + y * cloak_scale))

        def lerp(a, b, s):
            return a + (b - a) * s

        # A wave that travels down the cloak; grows toward the tail.
        def wave(t, phase=0.0):
            return math.sin(self.time * 7 - t * 5 + phase) * (1 + 10 * t)

        SEG = 16
        TAIL_X = -112

        def cloak_y(t, f):
            """y at position t (0 = shoulder, 1 = tail) and fraction f
            (0 = top edge, 1 = bottom edge)."""
            cy = 2 + wave(t)
            half_top = 12 + 22 * t ** 1.6      # widens toward the tail
            half_bot = 11 + 30 * t ** 1.4
            return lerp(cy - half_top, cy + half_bot, f)

        def cloak_x(t):
            return -26 + (TAIL_X + 26) * t

        top = [cpt(cloak_x(i / SEG), cloak_y(i / SEG, 0)) for i in range(SEG + 1)]
        bot = [cpt(cloak_x(i / SEG), cloak_y(i / SEG, 1)) for i in range(SEG + 1)]

        # Ragged, fluttering hem at the tail end.
        hem = []
        TEETH = 6
        for k in range(TEETH + 1):
            s = k / TEETH
            y = cloak_y(1.0, s)
            x = TAIL_X + (-9 if k % 2 == 0 else 4)
            x += math.sin(self.time * 9 + k * 1.7) * 3
            y += math.sin(self.time * 8 + k * 1.3) * 2
            hem.append(cpt(x, y))

        body = top + hem + bot[::-1] + [pt(34, -2), pt(29, -7)]

        # Opaque royal-purple fabric.
        pygame.draw.polygon(surf, (48, 32, 68, 255), body)

        # Inner lighter panel (same shape, inset).
        IN_END = 0.9
        inner_top = [
            (round(c + cloak_x(i / SEG * IN_END) * cloak_scale),
             round(c + cloak_y(i / SEG * IN_END, 0.22) * cloak_scale))
            for i in range(SEG + 1)
        ]
        inner_bot = [
            (round(c + cloak_x(i / SEG * IN_END) * cloak_scale),
             round(c + cloak_y(i / SEG * IN_END, 0.78) * cloak_scale))
            for i in range(SEG + 1)
        ]
        pygame.draw.polygon(surf, (89, 60, 125, 255), inner_top + inner_bot[::-1])

        # Fabric folds running toward the tail.
        for f, color, w in (
            (0.30, (211, 201, 229, 255), 1),
            (0.52, (48, 32, 70, 255), 2),
            (0.74, (169, 153, 199, 255), 1),
        ):
            fold = [
                (round(c + cloak_x(t) * cloak_scale), round(c + cloak_y(t, f) * cloak_scale))
                for t in [0.08 + 0.87 * i / SEG for i in range(SEG + 1)]
            ]
            pygame.draw.lines(surf, color, False, fold, w)

        # Silver outline over the whole shape.
        pygame.draw.lines(surf, (190, 180, 215, 255), True, body, 2)

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

        # Dark face opening (smoother, deeper shape).
        face = [
            pt(17, -17),
            pt(24, -15),
            pt(30, -10),
            pt(30, -4),
            pt(25, -1),
            pt(18, -3),
            pt(13, -8),
            pt(13, -13),
        ]

        pygame.draw.polygon(
            surf, (8, 6, 18, 255), face
        )

        # Soft inner shadow so the face reads as a hollow under the hood.
        shade = [
            pt(17, -17),
            pt(24, -15),
            pt(29, -11),
            pt(22, -11),
            pt(15, -12),
        ]

        pygame.draw.polygon(
            surf, (22, 16, 38, 255), shade
        )

        # Glowing cyan eye: halo, almond shape, bright core.
        ex, ey = pt(24, -8)

        glow = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(glow, (115, 220, 255, 35), (12, 12), 9)
        pygame.draw.circle(glow, (115, 220, 255, 70), (12, 12), 6)
        surf.blit(glow, (ex - 12, ey - 12))

        pygame.draw.ellipse(
            surf, (115, 220, 255, 255),
            pygame.Rect(ex - 4, ey - 2, 8, 4)
        )

        pygame.draw.ellipse(
            surf, (225, 250, 255, 255),
            pygame.Rect(ex - 1, ey - 1, 4, 2)
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
        if self.alpha < 255:
            surf.set_alpha(self.alpha)

        screen.blit(
            surf,
            surf.get_rect(center=self.rect.center)
        )