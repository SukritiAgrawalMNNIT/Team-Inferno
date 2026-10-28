import math
import os
import pygame
from high_score_storage import HighScoreStorage
from settings import *
from player import Player
from score_manager import ScoreManager
from difficulty_manager import DifficultyManager
from power_up import TimeStoneEffect
from ghost_orb import GhostEffect
from barrier_spawner import BarrierSpawner
from checkpoints import CheckpointManager
from background_manager import BackgroundManager
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

        # ---------- Audio setup ----------
        self.audio_dir = os.path.join("assets", "audio")
        self.sounds = {}
        self.music_available = False
        self.audio_available = False

        try:
            pygame.mixer.init()
            self.audio_available = True

            sound_files = {
                "flap": "flap.wav",
                "collect": "collect.wav",
                "score": "score.wav",
                "hit": "hit.wav",
                "game_over": "game_over.wav",
                "checkpoint": "checkpoint.wav",
            }

            for name, filename in sound_files.items():
                path = os.path.join(self.audio_dir, filename)

                if os.path.isfile(path):
                    self.sounds[name] = pygame.mixer.Sound(path)

            music_path = os.path.join(
                self.audio_dir, "ambient.wav"
            )

            if os.path.isfile(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(1.0)
                self.music_available = True

        except pygame.error as error:
            print(f"Audio unavailable: {error}")

        # ---------- Background ----------
        self.background = pygame.image.load(
            "assets/images/background1.png"
        ).convert()
        self.background = pygame.transform.scale(
            self.background, (900, 600)
        )
        self.bg_manager = BackgroundManager(self.background)

        pygame.display.set_caption("Cloak of Chaos - Rift Runner")
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 20
        )
        self.big_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 42
        )
        self.small_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 15
        )

        
