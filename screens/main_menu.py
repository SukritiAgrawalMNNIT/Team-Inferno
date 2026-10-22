
import math
import random
import pygame


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.title_font = pygame.font.Font("assets/fonts/Cinzel-Regular.ttf", 52)
        self.subtitle_font = pygame.font.Font("assets/fonts/Cinzel-Regular.ttf", 22)
        self.button_font = pygame.font.Font(None, 34)
        self.small_font = pygame.font.Font(None, 22)

        self.start_button = pygame.Rect(0, 0, 250, 58)
        self.quit_button = pygame.Rect(0, 0, 250, 58)
        self.hovered_button = None

        random.seed(10)
        self.particles = [
            [
                random.randint(0, self.width),
                random.randint(0, self.height),
                random.uniform(0.3, 1.0),
                random.randint(1, 3),
            ]
            for _ in range(65)
        ]

    def draw(self):
        width, height = self.screen.get_size()
        self.screen.fill((10, 7, 19))

        # Background mist
        mist = pygame.Surface((width, height), pygame.SRCALPHA)

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
        cx = width // 2
        cy = height // 2 - 65
        pulse = math.sin(pygame.time.get_ticks() * 0.002)

        glow = pygame.Surface((width, height), pygame.SRCALPHA)

        pygame.draw.circle(
            glow, (100, 25, 160, 24),
            (cx, cy), int(105 + pulse * 5)
        )
        pygame.draw.circle(
            glow, (130, 45, 200, 32),
            (cx, cy), int(82 + pulse * 4)
        )

        self.screen.blit(glow, (0, 0))

        # Portal rings
        for radius, color, thickness in [
            (78, (95, 45, 145), 3),
            (67, (155, 75, 205), 2),
            (54, (90, 45, 145), 2),
        ]:
            pygame.draw.circle(
                self.screen, color, (cx, cy),
                int(radius + pulse * 2), thickness
            )

        # Rotating-looking rune marks
        angle = pygame.time.get_ticks() * 0.0003

        for i in range(8):
            a = angle + i * math.pi / 4
            x = cx + int(91 * math.cos(a))
            y = cy + int(91 * math.sin(a))

            pygame.draw.circle(
                self.screen, (195, 120, 235), (x, y), 3
            )

        # Floating magical particles
        for particle in self.particles:
            x, y, speed, radius = particle

            particle[1] -= speed
            if particle[1] < -5:
                particle[1] = height + 5
                particle[0] = random.randint(0, width)

            pygame.draw.circle(
                self.screen,
                (135, 85, 180),
                (int(x), int(y)),
                radius,
            )

        # Game title
        title = self.title_font.render(
            "CLOAK OF CHAOS", True, (232, 216, 248)
        )
        self.screen.blit(
            title,
            title.get_rect(center=(cx, 95))
        )

        subtitle = self.subtitle_font.render(
            "R I F T   R U N N E R",
            True, (177, 125, 210)
        )
        self.screen.blit(
            subtitle,
            subtitle.get_rect(center=(cx, 140))
        )

        # Buttons
        self.start_button.center = (cx, height // 2 + 85)
        self.quit_button.center = (cx, height // 2 + 155)

        self.draw_button(self.start_button, "ENTER THE RIFT", "start")
        self.draw_button(self.quit_button, "ABANDON REALM", "quit")

        footer = self.small_font.render(
            "THE DIMENSION IS CALLING",
            True, (105, 85, 125)
        )
        self.screen.blit(
            footer,
            footer.get_rect(center=(cx, height - 28))
        )

    def draw_button(self, rect, text, button_name):
        hovered = self.hovered_button == button_name

        if hovered:
            fill = (54, 27, 76)
            border = (200, 120, 245)
            text_color = (255, 240, 255)
        else:
            fill = (24, 17, 35)
            border = (100, 65, 130)
            text_color = (213, 195, 229)

        pygame.draw.rect(
            self.screen, fill, rect, border_radius=5
        )
        pygame.draw.rect(
            self.screen, border, rect,
            width=2, border_radius=5
        )

        label = self.button_font.render(
            text, True, text_color
        )
        self.screen.blit(
            label, label.get_rect(center=rect.center)
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.start_button.collidepoint(event.pos):
                self.hovered_button = "start"
            elif self.quit_button.collidepoint(event.pos):
                self.hovered_button = "quit"
            else:
                self.hovered_button = None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_button.collidepoint(event.pos):
                return "start"
            if self.quit_button.collidepoint(event.pos):
                return "quit"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "start"
            if event.key == pygame.K_ESCAPE:
                return "quit"

        return None
