import power_up as pu
from power_up import PowerUp, PowerUpType, TimeStoneEffect, maybe_spawn_time_stone


class FakeRng:
    def __init__(self, value):
        self.value = value

    def random(self):
        return self.value


def make_stone(x=100, y=100):
    p = PowerUp(PowerUpType.TIME_STONE)
    p.spawn(x, y)
    return p


# ---- TimeStoneEffect ----
def test_effect_is_off_by_default():
    e = TimeStoneEffect()
    assert not e.active
    assert e.multiplier == 1.0


def test_activate_slows_barriers():
    e = TimeStoneEffect()
    e.activate()
    assert e.active
    assert e.multiplier == pu.TIME_STONE_SLOW_FACTOR


def test_effect_expires_after_duration():
    e = TimeStoneEffect()
    e.activate()
    e.update(pu.TIME_STONE_DURATION - 0.1)
    assert e.active
    e.update(0.2)
    assert not e.active
    assert e.multiplier == 1.0


def test_timer_never_goes_negative():
    e = TimeStoneEffect()
    e.activate()
    e.update(100)
    assert e.time_left == 0


def test_second_stone_refreshes_but_does_not_stack():
    e = TimeStoneEffect()
    e.activate()
    e.update(3.0)
    e.activate()
    assert e.time_left == pu.TIME_STONE_DURATION
    assert e.multiplier == pu.TIME_STONE_SLOW_FACTOR   # still 0.5, not 0.25


def test_reset_clears_effect():
    e = TimeStoneEffect()
    e.activate()
    e.reset()
    assert not e.active


# ---- PowerUp item ----
def test_power_up_moves_left():
    p = make_stone(x=200)
    p.update(0.5, 100)
    assert p.x == 150


def test_power_up_deactivates_off_screen():
    p = make_stone(x=-pu.POWERUP_SIZE + 1)
    p.update(1.0, 100)
    assert not p.active


def test_collision_when_overlapping():
    assert make_stone(100, 100).collides_with((110, 110, 30, 30))


def test_no_collision_when_apart():
    assert not make_stone(100, 100).collides_with((300, 300, 30, 30))


def test_collect_makes_item_disappear():
    p = make_stone()
    p.collect()
    assert not p.active
    assert not p.collides_with((100, 100, 30, 30))


# ---- spawning ----
def test_spawns_when_roll_is_low():
    stone = maybe_spawn_time_stone(50, 60, rng=FakeRng(0.0))
    assert stone is not None
    assert stone.active and stone.type == PowerUpType.TIME_STONE
    assert (stone.x, stone.y) == (50, 60)


def test_does_not_spawn_when_roll_is_high():
    assert maybe_spawn_time_stone(50, 60, rng=FakeRng(0.99)) is None