import math
import random
import pygame
from settings import WIDTH, HEIGHT

FADE_TIME = 1.5   # seconds to blend from one stage into the next


def lerp(a, b, t):
    return a + (b - a) * t


def clamp01(v):
    return max(0.0, min(1.0, v))


# One entry per checkpoint. Stage 0 = the original background (the start look).
#   tint  : colour multiplied over the picture (darkens + colours it)
#   desat : 0..1  how much colour is drained out of the picture
#   vig   : 0..1  strength of the dark-red vignette (closing-in edges)
#   fog   : 0..255 opacity of the drifting fog
#   eyes  : number of glowing eye pairs lurking in the dark
#   flash : chance per second of a lightning-style flash
STAGES = [
    dict(tint=(255, 255, 255), desat=0.00, vig=0.00, fog=0,   eyes=0, flash=0.00),
    dict(tint=(175, 140, 200), desat=0.35, vig=0.45, fog=40,  eyes=0, flash=0.00),
    dict(tint=(215, 85, 95),   desat=0.55, vig=0.60, fog=70,  eyes=3, flash=0.08),
    dict(tint=(95, 150, 105),  desat=0.65, vig=0.72, fog=95,  eyes=5, flash=0.12),
    dict(tint=(150, 30, 45),   desat=0.75, vig=0.85, fog=120, eyes=7, flash=0.18),
]


class BackgroundManager:
    def __init__(self, base):
        self.base = base
        self.stage_surfs = [self._build_stage(cfg) for cfg in STAGES]
        self.vignette = self._build_vignette()
        self.fog_layers = [self._build_fog(1), self._build_fog(2)]

        flash = pygame.Surface((WIDTH, HEIGHT))
        flash.fill((230, 210, 255))
        self.flash_surf = flash

        # Fixed hiding places for the eyes (same every run)
        rng = random.Random(13)
        self.eyes = []
        for _ in range(max(s["eyes"] for s in STAGES)):
            y = rng.choice((rng.randint(40, 190), rng.randint(410, 560)))
            self.eyes.append((
                rng.randint(40, WIDTH - 40),   # x
                y,
                rng.randint(7, 12),            # half distance between the eyes
                rng.uniform(0, 6.28),          # blink phase
                rng.uniform(0.5, 1.1),         # blink speed
            ))

        self.reset()

    # ---------- building the pictures (done once) ----------
    def _build_stage(self, cfg):
        surf = self.base.copy()
        if cfg["desat"] > 0:
            try:
                gray = pygame.transform.grayscale(self.base)
                gray.set_alpha(int(255 * cfg["desat"]))
                surf.blit(gray, (0, 0))
            except AttributeError:      # very old pygame: skip desaturation
                pass
        surf.fill(cfg["tint"], special_flags=pygame.BLEND_RGB_MULT)
        return surf

    def _build_vignette(self):
        w, h = 64, 40
        small = pygame.Surface((w, h), pygame.SRCALPHA)
        for x in range(w):
            for y in range(h):
                dx = (x - (w - 1) / 2) / (w / 2)
                dy = (y - (h - 1) / 2) / (h / 2)
                d = math.sqrt(dx * dx + dy * dy) / 1.41
                a = clamp01((d - 0.35) / 0.65) ** 1.5
                small.set_at((x, y), (18, 0, 6, int(255 * a)))
        return pygame.transform.smoothscale(small, (WIDTH, HEIGHT))

    def _build_fog(self, seed):
        rng = random.Random(seed)
        layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for _ in range(7):
            cx = rng.randint(0, WIDTH)
            cy = rng.randint(int(HEIGHT * 0.2), int(HEIGHT * 0.9))
            radius = rng.randint(90, 170)
            for offset in (-WIDTH, 0, WIDTH):          # wraps around seamlessly
                for r in range(radius, 0, -8):
                    a = int(70 * (1 - r / radius) ** 1.5)
                    pygame.draw.circle(
                        layer, (170, 150, 190, a), (cx + offset, cy), r
                    )
        return layer

    # ---------- control ----------
    def reset(self):
        self.stage = 0
        self.prev = 0
        self.fade = 1.0
        self.time = 0.0
        self.flash = 0.0
        self.fog_off = [0.0, 0.0]
        for s in self.stage_surfs:
            s.set_alpha(255)

    def set_stage(self, number):
        """Call at each checkpoint. Fades into the next, scarier background."""
        number = min(number, len(STAGES) - 1)
        if number == self.stage:
            return
        # If still fading, snap to the stage we were heading for
        self.stage_surfs[self.stage].set_alpha(255)
        self.prev = self.stage
        self.stage = number
        self.fade = 0.0

    def update(self, dt):
        self.time += dt

        if self.fade < 1.0:
            self.fade = min(1.0, self.fade + dt / FADE_TIME)
            if self.fade >= 1.0:
                self.stage_surfs[self.stage].set_alpha(255)
                self.prev = self.stage

        self.fog_off[0] = (self.fog_off[0] + 18 * dt) % WIDTH
        self.fog_off[1] = (self.fog_off[1] + 40 * dt) % WIDTH

        # Random flash (gentle, never full white)
        self.flash = max(0.0, self.flash - dt * 3.5)
        if random.random() < STAGES[self.stage]["flash"] * dt:
            self.flash = 1.0

    def _mix(self, key):
        return lerp(STAGES[self.prev][key], STAGES[self.stage][key], self.fade)

    # ---------- drawing ----------
    def draw(self, screen):
        # 1. Picture (cross-fading between two stages)
        screen.blit(self.stage_surfs[self.prev], (0, 0))
        if self.fade < 1.0:
            top = self.stage_surfs[self.stage]
            top.set_alpha(int(255 * self.fade))
            screen.blit(top, (0, 0))

        # 2. Drifting fog (two layers, different speeds)
        fog_alpha = int(self._mix("fog"))
        if fog_alpha > 1:
            for layer, off in zip(self.fog_layers, self.fog_off):
                layer.set_alpha(fog_alpha)
                screen.blit(layer, (-off, 0))
                screen.blit(layer, (WIDTH - off, 0))

        # 3. Glowing eyes watching from the dark
        count = self._mix("eyes")
        for i, (x, y, sp, phase, speed) in enumerate(self.eyes):
            k = clamp01(count - i)
            if k <= 0:
                continue
            blink = clamp01((math.sin(self.time * speed + phase) - 0.2) * 2.5)
            power = blink * k
            if power < 0.05:
                continue
            halo = (int(110 * power), 0, int(10 * power))
            core = (int(255 * power), int(40 * power), int(40 * power))
            for dx in (-sp, sp):
                pygame.draw.circle(screen, halo, (x + dx, y), 8)
                pygame.draw.circle(screen, core, (x + dx, y), 3)

        # 4. Lightning-style flash
        if self.flash > 0.02:
            self.flash_surf.set_alpha(int(80 * self.flash))
            screen.blit(self.flash_surf, (0, 0))

        # 5. Heartbeat vignette (edges close in and throb)
        vig = self._mix("vig")
        if vig > 0.01:
            beat = max(0.0, math.sin(self.time * 5)) ** 4
            self.vignette.set_alpha(int(255 * clamp01(vig * (0.85 + 0.3 * beat))))
            screen.blit(self.vignette, (0, 0))