# Reset the saved high score whenever the game launches
        self.high_score_storage = HighScoreStorage()
        self.high_score_storage.save(0)

        self.player = Player()
        self.score_manager = ScoreManager(self.high_score_storage)
        self.difficulty = DifficultyManager()
        self.power_up = TimeStoneEffect()
        self.ghost = GhostEffect()
        self.ghost_exiting = False   # True until the cloak is clear of barriers after the effect ends
        self.spawner = BarrierSpawner()
        self.checkpoints = CheckpointManager()

        self.menu = MainMenu(
            self.screen,
            self.score_manager.high_score
        )

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
        self.elapsed_time = 0.0
        self.play_music()

    # ---------- Audio helpers ----------
    def play_sound(self, name):
        sound = self.sounds.get(name)

        if sound:
            sound.play()

    def play_music(self):
        if not self.music_available:
            return

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    # ---------- Changing state ----------
    def start_run(self):
        self.elapsed_time = 0.0
        self.score_manager.reset()
        self.difficulty.reset()
        self.power_up.reset()
        self.ghost.reset()
        self.ghost_exiting = False
        self.spawner.reset()
        self.checkpoints.reset()
        self.bg_manager.reset()
        self.player.reset()
        self.popups = []
        self.state = "playing"

        # Start looping background music.
        self.play_music()

    def end_run(self):
        # Prevent repeated game-over sounds.
        if self.state != "playing":
            return

        is_record = self.score_manager.end_run()
        self.final_score = self.score_manager.score
        self.final_best = self.score_manager.high_score

        self.high_score = self.final_best
        self.menu.high_score = self.high_score
        self.final_record = is_record
        self.final_saved = self.score_manager.last_save_ok

        self.game_over_screen.set_score(self.final_score)

        if hasattr(self.game_over_screen, "set_high_score"):
            self.game_over_screen.set_high_score(self.final_best)

        self.play_sound("game_over")
        self.state = "game_over"

    def current_speed(self):
        """Barrier speed, including the Time Stone slow-down."""
        return self.difficulty.speed * self.power_up.multiplier

    # ---------- Events ----------
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_F1
            ):
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
                self.play_sound("flap")

            elif event.key == pygame.K_ESCAPE:
                self.state = "paused"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.player.thrust()
            self.play_sound("flap")

    def on_paused_event(self, event):
        action = ask(self.pause_screen, event)

        if has(action, "resume", "continue"):
            self.state = "playing"

        elif has(action, "menu"):
            self.state = "menu"

        elif has(action, "quit", "exit"):
            self.running = False

        elif (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            self.state = "playing"

    def on_game_over_event(self, event):
        action = ask(self.game_over_screen, event)

        if has(action, "restart", "retry", "again", "start"):
            self.start_run()

        elif has(action, "menu"):
            self.state = "menu"

        elif has(action, "quit", "exit"):
            self.running = False

        elif (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
        ):
            self.start_run()

    # ---------- Floating score popups ----------
    def add_popup(self, text, x, y, color=GOLD):
        self.popups.append({
            "text": text,
            "x": x,
            "y": y,
            "age": 0.0,
            "color": color
        })

    def update_popups(self, dt):
        for popup in self.popups:
            popup["age"] += dt
            popup["y"] -= 60 * dt

        self.popups = [
            p for p in self.popups
            if p["age"] < POPUP_TIME
        ]

    # ---------- Update ----------
    def update_playing(self, dt):
        self.bg_manager.update(dt)

        # Cut the frame into equal slices of at most PHYSICS_STEP seconds,
        # so a slow PC and a fast PC run the same simulation.
        steps = max(1, math.ceil(dt / PHYSICS_STEP))
        step_dt = dt / steps

        for _ in range(steps):
            self.step_playing(step_dt)
            if self.state != "playing":      # player died during this slice
                break

    def step_playing(self, dt):
        self.elapsed_time += dt
        self.player.update(dt)
        self.power_up.update(dt)
        self.ghost.update(dt)

        self.spawner.update(
            dt,
            self.current_speed(),
            self.difficulty.gap_size
        )

        # Collecting the Time Stone activates slow motion.
        if self.spawner.stone_collected(self.player.rect):
            self.power_up.activate()
            self.play_sound("collect")

        # Collecting the yellow Ghost Orb makes the Cloak invisible + invincible.
        if self.spawner.ghost_collected(self.player.rect):
            self.ghost.activate()
            self.add_popup(
                "GHOST!",
                self.player.rect.right + 10,
                self.player.rect.top - 10,
                (255, 215, 40)
            )
            self.play_sound("collect")

        # Collecting a red Bonus Orb gives extra points.
        if self.spawner.bonus_collected(self.player.rect):
            self.score_manager.add_points(BONUS_POINTS)
            self.difficulty.on_score(self.score_manager.score)
            self.add_popup(
                f"+{BONUS_POINTS}",
                self.player.rect.right + 10,
                self.player.rect.top - 10,
                RED_WARN
            )
            self.play_sound("collect")
            self.check_checkpoint()

        # Score for passed barriers.
        passed = self.spawner.count_passed(self.player.rect)

        for _ in range(passed):
            self.score_manager.add_point()
            self.difficulty.on_score(self.score_manager.score)

            self.add_popup(
                "+1",
                self.player.rect.right + 10,
                self.player.rect.top - 10
            )

            self.play_sound("score")

            self.check_checkpoint()

        self.checkpoints.update(dt)
        self.update_popups(dt)

        # Collision detection (barriers are harmless while the Ghost effect is on).
        if self.ghost.active:
            self.ghost_exiting = True
            # Can't fly out of the screen either: stay inside while invincible.
            if self.player.rect.top < 0:
                self.player.y = 0.0
                self.player.vy = 0.0
                self.player.rect.y = 0
            elif self.player.rect.bottom > HEIGHT:
                self.player.y = float(HEIGHT - self.player.rect.height)
                self.player.vy = 0.0
                self.player.rect.y = round(self.player.y)
        else:
            if self.ghost_exiting:
                # Effect just ended: stay safe from barriers until fully clear of them.
                if not self.spawner.hits_player(self.player.rect):
                    self.ghost_exiting = False
                barrier_hit = False
            else:
                barrier_hit = self.spawner.hits_player(self.player.rect)

            if self.player.hits_bounds() or barrier_hit:
                self.play_sound("hit")
                self.end_run()

    def check_checkpoint(self):
        """Fires once per milestone (also after a bonus jump in score)."""
        if self.checkpoints.check(self.score_manager.score):
            self.bg_manager.set_stage(self.checkpoints.reached)
            if "checkpoint" in self.sounds:
                self.play_sound("checkpoint")
            else:
                self.play_sound("collect")

    def update(self, dt):
        if self.state == "menu":
            safe_update(self.menu, dt)

        elif self.state == "playing":
            self.update_playing(dt)

        elif self.state == "paused":
            safe_update(self.pause_screen, dt)

        elif self.state == "game_over":
            safe_update(self.game_over_screen, dt)

    # ---------- Drawing helpers ----------
    def draw_text(self, text, x, y, color=(195, 175, 215)):
        image = self.font.render(text, True, color)
        self.screen.blit(image, (x, y))

    def draw_center(self, text, y, font, color):
        image = font.render(text, True, color)
        self.screen.blit(
            image,
            image.get_rect(center=(WIDTH // 2, y))
        )

    def draw_panel(self, x, y, w, h, alpha=150):
        panel = pygame.Surface((w, h), pygame.SRCALPHA)
        panel.fill((0, 0, 0, alpha))
        self.screen.blit(panel, (x, y))

    def draw_checkpoint_banner(self):
        timer = self.checkpoints.banner_timer
        if timer <= 0:
            return

        # Fade in quickly, fade out during the last 0.5 seconds.
        fade = min(1.0, timer / 0.5, (CHECKPOINT_BANNER_TIME - timer) / 0.2)
        fade = max(0.0, min(1.0, fade))
        alpha = int(255 * fade)

        y = HEIGHT // 2 - 130
        band = pygame.Surface((WIDTH, 90), pygame.SRCALPHA)
        band.fill((15, 9, 27, int(170 * fade)))
        self.screen.blit(band, (0, y - 45))

        title = self.big_font.render("CHECKPOINT", True, (232, 195, 115))
        title.set_alpha(alpha)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, y - 8)))

        sub = self.font.render(
            f"{self.score_manager.score} POINTS", True, (195, 175, 215)
        )
        sub.set_alpha(alpha)
        self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, y + 28)))

    def draw_popups(self):
        for popup in self.popups:
            fade = 1 - popup["age"] / POPUP_TIME
            image = self.font.render(
                popup["text"], True, popup.get("color", GOLD)
            )
            image.set_alpha(int(255 * fade))
            self.screen.blit(image, (popup["x"], popup["y"]))

    # ---------- Drawing ----------
    def draw_ghost_aura(self):
        """Soft yellow shimmer around the see-through Cloak."""
        pulse = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.012)
        radius = round(34 + pulse * 5)
        aura = pygame.Surface((radius * 2 + 4, radius * 2 + 4), pygame.SRCALPHA)
        c = radius + 2
        pygame.draw.circle(aura, (255, 215, 40, 30), (c, c), radius)
        pygame.draw.circle(aura, (255, 230, 90, 110), (c, c), radius, 2)
        self.screen.blit(aura, aura.get_rect(center=self.player.rect.center))

    def draw_world(self):
        self.bg_manager.draw(self.screen)
        self.spawner.draw(self.screen)
        self.player.alpha = self.ghost.alpha
        self.player.draw(self.screen)
        if self.ghost.active:
            self.draw_ghost_aura()
        self.draw_popups()
        self.draw_checkpoint_banner()

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
            self.draw_center(
                "NEW RECORD!", 88, self.font, colour
            )

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

        self.draw_text(
            f"CHECKPOINTS: {self.checkpoints.reached}",
            20, 140, color=lavender
        )

        if self.power_up.active:
            self.draw_text(
                f"TIME STONE: {self.power_up.time_left:.1f}s",
                20, 110, color=gold
            )

        if self.ghost.active:
            self.draw_text(
                f"GHOST: {self.ghost.time_left:.1f}s",
                20, 170, color=(255, 215, 40)
            )

        # Survival timer.
        total_seconds = int(self.elapsed_time)
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        timer_text = self.font.render(
            f"TIME: {minutes:02d}:{seconds:02d}",
            True,
            GOLD
        )

        timer_rect = timer_text.get_rect(
            topright=(WIDTH - 20, 20)
        )
        self.screen.blit(timer_text, timer_rect)

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

        self.draw_center(
            message, HEIGHT - 45, message_font, color
        )

    def draw_debug(self):
        lines = [
            ("RIFT DIAGNOSTICS", (232, 195, 115)),
            (
                f"Score: {self.score_manager.score}",
                (225, 210, 240)
            ),
            (
                f"High score: {self.score_manager.high_score}",
                (232, 195, 115)
            ),
            (
                f"New record: {self.score_manager.new_record}",
                (195, 175, 215)
            ),
            (
                f"Save successful: {self.score_manager.last_save_ok}",
                (195, 175, 215)
            ),
            (
                f"Barriers: {len(self.spawner.active_barriers())}",
                (195, 175, 215)
            ),
            (
                f"Time Stone active: {self.power_up.active}",
                (195, 175, 215)
            ),
            (
                f"Ghost active: {self.ghost.active}",
                (195, 175, 215)
            ),
            (
                f"Checkpoints reached: {self.checkpoints.reached}",
                (195, 175, 215)
            ),
        ]

        panel_width = 330
        row_height = 25
        panel_height = len(lines) * row_height + 24
        x = WIDTH - panel_width - 15
        y = 15

        panel = pygame.Surface(
            (panel_width, panel_height), pygame.SRCALPHA
        )
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
            image = self.small_font.render(
                line, True, color
            )
            self.screen.blit(
                image,
                (x + 14, y + 12 + i * row_height)
            )

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

    # ---------- Main loop ----------
    def run(self):
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000, MAX_FRAME_TIME)
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()