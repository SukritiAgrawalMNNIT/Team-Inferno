import pygame
from settings import *
from player import Player
from score_manager import ScoreManager
from difficulty_manager import DifficultyManager
from power_up import PowerUp


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cloak of Chaos - Rift Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

        self.player = Player()
        self.score_manager = ScoreManager()
        self.difficulty = DifficultyManager()
        self.power_up = PowerUp()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.thrust()
                elif event.key == pygame.K_p:
                    # TEST KEY: pretend we passed a gap
                    self.score_manager.add_point()
                    self.difficulty.update(self.score_manager.score)
                elif event.key == pygame.K_t:
                    # TEST KEY: pretend we collected the Time Stone
                    self.power_up.activate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.thrust()

    def update(self, dt):
        self.player.update(dt)
        self.power_up.update(dt)

        if self.player.hits_bounds():
            self.game_over()

    def game_over(self):
        # Save the high score if this run beat it, then start again
        self.score_manager.end_run()
        self.score_manager.reset()
        self.difficulty.reset()
        self.power_up.reset()
        self.player.reset()

    def draw_text(self, text, x, y):
        image = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(image, (x, y))

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.player.draw(self.screen)

        # Show everything the logic files are tracking
        speed = self.difficulty.get_speed() * self.power_up.speed_multiplier()
        self.draw_text(f"Score: {self.score_manager.score}", 20, 20)
        self.draw_text(f"High score: {self.score_manager.high_score}", 20, 50)
        self.draw_text(f"Barrier speed: {speed:.0f}", 20, 80)
        self.draw_text(f"Gap size: {self.difficulty.get_gap()}", 20, 110)
        if self.power_up.active:
            self.draw_text(f"Time Stone: {self.power_up.timer:.1f}s", 20, 140)
        self.draw_text("P = test point   T = test Time Stone", 20, HEIGHT - 40)

        pygame.display.flip()

    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, 0.05)
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()