import pygame
from settings import *
from player import Player
from barrier import Barrier
from barrier_spawner import BarrierSpawner


def make_barrier(x=300.0, gap_y=200, gap=200):
    """A barrier we place by hand, so the test does not depend on randomness.
    With the default numbers: top block covers y 0-200, gap is y 200-400, bottom block is y 400-600."""
    b = Barrier()
    b.x = x
    b.gap = gap
    b.gap_y = gap_y
    b.active = True
    b.update_rects()
    return b


# ---------- Cloak against a barrier ----------
def test_cloak_in_gap_is_safe():
    b = make_barrier()
    assert b.collides(pygame.Rect(320, 250, 40, 40)) is False


def test_cloak_hits_top_block():
    b = make_barrier()
    assert b.collides(pygame.Rect(320, 150, 40, 40)) is True


def test_cloak_hits_bottom_block():
    b = make_barrier()
    assert b.collides(pygame.Rect(320, 380, 40, 40)) is True


def test_cloak_before_barrier_is_safe():
    b = make_barrier()
    assert b.collides(pygame.Rect(100, 150, 40, 40)) is False


# ---------- Barrier movement ----------
def test_barrier_off_screen():
    b = make_barrier(x=-BARRIER_WIDTH - 1)
    assert b.is_off_screen() is True
    assert make_barrier(x=0.0).is_off_screen() is False


def test_barrier_returns_to_pool_after_leaving():
    b = make_barrier(x=100.0)
    b.update(1.0, 250)               # moves 250 pixels left, now fully off-screen
    assert b.active is False


def test_gap_stays_inside_margins():
    b = Barrier()
    for _ in range(200):
        b.spawn(150)
        assert b.gap_y >= GAP_MARGIN
        assert b.gap_y + 150 <= HEIGHT - GAP_MARGIN


# ---------- Cloak against the ceiling and ground ----------
def test_player_hits_ceiling():
    p = Player()
    p.rect.top = 0
    assert p.hits_bounds() is True


def test_player_hits_ground():
    p = Player()
    p.rect.bottom = HEIGHT
    assert p.hits_bounds() is True


def test_player_in_middle_is_safe():
    p = Player()
    assert p.hits_bounds() is False


# ---------- The spawner (object pool) ----------
def test_pool_never_grows():
    s = BarrierSpawner()
    for _ in range(2000):
        s.update(0.016, 250, 200)
    assert len(s.pool) == POOL_SIZE
    assert len(s.active_barriers()) <= POOL_SIZE


def test_spawner_detects_hit():
    s = BarrierSpawner()
    s.spawn(200)
    b = s.pool[0]
    b.x, b.gap, b.gap_y = 300.0, 200, 200
    b.update_rects()
    assert s.hits_player(pygame.Rect(320, 150, 40, 40)) is True
    assert s.hits_player(pygame.Rect(320, 250, 40, 40)) is False


def test_gap_counted_once():
    s = BarrierSpawner()
    b = s.pool[0]
    b.x, b.active, b.passed = 100.0, True, False    # right edge at 180, behind the Cloak
    cloak = pygame.Rect(200, 250, 40, 40)
    assert s.count_passed(cloak) == 1
    assert s.count_passed(cloak) == 0               # the same barrier never scores twice


def test_barrier_ahead_is_not_counted():
    s = BarrierSpawner()
    b = s.pool[0]
    b.x, b.active, b.passed = 400.0, True, False
    assert s.count_passed(pygame.Rect(200, 250, 40, 40)) == 0