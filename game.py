import pygame
from settings import *
from player import Player
from score_manager import ScoreManager
from difficulty_manager import DifficultyManager
from power_up import PowerUp
from screens.main_menu import MainMenu
from screens.game_over import GameOverScreen
from screens.pause_screen import PauseScreen

# Set to True to print every action the screens send (helps if a button does nothing)
DEBUG = True


def ask(screen_obj, event):
    """Send an event to a screen. Returns its action as lowercase text, or "" if none."""
    action = screen_obj.handle_event(event)
    if action is None or action is False:
        return ""
    text = str(action).lower()
    if DEBUG:
        print("screen action:", text)
    return text


def has(text, *words):
    """True if any of the words appears in the action text."""
    for word in words:
        if word in text:
            return True
    return False


def safe_update(screen_obj, dt):
    """Call update(dt) if the screen has it."""
    if hasattr(screen_obj, "update"):
        try:
            screen_obj.update(dt)
        except TypeError:
            screen_obj.update()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Cloak of Chaos - Rift Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 30)

        # Game objects
        self.player = Player()
        self.score_manager = ScoreManager()
        self.difficulty = DifficultyManager()
        self.power_up = PowerUp()

        # Screens
        self.menu = MainMenu(self.screen)
        self.game_over_screen = GameOverScreen(self.screen)
        self.pause_screen = PauseScreen(self.screen)

        # state is one of: "menu", "playing", "paused", "game_over"
        self.state = "menu"
        self.running = True

    # ---------- changing state ----------
    def start_run(self):
        self.score_manager.reset()
        self.difficulty.reset()
        self.power_up.reset()
        self.player.reset()
        self.state = "playing"

    def end_run(self):
        self.score_manager.end_run()    # saves the high score if it is a new record
        self.game_over_screen.set_score(self.score_manager.score)
        self.state = "game_over"

    # ---------- events ----------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.state == "menu":
                self.on_menu_event(event)
            elif self.state == "playing":
                self.on_playing_event(event)
            elif self.state == "paused":
                self.on_paused_event(event)
            elif self.state == "game_over":
                self.on_game_over_event(event)

    def on_menu_event(self, event):
        action = ask(self.menu, event)
        if has(action, "start", "play"):
            self.start_run()
        elif has(action, "quit", "exit"):
            self.running = False

    def on_playing_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.thrust()
            elif event.key == pygame.K_ESCAPE:
                self.state = "paused"
            elif event.key == pygame.K_o:
                # TEST KEY: pretend we passed a gap (until barriers exist)
                self.score_manager.add_point()
                self.difficulty.update(self.score_manager.score)
            elif event.key == pygame.K_t:
                # TEST KEY: pretend we collected the Time Stone
                self.power_up.activate()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.player.thrust()

    def on_paused_event(self, event):
        action = ask(self.pause_screen, event)
        if has(action, "resume", "continue"):
            self.state = "playing"
        elif has(action, "menu"):
            self.state = "menu"
        elif has(action, "quit", "exit"):
            self.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.state = "playing"

    def on_game_over_event(self, event):
        action = ask(self.game_over_screen, event)
        if has(action, "restart", "retry", "again", "start"):
            self.start_run()
        elif has(action, "menu"):
            self.state = "menu"
        elif has(action, "quit", "exit"):
            self.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.start_run()    # single key restart (rule B3)

    # ---------- update ----------
    def update(self, dt):
        if self.state == "menu":
            safe_update(self.menu, dt)
        elif self.state == "playing":
            self.player.update(dt)
            self.power_up.update(dt)
            if self.player.hits_bounds():
                self.end_run()
        elif self.state == "paused":
            safe_update(self.pause_screen, dt)
        elif self.state == "game_over":
            safe_update(self.game_over_screen, dt)

    # ---------- drawing ----------
    def draw_text(self, text, x, y):
        image = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(image, (x, y))

    def draw_world(self):
        self.screen.fill(BG_COLOR)
        self.player.draw(self.screen)

        speed = self.difficulty.get_speed() * self.power_up.speed_multiplier()
        self.draw_text(f"Score: {self.score_manager.score}", 20, 20)
        self.draw_text(f"High score: {self.score_manager.high_score}", 20, 50)
        self.draw_text(f"Barrier speed: {speed:.0f}", 20, 80)
        self.draw_text(f"Gap size: {self.difficulty.get_gap()}", 20, 110)
        if self.power_up.active:
            self.draw_text(f"Time Stone: {self.power_up.timer:.1f}s", 20, 140)
        self.draw_text("O = test point   T = test Time Stone   Esc = pause",
                       20, HEIGHT - 40)

    def draw(self):
        if self.state == "menu":
            self.menu.draw()
        elif self.state == "playing":
            self.draw_world()
        elif self.state == "paused":
            self.draw_world()               # the game stays visible behind the pause screen
            self.pause_screen.draw()
        elif self.state == "game_over":
            self.draw_world()
            self.game_over_screen.draw()
        pygame.display.flip()

    # ---------- main loop ----------
    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, 0.05)
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()