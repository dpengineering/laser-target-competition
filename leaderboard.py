import json


class Leaderboard:
    def __init__(self):
        self.scores = {level: [] for level in range(1, 6)}
        self.temp_entry = None
        self.load_from_json()

    def add_score(self, player_name, points, level):

        new_score = {'name': player_name, 'points': points}
        self.scores[level].append(new_score)
        if self.replace_existing_entry(level, points, player_name):
            self.scores[level].remove(self.temp_entry)
        elif self.in_top_ten(level, points):
            print(f"Adding score to leaderboard: {player_name} with {points} points")
            #do nothing, just don't run the else statement
        else:
            self.scores[level].remove(new_score)
        self.scores[level] = sorted(self.scores[level], key=lambda x: x['points'], reverse=True)
        self.save_to_json()

    def in_top_ten(self, level, points):
        if len(self.scores[level]) < 10:
            print("Score should be in top 10")
            return True
        return points > self.scores[level][9]['points']


    def replace_existing_entry(self, level, points, name):
        for player in self.scores[level]:
            if player['name'] == name and player['points'] < points:
                print(f"{player['name']} with {player['points']} points should be replace by {name} with {points} points")
                self.temp_entry = player
                return True
        return False



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
