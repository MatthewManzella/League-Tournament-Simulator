class Team:
    def __init__(self, t=None, s=None, to_play=None):
        """
        team = name of team
        wins/draws/losses = number of occurrences of each result
        seed = initial placement read in at beginning of simulation
        gf = goals for
        ga = goals against
        opponent_list =  list of all teams excluding self/teams seeded higher than self
        game_obj_list = list of all games played
        """
        self.team = t
        self.seed = s
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.gf = 0
        self.ga = 0
        if to_play is None:
            self.opponent_list = []
        else:
            self.opponent_list = to_play
        self.game_obj_list = []
        self.playoff_game_list = []
        self.playoff_seed = 0
        self.playoff_wins = 0
        self.playoff_losses = 0
        self.playoff_gf = 0
        self.playoff_ga = 0

    def incr_playoff_wins(self):
        self.playoff_wins += 1

    def incr_playoff_losses(self):
        self.playoff_losses += 1

    def incr_playoff_gf(self, goals):
        self.playoff_gf += goals

    def incr_playoff_ga(self, goals):
        self.playoff_ga += goals

    def get_playoff_wins(self):
        return self.playoff_wins

    def get_playoff_losses(self):
        return self.playoff_losses

    def get_playoff_gf(self):
        return self.playoff_gf

    def get_playoff_ga(self):
        return self.playoff_ga

    def get_playoff_gd(self):
        return self.playoff_gf - self.playoff_ga

    def get_playoff_seed(self):
        return self.playoff_seed

    def set_playoff_seed(self, seed):
        self.playoff_seed = seed

    def get_playoff_game_list(self):
        return self.playoff_game_list

    def add_playoff_game(self, game):
        self.playoff_game_list.append(game)

    def get_team(self):
        return self.team

    def get_seed(self):
        return self.seed

    def get_wins(self):
        return self.wins

    def get_draws(self):
        return self.draws

    def get_losses(self):
        return self.losses

    def get_gf(self):
        return self.gf

    def get_ga(self):
        return self.ga

    def get_gd(self):
        return self.gf - self.ga

    def print_opponent_list(self):
        for i in self.opponent_list:
            print(i.get_team())

    def get_opponent_list(self):
        return self.opponent_list

    def set_opponent_list(self, to_play):
        self.opponent_list = to_play

    def incr_wins(self):
        self.wins += 1

    def incr_draws(self):
        self.draws += 1

    def incr_losses(self):
        self.losses += 1

    def incr_gf(self, goals):
        self.gf += goals

    def incr_ga(self, goals):
        self.ga += goals

    def get_points(self):
        return self.get_wins()*3 + self.get_draws()*1

    def get_game_list(self):
        return self.game_obj_list

    def add_game(self, game):
        self.game_obj_list.append(game)
