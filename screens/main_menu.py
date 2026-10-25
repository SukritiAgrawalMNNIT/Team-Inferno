
import math
import random
import pygame


class MainMenu:
    def __init__(self, screen, high_score=0):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.high_score = high_score

        # Fonts — dark fantasy theme
        self.title_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 52
        )
        self.subtitle_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 22
        )
        self.score_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 24
        )
        self.button_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 21
        )
        self.small_font = pygame.font.Font(
            "assets/fonts/Cinzel-Regular.ttf", 14
        )

        # Buttons
        self.start_button = pygame.Rect(0, 0, 280, 58)
        self.quit_button = pygame.Rect(0, 0, 280, 58)
        self.hovered_button = None

        # Floating magical particles
        random.seed(10)
        self.particles = [
            [
                random.randint(0, self.width),
                random.randint(0, self.height),
                random.uniform(0.25, 0.7),
                random.choice([1, 1, 2]),
                random.choice([
                    (155, 100, 220),
                    (190, 145, 65),
                    (115, 70, 175),
                    (225, 190, 110),
                ]),
            ]
            for _ in range(100)
        ]

    def draw_glow_text(
        self, text, font, color, center, glow_color
    ):
        # Sharp, focused glow
        for radius, alpha in [(3, 35), (2, 70), (1, 120)]:
            glow = font.render(text, True, glow_color)
            glow.set_alpha(alpha)

            for dx, dy in [
                (-radius, 0),
                (radius, 0),
                (0, -radius),
                (0, radius),
            ]:
                rect = glow.get_rect(
                    center=(
                        center[0] + dx,
                        center[1] + dy,
                    )
                )
                self.screen.blit(glow, rect)

        # Crisp text over the glow
        label = font.render(text, True, color)
        self.screen.blit(
            label, label.get_rect(center=center)
        )

    def draw(self):
        width, height = self.screen.get_size()
        cx = width // 2

        # Dark fantasy background
        self.screen.fill((10, 7, 19))
        # Moving golden ambient lights
        time = pygame.time.get_ticks() * 0.001

        for i, (x, y, radius) in enumerate([
            (120, 100, 90),
            (780, 150, 110),
            (150, 490, 100),
            (760, 470, 120),
            (450, 80, 85),  # New golden light
        ]):
            move_x = math.sin(time * 0.8 + i) * 35
            move_y = math.cos(time * 0.6 + i) * 25

            glow = pygame.Surface(
                (radius * 2, radius * 2),
                pygame.SRCALPHA,
            )

            for r in range(radius, 0, -4):
                alpha = int(22 * (1 - r / radius))
                pygame.draw.circle(
                    glow,
                    (255, 190, 75, alpha),
                    (radius, radius),
                    r,
                )

            self.screen.blit(
                glow,
                (int(x + move_x - radius), int(y + move_y - radius)),
            )
                

        # Background mist
        mist = pygame.Surface(
            (width, height), pygame.SRCALPHA
        )

        for i in range(7):
            x = (i * 173 + 60) % width
            y = (i * 97 + 100) % height

            pygame.draw.ellipse(
                mist,
                (70, 25, 105, 18),
                (x - 160, y - 65, 320, 130),
            )

        self.screen.blit(mist, (0, 0))

        # Dimensional portal
        cy = height // 2 - 65
        pulse = math.sin(
            pygame.time.get_ticks() * 0.002
        )

        # Layered purple aura
        glow = pygame.Surface(
            (width, height), pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (105, 35, 170, 18),
            (cx, cy),
            int(112 + pulse * 4),
        )
        pygame.draw.circle(
            glow,
            (125, 40, 195, 28),
            (cx, cy),
            int(91 + pulse * 3),
        )
        pygame.draw.circle(
            glow,
            (150, 55, 220, 32),
            (cx, cy),
            int(74 + pulse * 2),
        )

        self.screen.blit(glow, (0, 0))

        # Portal rings — outer purple, middle gold, inner purple
        for radius, color, thickness in [
            (78, (175, 90, 225), 2),
            (67, (235, 185, 95), 2),
            (54, (110, 55, 165), 1),
        ]:
            pygame.draw.circle(
                self.screen,
                color,
                (cx, cy),
                int(radius + pulse * 2),
                thickness,
            )

                # Six small magical orbs: 3 gold, 3 purple
        orb_time = pygame.time.get_ticks() * 0.001

        orb_colors = [
            (235, 190, 105),
            (175, 110, 220),
            (235, 190, 105),
            (175, 110, 220),
            (235, 190, 105),
            (175, 110, 220),
        ]

        for i, orb_color in enumerate(orb_colors):
            angle = orb_time * 0.25 + i * (math.pi / 3)

            orbit_radius = 100 + math.sin(
                orb_time + i
            ) * 4

            ox = cx + int(orbit_radius * math.cos(angle))
            oy = cy + int(orbit_radius * math.sin(angle))

            # Tiny outer glow
            pygame.draw.circle(
                self.screen,
                orb_color,
                (ox, oy),
                4,
                1,
            )

            # Small bright center
            pygame.draw.circle(
                self.screen,
                orb_color,
                (ox, oy),
                2,
            )
            # Subtle outer glow
            pygame.draw.circle(
                self.screen,
                orb_color,
                (ox, oy),
                5,
                1,
            )

            # Small luminous orb
            pygame.draw.circle(
                self.screen,
                orb_color,
                (ox, oy),
                2,
            )

        # Small rotating rune accents
        angle = pygame.time.get_ticks() * 0.0003

        for i in range(8):
            a = angle + i * math.pi / 4
            x = cx + int(91 * math.cos(a))
            y = cy + int(91 * math.sin(a))

            pygame.draw.circle(
                self.screen,
                (195, 120, 235),
                (x, y),
                2,
            )

        # Floating magical particles
        for particle in self.particles:
            particle[1] -= particle[2]

            if particle[1] < -5:
                particle[1] = height + 5
                particle[0] = random.randint(0, width)

            pygame.draw.circle(
                self.screen,
                particle[4],
                (int(particle[0]), int(particle[1])),
                particle[3],
            )

        
        # Royal golden heading with side ornaments
        title_y = 55

        self.draw_glow_text(
            "CLOAK OF CHAOS",
            self.title_font,
            (240, 205, 125),
            (cx, title_y),
            (255, 185, 65),
        )

        # Royal ornaments beside the heading
        title_width = self.title_font.size("CLOAK OF CHAOS")[0]
        half_width = title_width // 2
        ornament_gap = 22

        left_x = cx - half_width - ornament_gap
        right_x = cx + half_width + ornament_gap

        for side in (-1, 1):
            x = left_x if side == -1 else right_x

            # Fine golden horizontal lines
            pygame.draw.line(
                self.screen,
                (175, 130, 65),
                (x - side * 25, title_y),
                (x - side * 5, title_y),
                1,
            )

            # Small royal diamond
            diamond_size = 5
            pygame.draw.polygon(
                self.screen,
                (225, 185, 105),
                [
                    (x, title_y - diamond_size),
                    (x + side * diamond_size, title_y),
                    (x, title_y + diamond_size),
                    (x - side * diamond_size, title_y),
                ],
            )

            # Tiny accent above the diamond
            pygame.draw.circle(
                self.screen,
                (245, 215, 155),
                (x, title_y - 12),
                1,
            )


        # Subtitle
        subtitle = self.subtitle_font.render(
    "R I F T   R U N N E R",
    True,
    (177, 125, 210),
)
        subtitle_rect = subtitle.get_rect(center=(cx, 105))
        self.screen.blit(subtitle, subtitle_rect)

        # Button positions
        self.start_button.center = (
            cx, height // 2 + 85
        )
        self.quit_button.center = (
            cx, height // 2 + 155
        )

        self.draw_button(
            self.start_button,
            "ENTER THE RIFT",
            "start",
        )
        self.draw_button(
            self.quit_button,
            "ABANDON REALM",
            "quit",
        )

        # High score
        self.draw_glow_text(
            f"HIGH SCORE: {self.high_score}",
            self.score_font,
            (195, 165, 110),
            (cx, height - 65),
            (190, 125, 50),
        )

        # Footer
        footer = self.small_font.render(
            "THE DIMENSION IS CALLING",
            True,
            (105, 85, 125),
        )
        self.screen.blit(
            footer,
            footer.get_rect(
                center=(cx, height - 28)
            ),
        )

    def draw_button(self, rect, text, button_name):
        hovered = self.hovered_button == button_name

        if hovered:
            fill = (35, 23, 47)
            border = (235, 195, 130)
            text_color = (255, 238, 205)
            glow_color = (220, 150, 75)
            glow_alpha = 45
            border_width = 2
        else:
            fill = (18, 12, 28)
            border = (145, 100, 175)
            text_color = (220, 200, 235)
            glow_color = (145, 65, 200)
            glow_alpha = 22
            border_width = 1

        # Medium outer glow
        margin = 18
        glow_surface = pygame.Surface(
            (
                rect.width + margin * 2,
                rect.height + margin * 2,
            ),
            pygame.SRCALPHA,
        )

        for padding, alpha, thickness in [
            (12, glow_alpha // 3, 4),
            (7, glow_alpha // 2, 3),
            (3, glow_alpha, 2),
        ]:
            glow_rect = pygame.Rect(
                margin - padding,
                margin - padding,
                rect.width + padding * 2,
                rect.height + padding * 2,
            )

            pygame.draw.rect(
                glow_surface,
                (*glow_color, alpha),
                glow_rect,
                width=thickness,
                border_radius=8,
            )

        self.screen.blit(
            glow_surface,
            (rect.x - margin, rect.y - margin),
        )

        # Button background
        pygame.draw.rect(
            self.screen,
            fill,
            rect,
            border_radius=5,
        )

        # Button border
        pygame.draw.rect(
            self.screen,
            border,
            rect,
            border_width,
            border_radius=5,
        )

        # Glowing text
        self.draw_glow_text(
            text,
            self.button_font,
            text_color,
            rect.center,
            glow_color,
        )

    def handle_event(self, event):
        # Mouse hover
        if event.type == pygame.MOUSEMOTION:
            if self.start_button.collidepoint(event.pos):
                self.hovered_button = "start"
            elif self.quit_button.collidepoint(event.pos):
                self.hovered_button = "quit"
            else:
                self.hovered_button = None

        # Mouse clicks
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if self.start_button.collidepoint(event.pos):
                return "start"

            if self.quit_button.collidepoint(event.pos):
                return "quit"

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "start"

            if event.key == pygame.K_ESCAPE:
                return "quit"

        return None
