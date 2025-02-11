class Matchup(object):
    """Holds each matchup this year."""
    def __init__(self, matchupId, gameNumber, teamOne, teamTwo, winner, yearPlaying):
        self.matchupId = matchupId
        self.gameNumber = gameNumber
        self.teamOne = teamOne
        self.teamTwo = teamTwo
        self.winner = winner
        self.yearPlaying = yearPlaying


