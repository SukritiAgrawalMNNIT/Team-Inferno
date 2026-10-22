import pygame
from settings import *
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cloak of Chaos - Rift Runner")
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.thrust()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.thrust()

    def update(self, dt):
        self.player.update(dt)
        if self.player.hits_bounds():
            self.player.reset()   # temporary; becomes game over on Day 2

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.player.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, 0.05)  # seconds, capped
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()