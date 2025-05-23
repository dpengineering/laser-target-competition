import json


class Leaderboard:
    """
        Class to handle the leaderboard.
    """
    def __init__(self):
        self.scores = {level: [] for level in range(1, 6)}
        self.temp_entry = None
        self.load_from_json()

    def add_score(self, player_name, points, level):
        """
            Adds an entry to the json file leaderboard.json, then removes the score if it's less than
            an existing score with the same name.
            Entry consists of a name and score(called points sometimes, sorry!)
            If there is a score with the same name but the new score is higher, it removes the lower score.
            If the score isn't in the top one thousand, don't add it(as to not have a giant leaderboard.json
            file in the future, one thousand entries is plenty)
            :param player_name
            :param points
            :param level
        """
        new_score = {'name': player_name, 'points': points}
        self.scores[level].append(new_score)
        if self.replace_existing_entry(level, points, player_name):
            self.scores[level].remove(self.temp_entry)
        elif self.no_new_entry(level, points, player_name):
            self.scores[level].remove(new_score)
        elif self.in_top_thousand(level, points):
            print(f"Adding score to leaderboard: {player_name} with {points} points")
            #do nothing, just don't run the else statement
        else:
            self.scores[level].remove(new_score)
        self.scores[level] = sorted(self.scores[level], key=lambda x: x['points'], reverse=True)
        self.save_to_json()

    def in_top_thousand(self, level, points):
        """
        :param level:
        :param points:
        :return: true if
        - there are less than 1000 entries
        - inputted points are more than the points of 1000th place.
        """
        if len(self.scores[level]) < 1000:
            print("Score should be in top 1000")
            return True
        return points > self.scores[level][1000]['points']

    def no_new_entry(self, level, points, name):
        """
        :param level:
        :param points:
        :param name:
        :return: True if there is another entry on the leaderboard with the same name and higher points. Returns false otherwise
        """
        for player in self.scores[level]:
            if player['name'] == name and player['points'] > points:
                print(f"{name} with {points} points shouldn't be added to the leaderboard because {player['name']} with {player['points']} points exists")
                return True
        return False

    def replace_existing_entry(self, level, points, name):
        """
        :param level:
        :param points:
        :param name:
        :return: True if there is another entry in the leaderboard with the same name and fewer points. Returns false otherwise.
        """
        for player in self.scores[level]:
            if player['name'] == name and player['points'] < points:
                print(f"{player['name']} with {player['points']} points should be replace by {name} with {points} points")
                self.temp_entry = player
                return True
        return False


    def get_placement(self, level, points):
        """
        :param level:
        :param points:
        :return: Returns the place of an entry in the leaderboard.
        """
        print(f"level={level}, points={points}")
        for i, score in enumerate(self.scores[level]):
            print(f"i={i}score={score['points']}")
            if points == score['points']:
                return i+1
            return None
        return None

    def save_to_json(self):
        """
        Adds top 1000 entries in self.scores to the json file

        """
        with open("../../assets/data/leaderboard/leaderboard.json", 'w') as file:
            truncated_scores = {level: self.scores[level][:1000] for level in self.scores}
            json.dump(truncated_scores, file)
            # json.dump(self.scores, file) IDK why this is here

    def load_from_json(self):
        """
        Gets the scores from the json file and loads them onto self.scores
        """
        with open("../../assets/data/leaderboard/leaderboard.json", 'r') as file:
            loaded_scores = json.load(file)
            self.scores = {int(level): scores for level, scores in loaded_scores.items()}
