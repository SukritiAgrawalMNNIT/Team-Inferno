
import math
import pygame
from settings import *
from player import Player
from score_manager import ScoreManager
from difficulty_manager import DifficultyManager
from power_up import TimeStoneEffect
from barrier_spawner import BarrierSpawner
from screens.main_menu import MainMenu
from screens.game_over import GameOverScreen
from screens.pause_screen import PauseScreen

DEBUG = False

WHITE = (255, 255, 255)
GOLD = (240, 190, 60)
RED_WARN = (255, 100, 100)
GREEN_OK = (130, 225, 150)
POPUP_TIME = 0.8


def ask(screen_obj, event):
    action = screen_obj.handle_event(event)
    if action is None or action is False:
        return ""
    text = str(action).lower()
    if DEBUG:
        print("screen action:", text)
    return text


def has(text, *words):
    return any(word in text for word in words)


def safe_update(screen_obj, dt):
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

        self.font = pygame.font.Font("assets/fonts/Cinzel-Regular.ttf", 20)
        self.big_font = pygame.font.Font("assets/fonts/Cinzel-Regular.ttf", 42)
        self.small_font = pygame.font.Font("assets/fonts/Cinzel-Regular.ttf", 15)

        self.player = Player()
        self.score_manager = ScoreManager()
        self.difficulty = DifficultyManager()
        self.power_up = TimeStoneEffect()
        self.spawner = BarrierSpawner()

        self.menu = MainMenu(self.screen)
        self.game_over_screen = GameOverScreen(self.screen)
        self.pause_screen = PauseScreen(self.screen)

        self.popups = []
        self.show_debug = False
        self.final_score = 0
        self.final_best = self.score_manager.high_score
        self.final_record = False
        self.final_saved = None

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
        is_record = self.score_manager.end_run()
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
        return self.difficulty.speed * self.power_up.multiplier

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
            self.start_run()

    # ---------- floating score popups ----------
    def add_popup(self, text, x, y):
        self.popups.append({"text": text, "x": x, "y": y, "age": 0.0})

    def update_popups(self, dt):
        for popup in self.popups:
            popup["age"] += dt
            popup["y"] -= 60 * dt
        self.popups = [p for p in self.popups if p["age"] < POPUP_TIME]

    # ---------- update ----------
    def update_playing(self, dt):
        self.player.update(dt)
        self.power_up.update(dt)

        self.spawner.update(
            dt,
            self.current_speed(),
            self.difficulty.gap_size
        )

        # Collecting the Time Stone activates slow motion.
        if self.spawner.stone_collected(self.player.rect):
            self.power_up.activate()

        passed = self.spawner.count_passed(self.player.rect)
        for _ in range(passed):
            self.score_manager.add_point()
            self.difficulty.on_score(self.score_manager.score)
            self.add_popup(
                "+1",
                self.player.rect.right + 10,
                self.player.rect.top - 10
            )

        self.update_popups(dt)

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
    def draw_text(self, text, x, y, color=(195, 175, 215)):
        image = self.font.render(text, True, color)
        self.screen.blit(image, (x, y))

    def draw_center(self, text, y, font, color):
        image = font.render(text, True, color)
        self.screen.blit(image, image.get_rect(center=(WIDTH // 2, y)))

    def draw_panel(self, x, y, w, h, alpha=150):
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, alpha))
        self.screen.blit(panel, (x, y))

    def draw_popups(self):
        for popup in self.popups:
            fade = 1 - popup["age"] / POPUP_TIME
            image = self.font.render(popup["text"], True, GOLD)
            image.set_alpha(int(255 * fade))
            self.screen.blit(image, (popup["x"], popup["y"]))

    # ---------- drawing ----------
    def draw_world(self):
        self.screen.fill(BG_COLOR)
        self.spawner.draw(self.screen)
        self.player.draw(self.screen)
        self.draw_popups()

        self.draw_center(
            str(self.score_manager.score),
            45,
            self.big_font,
            (232, 195, 115)
        )

        if self.score_manager.new_record:
            pulse = 0.75 + 0.25 * math.sin(
                pygame.time.get_ticks() / 150
            )
            colour = (
                int(232 * pulse),
                int(195 * pulse),
                int(115 * pulse)
            )
            self.draw_center("NEW RECORD!", 88, self.font, colour)

        lavender = (195, 175, 215)
        gold = (232, 195, 115)

        self.draw_text(
            f"HIGH SCORE: {self.score_manager.high_score}",
            20, 20, color=gold
        )
        self.draw_text(
            f"BARRIER SPEED: {self.current_speed():.0f}",
            20, 50, color=lavender
        )
        self.draw_text(
            f"GAP SIZE: {self.difficulty.gap_size}",
            20, 80, color=lavender
        )

        if self.power_up.active:
            self.draw_text(
                f"TIME STONE: {self.power_up.time_left:.1f}s",
                20, 110, color=gold
            )

        self.draw_center(
            "SPACE  •  FLAP       ESC  •  PAUSE       F1  •  DETAILS",
            HEIGHT - 25,
            self.small_font,
            (155, 130, 180)
        )

    def draw_game_over_info(self):
        high_score_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 24
        )
        message_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 17
        )

        self.draw_center(
            f"HIGH SCORE: {self.final_best}",
            HEIGHT - 85,
            high_score_font,
            (232, 195, 115)
        )

        if self.final_record and self.final_saved:
            message = "A NEW RECORD HAS BEEN FORGED"
            color = (232, 195, 115)
        elif self.final_record:
            message = "NEW RECORD, BUT SAVE FAILED"
            color = (210, 105, 105)
        else:
            message = "SURPASS YOUR RECORD TO CLAIM GLORY"
            color = (190, 165, 210)

        self.draw_center(message, HEIGHT - 45, message_font, color)

    def draw_debug(self):
        stone = getattr(self.spawner, "stone", None)

        lines = [
            ("RIFT DIAGNOSTICS", (232, 195, 115)),
            (f"Score: {self.score_manager.score}", (225, 210, 240)),
            (f"High score: {self.score_manager.high_score}", (232, 195, 115)),
            (f"New record: {self.score_manager.new_record}", (195, 175, 215)),
            (f"Save successful: {self.score_manager.last_save_ok}", (195, 175, 215)),
            (f"Barriers: {len(self.spawner.active_barriers())}", (195, 175, 215)),
            (f"Time Stone active: {stone.active if stone else 'N/A'}", (195, 175, 215)),
        ]

        panel_width = 330
        row_height = 25
        panel_height = len(lines) * row_height + 24
        x = WIDTH - panel_width - 15
        y = 15

        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((15, 9, 27, 225))
        self.screen.blit(panel, (x, y))

        pygame.draw.rect(
            self.screen,
            (125, 91, 145),
            (x, y, panel_width, panel_height),
            1,
            border_radius=5
        )

        for i, (line, color) in enumerate(lines):
            image = self.small_font.render(line, True, color)
            self.screen.blit(image, (x + 14, y + 12 + i * row_height))

    def draw(self):
        if self.state == "menu":
            self.menu.draw()
        elif self.state == "playing":
            self.draw_world()
        elif self.state == "paused":
            self.draw_world()
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
