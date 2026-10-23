import math
import pygame
from settings import *
from player import Player
from score_manager import ScoreManager
from difficulty_manager import DifficultyManager
from power_up import PowerUp
from barrier_spawner import BarrierSpawner
from screens.main_menu import MainMenu
from screens.game_over import GameOverScreen
from screens.pause_screen import PauseScreen

# Set to True to print every action the screens send (helps if a button does nothing)
DEBUG = False

WHITE = (255, 255, 255)
GOLD = (240, 190, 60)
RED_WARN = (255, 100, 100)
GREEN_OK = (130, 225, 150)
POPUP_TIME = 0.8          # seconds a "+1" stays on screen


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
        self.big_font = pygame.font.SysFont(None, 64)
        self.small_font = pygame.font.SysFont(None, 24)

        # Game objects
        self.player = Player()
        self.score_manager = ScoreManager()
        self.difficulty = DifficultyManager()
        self.power_up = PowerUp()
        self.spawner = BarrierSpawner()

        # Screens
        self.menu = MainMenu(self.screen)
        self.game_over_screen = GameOverScreen(self.screen)
        self.pause_screen = PauseScreen(self.screen)

        # Things shown on screen to make the scoring visible
        self.popups = []                  # floating "+1" texts
        self.show_debug = False           # F1 toggles the scoring panel
        self.final_score = 0              # result of the last run
        self.final_best = self.score_manager.high_score
        self.final_record = False
        self.final_saved = None

        # state is one of: "menu", "playing", "paused", "game_over"
        self.state = "menu"
        self.running = True

    # ---------- changing state ----------
    def start_run(self):
        self.score_manager.reset()
        self.difficulty.reset()
        self.power_up.reset()
        self.spawner.reset()
        self.player.reset()
        self.popups = []
        self.state = "playing"

    def end_run(self):
        is_record = self.score_manager.end_run()      # saves the high score if it is a new record
        self.final_score = self.score_manager.score
        self.final_best = self.score_manager.high_score
        self.final_record = is_record
        self.final_saved = self.score_manager.last_save_ok
        self.game_over_screen.set_score(self.final_score)
        if hasattr(self.game_over_screen, "set_high_score"):
            self.game_over_screen.set_high_score(self.final_best)
        self.state = "game_over"

    def current_speed(self):
        """Barrier speed, including the Time Stone slow-down."""
        return self.difficulty.get_speed() * self.power_up.speed_multiplier()

    # ---------- events ----------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                self.show_debug = not self.show_debug
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

    # ---------- floating "+1" texts ----------
    def add_popup(self, text, x, y):
        self.popups.append({"text": text, "x": x, "y": y, "age": 0.0})

    def update_popups(self, dt):
        for popup in self.popups:
            popup["age"] += dt          # gets older
            popup["y"] -= 60 * dt       # floats upward
        self.popups = [p for p in self.popups if p["age"] < POPUP_TIME]

    # ---------- update ----------
    def update_playing(self, dt):
        self.player.update(dt)
        self.power_up.update(dt)
        self.spawner.update(dt, self.current_speed(), self.difficulty.get_gap())

        # Collecting the Time Stone slows the barriers
        if self.spawner.stone_collected(self.player.rect):
            self.power_up.activate()

        # +1 point for every gap the Cloak got through
        passed = self.spawner.count_passed(self.player.rect)
        for _ in range(passed):
            self.score_manager.add_point()
            self.difficulty.update(self.score_manager.score)
            self.add_popup("+1", self.player.rect.right + 10, self.player.rect.top - 10)

        self.update_popups(dt)

        # Game over if the Cloak hits the floor, the ceiling or a barrier
        if self.player.hits_bounds() or self.spawner.hits_player(self.player.rect):
            self.end_run()

    def update(self, dt):
        if self.state == "menu":
            safe_update(self.menu, dt)
        elif self.state == "playing":
            self.update_playing(dt)
        elif self.state == "paused":
            safe_update(self.pause_screen, dt)
        elif self.state == "game_over":
            safe_update(self.game_over_screen, dt)

    # ---------- drawing helpers ----------
    def draw_text(self, text, x, y):
        image = self.font.render(text, True, WHITE)
        self.screen.blit(image, (x, y))

    def draw_center(self, text, y, font, color):
        image = font.render(text, True, color)
        self.screen.blit(image, image.get_rect(center=(WIDTH // 2, y)))

    def draw_panel(self, x, y, w, h, alpha=150):
        """A dark see-through box so text stays readable."""
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, alpha))
        self.screen.blit(panel, (x, y))

    def draw_popups(self):
        for popup in self.popups:
            fade = 1 - popup["age"] / POPUP_TIME      # 1 = clear, 0 = invisible
            image = self.font.render(popup["text"], True, GOLD)
            image.set_alpha(int(255 * fade))
            self.screen.blit(image, (popup["x"], popup["y"]))

    # ---------- drawing ----------
    def draw_world(self):
        self.screen.fill(BG_COLOR)
        self.spawner.draw(self.screen)      # barriers first, so the Cloak is in front
        self.player.draw(self.screen)
        self.draw_popups()

        # Big score in the middle at the top
        self.draw_center(str(self.score_manager.score), 45, self.big_font, WHITE)
        if self.score_manager.new_record:
            pulse = 0.6 + 0.4 * math.sin(pygame.time.get_ticks() / 150)
            colour = (int(GOLD[0] * pulse), int(GOLD[1] * pulse), int(GOLD[2] * pulse))
            self.draw_center("NEW RECORD!", 95, self.font, colour)

        # Details at the top-left
        self.draw_text(f"High score: {self.score_manager.high_score}", 20, 20)
        self.draw_text(f"Barrier speed: {self.current_speed():.0f}", 20, 50)
        self.draw_text(f"Gap size: {self.difficulty.get_gap()}", 20, 80)
        if self.power_up.active:
            self.draw_text(f"Time Stone: {self.power_up.timer:.1f}s", 20, 110)
        self.draw_text("Space = flap   Esc = pause   F1 = scoring panel", 20, HEIGHT - 40)

    def draw_game_over_info(self):
        """Extra scoring information at the bottom of the game-over screen."""
        self.draw_panel(WIDTH // 2 - 260, HEIGHT - 110, 520, 95)
        self.draw_center(f"Score: {self.final_score}     High score: {self.final_best}",
                         HEIGHT - 82, self.font, WHITE)
        if self.final_record and self.final_saved:
            self.draw_center("NEW RECORD! Saved to highscore.json", HEIGHT - 45, self.font, GOLD)
        elif self.final_record:
            self.draw_center("New record, but the file could not be saved",
                             HEIGHT - 45, self.font, RED_WARN)
        else:
            self.draw_center("Beat the high score to set a new record",
                             HEIGHT - 45, self.font, GREEN_OK)

    def draw_debug(self):
        """Press F1: shows the numbers the scoring code is working with."""
        stone = getattr(self.spawner, "stone", None)
        lines = [
            f"state: {self.state}",
            f"score: {self.score_manager.score}",
            f"high score: {self.score_manager.high_score}",
            f"new record: {self.score_manager.new_record}",
            f"last save ok: {self.score_manager.last_save_ok}",
            f"barriers on screen: {len(self.spawner.active_barriers())}",
            f"time stone on screen: {stone.active if stone else 'n/a'}",
        ]
        height = len(lines) * 22 + 14
        self.draw_panel(WIDTH - 290, 10, 280, height, 180)
        for i, line in enumerate(lines):
            image = self.small_font.render(line, True, GREEN_OK)
            self.screen.blit(image, (WIDTH - 280, 18 + i * 22))

    def draw(self):
        if self.state == "menu":
            self.menu.draw()
            self.draw_center(f"High score: {self.score_manager.high_score}", HEIGHT - 30,
                             self.font, GOLD)
        elif self.state == "playing":
            self.draw_world()
        elif self.state == "paused":
            self.draw_world()               # the game stays visible behind the pause screen
            self.pause_screen.draw()
        elif self.state == "game_over":
            self.draw_world()
            self.game_over_screen.draw()
            self.draw_game_over_info()
        if self.show_debug:
            self.draw_debug()
        pygame.display.flip()

    # ---------- main loop ----------
    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, 0.05)
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()