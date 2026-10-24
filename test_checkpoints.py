from checkpoints import CheckpointManager


def test_no_checkpoint_before_n_points():
    c = CheckpointManager(every=10)
    assert c.check(9) is False
    assert c.reached == 0


def test_checkpoint_at_n_points():
    c = CheckpointManager(every=10)
    assert c.check(10) is True
    assert c.reached == 1
    assert c.banner_timer > 0


def test_same_checkpoint_not_repeated():
    c = CheckpointManager(every=10)
    c.check(10)
    assert c.check(11) is False
    assert c.check(19) is False


def test_second_checkpoint():
    c = CheckpointManager(every=10)
    c.check(10)
    assert c.check(20) is True
    assert c.reached == 2


def test_banner_counts_down_and_stops():
    c = CheckpointManager(every=10)
    c.check(10)
    c.update(10.0)
    assert c.banner_timer == 0


def test_reset_clears_checkpoints():
    c = CheckpointManager(every=10)
    c.check(30)
    c.reset()
    assert c.reached == 0
    assert c.banner_timer == 0