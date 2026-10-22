import json
import os

# The high score is saved in a file called highscore.json, next to the code
FILE_NAME = "highscore.json"


class HighScoreStorage:
    def __init__(self, path=FILE_NAME):
        self.path = path

    def load(self):
        """Read the high score from the file. Return 0 if anything goes wrong."""
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
            score = int(data["high_score"])
            if score < 0:
                return 0
            return score
        except Exception:
            # File missing, empty or damaged: just start from 0
            return 0

    def save(self, score):
        """Save the high score. Returns True if it worked, False if not."""
        temp_path = self.path + ".tmp"
        try:
            # Step 1: write the score to a temporary file
            with open(temp_path, "w") as f:
                json.dump({"high_score": int(score)}, f)
            # Step 2: swap the temporary file in
            # This way a crash never leaves a half-written file
            os.replace(temp_path, self.path)
            return True
        except Exception:
            # Saving failed, but the game should keep running
            return False