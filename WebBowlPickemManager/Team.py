class Team(object):
    """Holds each person that is playing this year."""
    def __init__(self, teamId, teamName, currentPoints, maxPoints, yearPlaying):
        self.teamId = teamId
        self.teamName = teamName
        self.currentPoints = currentPoints
        self.maxPoints = maxPoints
        self.yearPlaying = yearPlaying


