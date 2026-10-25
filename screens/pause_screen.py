
import math
import random
import pygame


class PauseScreen:
    def __init__(self, screen):
        self.screen = screen

        # Fonts
        self.title_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 42
        )
        self.button_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 20
        )
        self.subtitle_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 16
        )
        self.small_font = pygame.font.Font(None, 20)

        # Buttons
        self.resume_button = pygame.Rect(0, 0, 280, 58)
        self.menu_button = pygame.Rect(0, 0, 280, 58)
        self.hovered_button = None

        # Decorative particles
        random.seed(23)
        self.particles = []

        for _ in range(55):
            self.particles.append({
                "x": random.random(),
                "y": random.random(),
                "size": random.choice([1, 1, 2, 3]),
                "speed": random.uniform(5, 18),
                "phase": random.uniform(0, math.tau),
            })

        random.seed()

    def draw(self):
        width, height = self.screen.get_size()
        cx, cy = width // 2, height // 2
        ticks = pygame.time.get_ticks()

        # Dark overlay: gameplay remains visible
        overlay = pygame.Surface(
            (width, height), pygame.SRCALPHA
        )
        overlay.fill((8, 5, 16, 215))
        self.screen.blit(overlay, (0, 0))

        pulse = math.sin(ticks * 0.002)
        portal_y = cy - 135

        # Soft magical glow
        glow = pygame.Surface(
            (width, height), pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (85, 35, 125, 22),
            (cx, portal_y),
            int(155 + pulse * 8),
        )

        self.screen.blit(glow, (0, 0))

        # Faint background grid
        grid_color = (27, 19, 39)

        for x in range(35, width, 55):
            pygame.draw.line(
                self.screen, grid_color,
                (x, 0), (x, height), 1
            )

        for y in range(30, height, 55):
            pygame.draw.line(
                self.screen, grid_color,
                (0, y), (width, y), 1
            )

        # Floating magical particles
        for particle in self.particles:
            x = int(particle["x"] * width)

            y = int(
                (
                    particle["y"] * height
                    - ticks * particle["speed"] / 1000
                ) % height
            )

            shimmer = (
                math.sin(
                    ticks * 0.003 + particle["phase"]
                ) + 1
            ) / 2

            color = (
                int(150 + shimmer * 80),
                int(110 + shimmer * 90),
                int(40 + shimmer * 35),
            )

            pygame.draw.circle(
                self.screen,
                color,
                (x, y),
                particle["size"],
            )

        # Decorative outer frame
        margin = 30

        pygame.draw.rect(
            self.screen,
            (105, 80, 43),
            (margin, margin,
             width - 2 * margin, height - 2 * margin),
            1,
        )

        # Frame corner ornaments
        corner_length = 24
        corner_color = (125, 76, 145)

        corners = [
            (margin, margin, 1, 1),
            (width - margin, margin, -1, 1),
            (margin, height - margin, 1, -1),
            (width - margin, height - margin, -1, -1),
        ]

        for x, y, dx, dy in corners:
            pygame.draw.line(
                self.screen, corner_color,
                (x, y), (x + dx * corner_length, y), 2
            )

            pygame.draw.line(
                self.screen, corner_color,
                (x, y), (x, y + dy * corner_length), 2
            )

        # Animated portal rings
        for radius, color, thickness in [
            (78, (105, 75, 38), 2),
            (62, (185, 145, 70), 1),
            (46, (80, 55, 35), 1),
        ]:
            pygame.draw.circle(
                self.screen,
                color,
                (cx, portal_y),
                int(radius + pulse * 2),
                thickness,
            )

        # Broken portal arcs
        for i in range(6):
            start_angle = (
                i * math.tau / 6 + ticks * 0.00015
            )
            end_angle = start_angle + 0.45

            pygame.draw.arc(
                self.screen,
                (145, 75, 170),
                pygame.Rect(
                    cx - 88, portal_y - 88, 176, 176
                ),
                start_angle,
                end_angle,
                2,
            )

        # Rotating rune marks
        angle_offset = ticks * 0.0003

        for i in range(8):
            angle = angle_offset + i * math.pi / 4

            x = cx + int(95 * math.cos(angle))
            y = portal_y + int(95 * math.sin(angle))

            pygame.draw.circle(
                self.screen,
                (210, 170, 85),
                (x, y),
                2,
            )

            pygame.draw.line(
                self.screen,
                (95, 60, 125),
                (x - 4, y - 4),
                (x + 4, y + 4),
                1,
            )

        # Pause heading
        title = self.title_font.render(
            "REALM PAUSED",
            True,
            (235, 220, 245),
        )

        self.screen.blit(
            title,
            title.get_rect(center=(cx, cy - 18)),
        )

        # Decorative divider
        divider_y = cy + 17

        pygame.draw.line(
            self.screen,
            (115, 83, 135),
            (cx - 105, divider_y),
            (cx - 12, divider_y),
            1,
        )

        pygame.draw.polygon(
            self.screen,
            (205, 170, 105),
            [
                (cx, divider_y - 4),
                (cx + 4, divider_y),
                (cx, divider_y + 4),
                (cx - 4, divider_y),
            ],
        )

        pygame.draw.line(
            self.screen,
            (115, 83, 135),
            (cx + 12, divider_y),
            (cx + 105, divider_y),
            1,
        )

        subtitle = self.subtitle_font.render(
            "TIME STANDS STILL... FOR NOW",
            True,
            (175, 145, 190),
        )

        self.screen.blit(
            subtitle,
            subtitle.get_rect(center=(cx, cy + 42)),
        )

        # Buttons
        self.resume_button.center = (cx, cy + 105)
        self.menu_button.center = (cx, cy + 175)

        self.draw_button(
            self.resume_button,
            "RESUME JOURNEY",
            "resume",
        )

        self.draw_button(
            self.menu_button,
            "RETURN TO REALM",
            "menu",
        )

        # Keyboard hint
        hint = self.small_font.render(
            "ESC  |  RESUME",
            True,
            (135, 115, 150),
        )

        self.screen.blit(
            hint,
            hint.get_rect(
                center=(cx, height - 48)
            ),
        )

    def draw_button(self, rect, text, button_name):
        hovered = self.hovered_button == button_name

        if hovered:
            fill = (38, 25, 48)
            border = (205, 170, 105)
            text_color = (255, 235, 195)
            border_width = 2
        else:
            fill = (18, 12, 28)
            border = (105, 75, 125)
            text_color = (215, 195, 230)
            border_width = 1

        pygame.draw.rect(
            self.screen,
            fill,
            rect,
            border_radius=5,
        )

        pygame.draw.rect(
            self.screen,
            border,
            rect,
            border_width,
            border_radius=5,
        )

        label = self.button_font.render(
            text, True, text_color
        )

        self.screen.blit(
            label,
            label.get_rect(center=rect.center),
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.resume_button.collidepoint(event.pos):
                self.hovered_button = "resume"
            elif self.menu_button.collidepoint(event.pos):
                self.hovered_button = "menu"
            else:
                self.hovered_button = None

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if self.resume_button.collidepoint(event.pos):
                return "resume"

            if self.menu_button.collidepoint(event.pos):
                return "menu"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "resume"

        return None
