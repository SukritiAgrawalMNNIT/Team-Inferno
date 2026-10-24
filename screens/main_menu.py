
import math
import random
import pygame


class MainMenu:
    def __init__(self, screen, high_score=0):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.high_score = high_score

        # Fonts — Cinzel for the dark fantasy theme
        self.title_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 52
        )
        self.subtitle_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 22
        )
        self.score_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 24
        )
        self.button_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 21
        )
        self.small_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 14
        )

        # Buttons
        self.start_button = pygame.Rect(0, 0, 280, 58)
        self.quit_button = pygame.Rect(0, 0, 280, 58)
        self.hovered_button = None

                # Floating magical particles
        random.seed(10)
        self.particles = [
            [
                random.randint(0, self.width),
                random.randint(0, self.height),
                random.uniform(0.3, 1.0),
                random.randint(1, 3),
                random.choice([
                    (155, 100, 220),  # Mystical purple
                    (190, 145, 65),   # Antique gold
                    (115, 70, 175),   # Deep purple
                    (225, 190, 110),  # Bright gold
                ]),
            ]
            for _ in range(65)
        ]

    def draw(self):
        width, height = self.screen.get_size()
        cx = width // 2

        self.screen.fill((10, 7, 19))

        # Background mist
        mist = pygame.Surface(
            (width, height), pygame.SRCALPHA
        )

        for i in range(7):
            x = (i * 173 + 60) % width
            y = (i * 97 + 100) % height

            pygame.draw.ellipse(
                mist,
                (70, 25, 105, 18),
                (x - 160, y - 65, 320, 130),
            )

        self.screen.blit(mist, (0, 0))

        # Dimensional portal
        cy = height // 2 - 65
        pulse = math.sin(
            pygame.time.get_ticks() * 0.002
        )

        glow = pygame.Surface(
            (width, height), pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (100, 25, 160, 24),
            (cx, cy),
            int(105 + pulse * 5),
        )
        pygame.draw.circle(
            glow,
            (130, 45, 200, 32),
            (cx, cy),
            int(82 + pulse * 4),
        )

        self.screen.blit(glow, (0, 0))

        # Portal rings
        for radius, color, thickness in [
            (78, (95, 45, 145), 3),
            (67, (155, 75, 205), 2),
            (54, (90, 45, 145), 2),
        ]:
            pygame.draw.circle(
                self.screen,
                color,
                (cx, cy),
                int(radius + pulse * 2),
                thickness,
            )

        # Rotating rune marks
        angle = pygame.time.get_ticks() * 0.0003

        for i in range(8):
            a = angle + i * math.pi / 4
            x = cx + int(91 * math.cos(a))
            y = cy + int(91 * math.sin(a))

            pygame.draw.circle(
                self.screen,
                (195, 120, 235),
                (x, y),
                3,
            )

        # Floating magical particles
        for particle in self.particles:
            particle[1] -= particle[2]

            if particle[1] < -5:
                particle[1] = height + 5
                particle[0] = random.randint(0, width)

            pygame.draw.circle(
                self.screen,
                particle[4],  # Each particle's own color
                (int(particle[0]), int(particle[1])),
                particle[3],
            )

        # Game title
        title = self.title_font.render(
            "CLOAK OF CHAOS",
            True,
            (232, 195, 115),
        )
        self.screen.blit(
            title,
            title.get_rect(center=(cx, 95)),
        )

        subtitle = self.subtitle_font.render(
            "R I F T   R U N N E R",
            True,
            (177, 125, 210),
        )
        self.screen.blit(
            subtitle,
            subtitle.get_rect(center=(cx, 140)),
        )

        # Buttons
        self.start_button.center = (
            cx, height // 2 + 85
        )
        self.quit_button.center = (
            cx, height // 2 + 155
        )

        self.draw_button(
            self.start_button,
            "ENTER THE RIFT",
            "start",
        )
        self.draw_button(
            self.quit_button,
            "ABANDON REALM",
            "quit",
        )

        # High score — minimalist Cinzel
        score_text = self.score_font.render(
            f"HIGH SCORE: {self.high_score}",
            True,
            (190, 160, 110),
        )
        self.screen.blit(
            score_text,
            score_text.get_rect(
                center=(cx, height - 65)
            ),
        )

        # Footer
        footer = self.small_font.render(
            "THE DIMENSION IS CALLING",
            True,
            (105, 85, 125),
        )
        self.screen.blit(
            footer,
            footer.get_rect(
                center=(cx, height - 28)
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

        # Button background
        pygame.draw.rect(
            self.screen,
            fill,
            rect,
            border_radius=5,
        )

        # Button border
        pygame.draw.rect(
            self.screen,
            border,
            rect,
            border_width,
            border_radius=5,
        )

        # Cinzel button text
        label = self.button_font.render(
            text,
            True,
            text_color,
        )
        self.screen.blit(
            label,
            label.get_rect(center=rect.center),
        )

    def handle_event(self, event):
        # Mouse hover
        if event.type == pygame.MOUSEMOTION:
            if self.start_button.collidepoint(event.pos):
                self.hovered_button = "start"
            elif self.quit_button.collidepoint(event.pos):
                self.hovered_button = "quit"
            else:
                self.hovered_button = None

        # Mouse clicks
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if self.start_button.collidepoint(event.pos):
                return "start"

            if self.quit_button.collidepoint(event.pos):
                return "quit"

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "start"

            if event.key == pygame.K_ESCAPE:
                return "quit"

        return None
