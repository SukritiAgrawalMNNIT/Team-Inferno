
import math
import pygame


class PauseScreen:
    def __init__(self, screen):
        self.screen = screen

        self.title_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 42
        )
        self.button_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 20
        )
        self.subtitle_font = pygame.font.Font(None, 24)

        self.resume_button = pygame.Rect(0, 0, 280, 58)
        self.menu_button = pygame.Rect(0, 0, 280, 58)

        self.hovered_button = None

    def draw(self):
        width, height = self.screen.get_size()
        cx, cy = width // 2, height // 2

        # Dark purple overlay over the gameplay
        overlay = pygame.Surface(
            (width, height), pygame.SRCALPHA
        )
        overlay.fill((8, 4, 18, 225))
        self.screen.blit(overlay, (0, 0))

        # Animated magical portal
        pulse = math.sin(pygame.time.get_ticks() * 0.002)

        for radius, color, thickness in [
            (78, (85, 35, 120), 2),
            (62, (155, 75, 195), 2),
            (46, (75, 30, 105), 1),
        ]:
            pygame.draw.circle(
                self.screen,
                color,
                (cx, cy - 125),
                int(radius + pulse * 3),
                thickness,
            )

        # Floating rune-like particles around the portal
        angle_offset = pygame.time.get_ticks() * 0.0003

        for i in range(8):
            angle = angle_offset + i * math.pi / 4

            x = cx + int(88 * math.cos(angle))
            y = cy - 125 + int(88 * math.sin(angle))

            pygame.draw.circle(
                self.screen,
                (200, 125, 230),
                (x, y),
                3,
            )

        # Title
        title = self.title_font.render(
            "REALM SUSPENDED",
            True,
            (235, 215, 250),
        )
        self.screen.blit(
            title,
            title.get_rect(center=(cx, cy - 15)),
        )

        subtitle = self.subtitle_font.render(
            "TIME STANDS STILL... FOR NOW",
            True,
            (165, 120, 190),
        )
        self.screen.blit(
            subtitle,
            subtitle.get_rect(center=(cx, cy + 25)),
        )

        # Buttons
        self.resume_button.center = (cx, cy + 95)
        self.menu_button.center = (cx, cy + 170)

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

    def draw_button(self, rect, text, button_name):
        hovered = self.hovered_button == button_name

        if hovered:
            fill = (60, 30, 80)
            border = (205, 125, 240)
            text_color = (255, 240, 255)
        else:
            fill = (23, 15, 34)
            border = (105, 65, 135)
            text_color = (215, 195, 230)

        pygame.draw.rect(
            self.screen, fill, rect, border_radius=5
        )
        pygame.draw.rect(
            self.screen, border, rect, 2, border_radius=5
        )

        label = self.button_font.render(
            text, True, text_color
        )
        self.screen.blit(
            label, label.get_rect(center=rect.center)
        )

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.resume_button.collidepoint(event.pos):
                self.hovered_button = "resume"
            elif self.menu_button.collidepoint(event.pos):
                self.hovered_button = "menu"
            else:
                self.hovered_button = None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.resume_button.collidepoint(event.pos):
                return "resume"
            elif self.menu_button.collidepoint(event.pos):
                return "menu"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "resume"

        return None
