import os

class Score:
    def __init__(self):
        self.current = 0
        self.high_score = self.load_high_score()

    def load_high_score(self):
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as f:
                try: return int(f.read())
                except: return 0
        return 0

    def save_high_score(self):
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def reset_high_score(self):
        self.high_score = 0
        self.save_high_score()