
import math
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

        self.restart_button = pygame.Rect(0, 0, 270, 58)
        self.menu_button = pygame.Rect(0, 0, 270, 58)

        self.hovered_button = None
        self.score = 0

    def set_score(self, score):
        self.score = score

    def draw(self):
        width, height = self.screen.get_size()
        cx = width // 2
        cy = height // 2

        # Dark fantasy background
        self.screen.fill((10, 7, 19))

        # Purple magical glow
        glow = pygame.Surface((width, height), pygame.SRCALPHA)
        pulse = math.sin(pygame.time.get_ticks() * 0.002)

        pygame.draw.circle(
            glow,
            (100, 25, 150, 22),
            (cx, cy - 100),
            int(125 + pulse * 6),
        )
        self.screen.blit(glow, (0, 0))

        # Broken-looking magical portal rings
        for radius, color, thickness in [
            (85, (85, 35, 125), 2),
            (70, (145, 65, 185), 2),
            (55, (75, 35, 110), 1),
        ]:
            pygame.draw.circle(
                self.screen,
                color,
                (cx, cy - 105),
                int(radius + pulse * 2),
                thickness,
            )

        # Floating rune-like particles
        for i in range(8):
            angle = (
                i * math.pi / 4
                + pygame.time.get_ticks() * 0.0003
            )
            x = cx + int(95 * math.cos(angle))
            y = cy - 105 + int(95 * math.sin(angle))

            pygame.draw.circle(
                self.screen, (180, 100, 215), (x, y), 3
            )

        # Game over title
        title = self.title_font.render(
            "REALM COLLAPSED", True, (235, 210, 245)
        )
        self.screen.blit(
            title, title.get_rect(center=(cx, cy - 120))
        )

        subtitle = self.subtitle_font.render(
            "YOUR JOURNEY ENDS... FOR NOW",
            True, (165, 115, 190)
        )
        self.screen.blit(
            subtitle, subtitle.get_rect(center=(cx, cy - 75))
        )

        # Score
        score_text = self.score_font.render(
            f"RIFT SCORE: {self.score}",
            True, (225, 205, 240)
        )
        self.screen.blit(
            score_text, score_text.get_rect(center=(cx, cy - 15))
        )

        # Buttons
        self.restart_button.center = (cx, cy + 65)
        self.menu_button.center = (cx, cy + 140)

        self.draw_button(
            self.restart_button, "ENTER THE RIFT AGAIN", "restart"
        )
        self.draw_button(
            self.menu_button, "RETURN TO REALM", "menu"
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
            if self.restart_button.collidepoint(event.pos):
                self.hovered_button = "restart"
            elif self.menu_button.collidepoint(event.pos):
                self.hovered_button = "menu"
            else:
                self.hovered_button = None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
