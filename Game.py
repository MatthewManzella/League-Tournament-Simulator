class Game:

    def __init__(self, t1, t1_goals, t2, t2_goals, winner):
        """
        team1/team2 = names of both teams
        team1_goals/team2_goals = number of goals in the game for each team
        winning_team = name of winning team
        """
        self.team1 = t1
        self.team1_goals = t1_goals
        self.team2 = t2
        self.team2_goals = t2_goals
        self.winning_team = winner
        if winner == "Draw":
            self.losing_team = "Draw"
        elif winner == t1:
            self.losing_team = t2
        else:
            self.losing_team = t1

    def get_team1(self):
        return self.team1

    def get_team1_goals(self):
        return self.team1_goals

    def get_team2(self):
        return self.team2

    def get_team2_goals(self):
        return self.team2_goals

    def get_winner(self):
        return self.winning_team

    def get_loser(self):
        return self.losing_team
