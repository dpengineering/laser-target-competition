import json


class Leaderboard:
    # TODO if an entry has the same name as an another entry, remove the entry with the lower value
    # ex - HLS 3000 pts and HLS 8100 points, the 8100 point one will stay and the 3000 point one will get deleted
    def __init__(self):
        self.scores = {level: [] for level in range(1, 6)}
        self.load_from_json()

    def add_score(self, player_name, points, level):
        new_score = {'name': player_name, 'points': points}
        self.scores[level].append(new_score)
        self.scores[level] = sorted(self.scores[level], key=lambda x: x['points'], reverse=True)
        self.save_to_json()

    def in_top_ten(self, level, points):
        if len(self.scores[level]) < 10:
            return True
        return points > self.scores[level][9]['points']

    def get_placement(self, level, points):
        print(f"level={level}, points={points}")
        for i, score in enumerate(self.scores[level]):
            print(f"i={i}score={score['points']}")
            if points == score['points']:
                return i+1

    def save_to_json(self):
        with open("assets/data/leaderboard/leaderboard.json", 'w') as file:
            truncated_scores = {level: self.scores[level][:10] for level in self.scores}
            json.dump(truncated_scores, file)
            # json.dump(self.scores, file) IDK why this is here

    def load_from_json(self):
        with open("assets/data/leaderboard/leaderboard.json", 'r') as file:
            loaded_scores = json.load(file)
            self.scores = {int(level): scores for level, scores in loaded_scores.items()}
