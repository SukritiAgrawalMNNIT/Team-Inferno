from high_score_storage import HighScoreStorage


class ScoreManager:
    def __init__(self, storage=None):
        # Use the given storage, or make a normal one
        if storage is None:
            storage = HighScoreStorage()
        self.storage = storage

        self.score = 0                          # score of the current run
        self.high_score = self.storage.load()   # best score ever
        self.new_record = False                 # did this run beat the high score?

    def add_point(self):
        """Call this every time the Cloak passes through a gap (+1 point)."""
        self.score = self.score + 1
        if self.score > self.high_score:
            self.high_score = self.score
            self.new_record = True

    def end_run(self):
        """Call this once when the Cloak dies. Saves only if there is a new record."""
        if self.new_record:
            self.storage.save(self.high_score)
        return self.new_record

    def reset(self):
        """Call this when a new run starts."""
        self.score = 0
        self.new_record = False