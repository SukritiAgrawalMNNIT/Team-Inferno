
import math
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

        # Buttons
        self.resume_button = pygame.Rect(0, 0, 280, 58)
        self.menu_button = pygame.Rect(0, 0, 280, 58)
        self.hovered_button = None

    def draw(self):
        width, height = self.screen.get_size()
        cx, cy = width // 2, height // 2

        # Dark overlay â€” gameplay remains visible behind it
        overlay = pygame.Surface(
            (width, height), pygame.SRCALPHA
        )
        overlay.fill((8, 5, 16, 215))
        self.screen.blit(overlay, (0, 0))

        # Subtle animated portal
        pulse = math.sin(pygame.time.get_ticks() * 0.002)
        portal_y = cy - 125

        for radius, color, thickness in [
            (78, (75, 35, 105), 2),
            (62, (125, 65, 155), 1),
            (46, (65, 30, 90), 1),
        ]:
            pygame.draw.circle(
                self.screen,
                color,
                (cx, portal_y),
                int(radius + pulse * 2),
                thickness,
            )

        # Rotating rune marks
        angle_offset = pygame.time.get_ticks() * 0.0003

        for i in range(8):
            angle = angle_offset + i * math.pi / 4
            x = cx + int(88 * math.cos(angle))
            y = portal_y + int(88 * math.sin(angle))

            pygame.draw.circle(
                self.screen,
                (170, 115, 200),
                (x, y),
                2,
            )

        # Pause heading
        title = self.title_font.render(
            "REALM PAUSED",
            True,
            (235, 220, 245),
        )
        self.screen.blit(
            title,
            title.get_rect(center=(cx, cy - 15)),
        )

        # Subtle gold divider
        pygame.draw.line(
            self.screen,
            (145, 112, 75),
            (cx - 55, cy + 20),
            (cx + 55, cy + 20),
            1,
        )

        subtitle = self.subtitle_font.render(
            "TIME STANDS STILL...FOR NOW",
            True,
            (175, 145, 190),
        )
        self.screen.blit(
            subtitle,
            subtitle.get_rect(center=(cx, cy + 43)),
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
        hint = pygame.font.Font(None, 20).render(
            "ESC  |  RESUME",
            True,
            (115, 100, 130),
        )
        self.screen.blit(
            hint,
            hint.get_rect(center=(cx, height - 24)),
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
            self.screen, fill, rect, border_radius=5
        )
        pygame.draw.rect(
            self.screen, border, rect,
            border_width, border_radius=5
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
