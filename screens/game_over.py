
import math
import random
import pygame


class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen

        self.title_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 46
        )
        self.score_font = pygame.font.Font(None, 38)
        self.button_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 21
        )
        self.subtitle_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)

        self.restart_button = pygame.Rect(0, 0, 270, 58)
        self.menu_button = pygame.Rect(0, 0, 270, 58)

        self.hovered_button = None
        self.score = 0

        # Decorative particles
        random.seed(17)
        self.particles = []

        for _ in range(65):
            self.particles.append({
                "x": random.random(),
                "y": random.random(),
                "size": random.choice([1, 1, 2, 3]),
                "speed": random.uniform(8, 24),
                "phase": random.uniform(0, math.tau),
            })

        random.seed()

    def set_score(self, score):
        self.score = score

    def draw(self):
        width, height = self.screen.get_size()
        cx = width // 2
        cy = height // 2

        ticks = pygame.time.get_ticks()
        pulse = math.sin(ticks * 0.0018)

        # Dark fantasy background
        self.screen.fill((9, 7, 17))

        # Soft red-purple atmospheric glow
        glow = pygame.Surface(
            (width, height), pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (100, 20, 65, 18),
            (cx, cy - 90),
            int(220 + pulse * 10),
        )

        pygame.draw.circle(
            glow,
            (75, 30, 125, 15),
            (cx, cy + 100),
            int(190 + pulse * 8),
        )

        self.screen.blit(glow, (0, 0))

        # Subtle background grid
        grid_color = (22, 17, 34)

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

        # Animated fading embers
        for particle in self.particles:
            x = int(particle["x"] * width)
            y = int(
                (particle["y"] * height
                 - ticks * particle["speed"] / 1000)
                % height
            )

            shimmer = (
                math.sin(
                    ticks * 0.003 + particle["phase"]
                ) + 1
            ) / 2

            red = int(100 + shimmer * 90)
            green = int(35 + shimmer * 45)
            blue = int(90 + shimmer * 65)

            pygame.draw.circle(
                self.screen,
                (red, green, blue),
                (x, y),
                particle["size"],
            )

        # Decorative outer frame
        margin = 30
        frame_color = (57, 37, 75)

        pygame.draw.rect(
            self.screen,
            frame_color,
            (margin, margin, width - margin * 2,
             height - margin * 2),
            1,
        )

        # Corner ornaments
        corner_length = 24
        bright_frame = (125, 76, 145)

        corners = [
            (margin, margin, 1, 1),
            (width - margin, margin, -1, 1),
            (margin, height - margin, 1, -1),
            (width - margin, height - margin, -1, -1),
        ]

        for x, y, dx, dy in corners:
            pygame.draw.line(
                self.screen, bright_frame,
                (x, y), (x + dx * corner_length, y), 2
            )
            pygame.draw.line(
                self.screen, bright_frame,
                (x, y), (x, y + dy * corner_length), 2
            )

        # Magical portal rings
        portal_y = cy - 135

        for radius, color, thickness in [
            (82, (65, 30, 95), 1),
            (70, (125, 55, 145), 2),
            (57, (75, 35, 105), 1),
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
            end_angle = start_angle + 0.48

            rect = pygame.Rect(
                cx - 91, portal_y - 91, 182, 182
            )

            pygame.draw.arc(
                self.screen,
                (155, 75, 170),
                rect,
                start_angle,
                end_angle,
                2,
            )

        # Small magical runes around the portal
        for i in range(8):
            angle = (
                i * math.pi / 4 + ticks * 0.0003
            )

            x = cx + int(100 * math.cos(angle))
            y = portal_y + int(100 * math.sin(angle))

            pygame.draw.circle(
                self.screen, (170, 100, 195),
                (x, y), 2
            )

            pygame.draw.line(
                self.screen,
                (90, 55, 120),
                (x - 4, y - 5),
                (x + 4, y + 5),
                1,
            )

        # Game over title
        title = self.title_font.render(
            "REALM COLLAPSED",
            True,
            (240, 215, 245),
        )

        self.screen.blit(
            title,
            title.get_rect(center=(cx, cy - 155)),
        )

        # Decorative divider
        divider_y = cy - 113

        pygame.draw.line(
            self.screen, (95, 57, 115),
            (cx - 180, divider_y),
            (cx - 35, divider_y), 1
        )

        pygame.draw.polygon(
            self.screen, (180, 125, 195),
            [
                (cx, divider_y - 5),
                (cx + 5, divider_y),
                (cx, divider_y + 5),
                (cx - 5, divider_y),
            ]
        )

        pygame.draw.line(
            self.screen, (95, 57, 115),
            (cx + 35, divider_y),
            (cx + 180, divider_y), 1
        )

        subtitle = self.subtitle_font.render(
            "YOUR JOURNEY ENDS... FOR NOW",
            True,
            (170, 125, 190),
        )

        self.screen.blit(
            subtitle,
            subtitle.get_rect(center=(cx, cy - 88)),
        )

        # Score panel
        panel = pygame.Rect(
            cx - 190, cy - 60, 380, 88
        )

        pygame.draw.rect(
            self.screen,
            (17, 12, 27),
            panel,
            border_radius=8,
        )

        pygame.draw.rect(
            self.screen,
            (90, 57, 115),
            panel,
            1,
            border_radius=8,
        )

        score_label = self.small_font.render(
            "YOUR RIFT SCORE",
            True,
            (155, 125, 175),
        )

        self.screen.blit(
            score_label,
            score_label.get_rect(
                center=(cx, panel.top + 24)
            ),
        )

        score_text = self.score_font.render(
            str(self.score),
            True,
            (235, 215, 250),
        )

        self.screen.blit(
            score_text,
            score_text.get_rect(
                center=(cx, panel.top + 59)
            ),
        )

        # Buttons
        self.restart_button.center = (cx, cy + 75)
        self.menu_button.center = (cx, cy + 145)

        self.draw_button(
            self.restart_button,
            "ENTER THE RIFT AGAIN",
            "restart",
        )

        self.draw_button(
            self.menu_button,
            "RETURN TO REALM",
            "menu",
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
            if self.restart_button.collidepoint(event.pos):
                self.hovered_button = "restart"
            elif self.menu_button.collidepoint(event.pos):
                self.hovered_button = "menu"
            else:
                self.hovered_button = None

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if self.restart_button.collidepoint(event.pos):
                return "restart"

            elif self.menu_button.collidepoint(event.pos):
                return "menu"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "restart"

            elif event.key == pygame.K_ESCAPE:
                return "menu"

        return None
