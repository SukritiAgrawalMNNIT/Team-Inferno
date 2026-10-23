WIDTH, HEIGHT = 900, 600
FPS = 60

GRAVITY = 900           # pixels per second squared (was 1500)
THRUST = -400           # upward speed on key press (negative = up)
MAX_FALL_SPEED = 450    # the cloak never falls faster than this

PLAYER_X = 200
PLAYER_SIZE = (40, 40)  # hitbox only, the cloak is drawn around it

BG_COLOR = (20, 10, 30)
CLOAK_RED = (190, 30, 40)
CLOAK_DARK = (110, 15, 30)
CLOAK_GOLD = (240, 190, 60)
CLOAK_SCALE = 0.9                 # make the cloak bigger or smaller
CLOAK_OUTLINE = (40, 10, 20)

BARRIER_WIDTH = 80
BARRIER_SPACING = 320     # distance between one barrier and the next (pixels)
GAP_MARGIN = 80           # the gap stays this far from the ceiling and ground
POOL_SIZE = 15             # how many barriers exist in total (they are reused)
BARRIER_COLOR = (90, 40, 140)
BARRIER_EDGE = (200, 160, 255)