
from leaderboard import Leaderboard

leaderboard = Leaderboard()

level = 1


print(leaderboard.in_top_ten(1, 120))

for i , score in enumerate(leaderboard.scores[level]):
    print(str((i+1)) + ". " + str(score['name']) + " " + str(score['points']))



