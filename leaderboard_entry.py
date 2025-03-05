class LeaderboardEntry:
    def __init__(self, rank, name, points):
        self.name = name
        self.points = points
        self.rank = rank


    def __str__(self):
        return f"{self.rank}-{self.name}-{self.points}"

# Creating objects (instances) of the Dog class


