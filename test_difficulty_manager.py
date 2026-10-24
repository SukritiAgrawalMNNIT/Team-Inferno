import difficulty_manager as dm
from difficulty_manager import DifficultyManager


def test_speed_up_and_gap_narrows_with_score():
    d = DifficultyManager()
    s0, g0 = d.speed, d.gap_size
    d.on_score(20)
    assert d.speed > s0
    assert d.gap_size < g0


def test_limits_are_respected():
    d = DifficultyManager()
    d.on_score(100000)
    assert d.speed == dm.MAX_SPEED
    assert d.gap_size == dm.MIN_GAP


def test_reset_returns_to_level_zero():
    d = DifficultyManager()
    d.on_score(50)
    d.reset()
    assert d.speed == dm.BASE_SPEED
    assert d.gap_size == dm.BASE_GAP


def test_difficulty_never_gets_easier_as_score_rises():
    d = DifficultyManager()
    prev_speed, prev_gap = d.speed, d.gap_size
    for score in range(0, 300):
        d.on_score(score)
        assert d.speed >= prev_speed
        assert d.gap_size <= prev_gap
        prev_speed, prev_gap = d.speed, d.gap_size