
import math
import random
import pygame

from screens.main_menu import MainMenu
from screens.pause_screen import PauseScreen
from screens.game_over import GameOverScreen
from high_score_storage import HighScoreStorage


class ScreenManager:
    def __init__(self):
        pygame.init()

        # Fullscreen display
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h

        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            pygame.FULLSCREEN
        )

        self.width, self.height = self.screen.get_size()
        pygame.display.set_caption("Cloak of Chaos: Rift Runner")

        self.clock = pygame.time.Clock()
        self.running = True
        self.current_screen = "menu"
        self.game_time = 0.0

        # High score storage
        self.high_score_storage = HighScoreStorage()
        self.high_score = self.high_score_storage.load()

        # Screen objects
        self.menu = MainMenu(self.screen, self.high_score)
        self.pause_screen = PauseScreen(self.screen)
        self.game_over_screen = GameOverScreen(self.screen)

        # Fonts
        self.font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 32
        )
        self.hud_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 22
        )
        self.small_font = pygame.font.Font(None, 24)

        # Floating magical particles
        self.particles = []

        for _ in range(50):
            self.particles.append([
                random.randint(0, self.width),
                random.randint(0, self.height),
                random.uniform(0.4, 1.2),
                random.randint(1, 3),
            ])

    def draw_cloak(self, x, y):
        # Soft purple glow
        pygame.draw.circle(
            self.screen, (38, 15, 55), (x, y), 24
        )

        # Flowing cloak
        cloak_points = [
            (x - 9, y - 2),
            (x + 9, y - 2),
            (x + 14, y + 17),
            (x + 5, y + 14),
            (x, y + 22),
            (x - 7, y + 14),
            (x - 15, y + 17),
        ]

        pygame.draw.polygon(
            self.screen, (25, 15, 36), cloak_points
        )

        pygame.draw.lines(
            self.screen, (115, 45, 155),
            True, cloak_points, 1
        )

        # Hood
        pygame.draw.circle(
            self.screen, (28, 17, 40), (x, y - 7), 12
        )
        pygame.draw.circle(
            self.screen, (125, 55, 165),
            (x, y - 7), 12, 1
        )

        # Dark face opening
        pygame.draw.ellipse(
            self.screen, (5, 3, 10),
            (x + 1, y - 13, 9, 12)
        )

        # Glowing violet eye
        pygame.draw.circle(
            self.screen, (210, 125, 255),
            (x + 7, y - 7), 2
        )

    def draw_game(self):
        # Background
        self.screen.fill((10, 7, 19))

        cx = self.width // 2
        cy = self.height // 2

        # Animated portal
        pulse = math.sin(pygame.time.get_ticks() * 0.002)

        pygame.draw.circle(
            self.screen, (45, 18, 65),
            (cx, cy), int(100 + pulse * 5), 2
        )
        pygame.draw.circle(
            self.screen, (95, 40, 130),
            (cx, cy), int(75 + pulse * 3), 2
        )
        pygame.draw.circle(
            self.screen, (145, 70, 180), (cx, cy), 3
        )

        # Floating particles
        for particle in self.particles:
            x, y, speed, radius = particle
            particle[1] -= speed

            if particle[1] < 0:
                particle[1] = self.height
                particle[0] = random.randint(0, self.width)

            pygame.draw.circle(
                self.screen,
                (135, 75, 175),
                (int(particle[0]), int(particle[1])),
                radius
            )

        # Temporary gameplay message
        message = self.font.render(
            "THE RIFT AWAITS", True, (225, 205, 240)
        )
        self.screen.blit(
            message, message.get_rect(center=(cx, cy - 15))
        )

        hint = self.small_font.render(
            "Gameplay will be connected here",
            True, (155, 120, 175)
        )
        self.screen.blit(
            hint, hint.get_rect(center=(cx, cy + 25))
        )

        # Score HUD
        hud_rect = pygame.Rect(20, 20, 220, 48)

        pygame.draw.rect(
            self.screen, (23, 15, 34),
            hud_rect, border_radius=5
        )
        pygame.draw.rect(
            self.screen, (105, 65, 135),
            hud_rect, width=2, border_radius=5
        )

        score_text = self.hud_font.render(
            "RIFT SCORE: 0", True, (220, 195, 240)
        )
        self.screen.blit(
            score_text,
            score_text.get_rect(center=hud_rect.center)
        )

        # Survival timer
        total_seconds = int(self.game_time)
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        timer_text = self.hud_font.render(
            f"TIME: {minutes:02d}:{seconds:02d}",
            True, (235, 195, 110)
        )

        # Put timer near the top-right corner
        timer_rect = timer_text.get_rect(
            topright=(self.width - 32, 32)
        )

        timer_bg = timer_rect.inflate(28, 18)

        pygame.draw.rect(
            self.screen, (23, 15, 34),
            timer_bg, border_radius=5
        )
        pygame.draw.rect(
            self.screen, (190, 145, 75),
            timer_bg, width=2, border_radius=5
        )

        self.screen.blit(timer_text, timer_rect)

        # Pause hint
        pause_hint = self.small_font.render(
            "ESC  |  PAUSE", True, (135, 105, 155)
        )
        self.screen.blit(
            pause_hint,
            pause_hint.get_rect(
                bottomright=(self.width - 20, self.height - 18)
            )
        )

        # Cloak character
        self.draw_cloak(260, self.height // 2)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            # Timer advances only during active gameplay
            if self.current_screen == "game":
                self.game_time += dt

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    continue

                # Toggle fullscreen
                if (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_F11
                ):
                    pygame.display.toggle_fullscreen()
                    self.width, self.height = self.screen.get_size()
                    continue

                if self.current_screen == "menu":
                    action = self.menu.handle_event(event)

                    if action == "start":
                        self.game_time = 0.0
                        self.current_screen = "game"

                    elif action == "quit":
                        self.running = False

                elif self.current_screen == "game":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.current_screen = "pause"

                        elif event.key == pygame.K_g:
                            self.game_over_screen.set_score(42)
                            self.current_screen = "game_over"

                elif self.current_screen == "pause":
                    action = self.pause_screen.handle_event(event)

                    if action == "resume":
                        self.current_screen = "game"

                    elif action == "menu":
                        self.current_screen = "menu"

                elif self.current_screen == "game_over":
                    action = self.game_over_screen.handle_event(event)

                    if action == "restart":
                        self.game_time = 0.0
                        self.current_screen = "game"

                    elif action == "menu":
                        self.current_screen = "menu"

            # Draw current screen
            if self.current_screen == "menu":
                self.menu.draw()

            elif self.current_screen == "game":
                self.draw_game()

            elif self.current_screen == "pause":
                self.draw_game()
                self.pause_screen.draw()

            elif self.current_screen == "game_over":
                self.game_over_screen.draw()

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = ScreenManager()
    game.run()
