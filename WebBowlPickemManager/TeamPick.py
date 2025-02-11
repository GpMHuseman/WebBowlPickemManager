class TeamPick(object):
    """Holds each person that is playing this year."""
    def __init__(self, pickId, teamId, gameNumber, teamSelection, pointValue, isCorrect, yearPlaying):
        self.pickId = pickId
        self.teamId = teamId
        self.gameNumber = gameNumber
        self.teamSelection = teamSelection
        self.pointValue = pointValue
        self.isCorrect = isCorrect
        self.yearPlaying = yearPlaying


