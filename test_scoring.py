from high_score_storage import HighScoreStorage
from score_manager import ScoreManager


def make_manager(folder):
    """A ScoreManager that saves into a temporary folder (your real highscore.json is never touched)."""
    storage = HighScoreStorage(str(folder / "hs.json"))
    return ScoreManager(storage)


def test_starts_at_zero(tmp_path):
    m = make_manager(tmp_path)
    assert m.score == 0
    assert m.high_score == 0
    assert m.new_record is False


def test_add_point_adds_one(tmp_path):
    m = make_manager(tmp_path)
    m.add_point()
    assert m.score == 1


def test_three_points_make_a_record(tmp_path):
    m = make_manager(tmp_path)
    for _ in range(3):
        m.add_point()
    assert m.score == 3
    assert m.high_score == 3
    assert m.new_record is True


def test_new_record_is_saved(tmp_path):
    m = make_manager(tmp_path)
    m.add_point()
    m.add_point()
    assert m.end_run() is True
    reloaded = make_manager(tmp_path)        # like closing and reopening the game
    assert reloaded.high_score == 2


def test_no_save_without_new_record(tmp_path):
    first = make_manager(tmp_path)
    for _ in range(5):
        first.add_point()
    first.end_run()                          # saves 5

    second = make_manager(tmp_path)
    second.add_point()                       # only 1 point, no record
    assert second.end_run() is False
    assert make_manager(tmp_path).high_score == 5


def test_reset_keeps_high_score(tmp_path):
    m = make_manager(tmp_path)
    for _ in range(3):
        m.add_point()
    m.reset()
    assert m.score == 0
    assert m.high_score == 3
    assert m.new_record is False


def test_equal_score_is_not_a_record(tmp_path):
    first = make_manager(tmp_path)
    for _ in range(5):
        first.add_point()
    first.end_run()

    second = make_manager(tmp_path)
    for _ in range(5):
        second.add_point()
    assert second.high_score == 5
    assert second.new_record is False

def test_end_run_reports_a_successful_save(tmp_path):
    m = make_manager(tmp_path)
    assert m.last_save_ok is None            # nothing saved yet
    m.add_point()
    m.end_run()
    assert m.last_save_ok is True


def test_end_run_without_record_saves_nothing(tmp_path):
    m = make_manager(tmp_path)
    m.end_run()                              # score 0, no record
    assert m.last_save_ok is None