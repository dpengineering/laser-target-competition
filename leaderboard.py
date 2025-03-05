import leaderboard_entry

class Leaderboard:
    def __init__(self):
        with open('assets/leaderboard/leaderboard.txt', 'r') as file:
            loaded_scores = file

        self.entry_1 = leaderboard_entry.LeaderboardEntry(1, "HLS", 12600)
        self.entry_2 = leaderboard_entry.LeaderboardEntry(2, "PRS", 11500)
        self.entry_3 = leaderboard_entry.LeaderboardEntry(3, "TRM", 10900)
        self.entry_4 = leaderboard_entry.LeaderboardEntry(4, "SZC", 9200)
        self.leaderboard = [self.entry_1, self.entry_2, self.entry_3, self.entry_4]


    def write(self):
        print()

    def add_score(self, entry):
        print(f"entry={entry}")

    def get_placement(self, points):
        print()


