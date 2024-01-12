import random
import sys
from Team import Team
from Game import Game


def main():
    """
    Prompts the user for the number of teams and the absolute file path to the list of seeded teams. Validates input
    and ensures the file contains unique teams sorted from 1 through num_of_teams. It then prompts for the number of
    round-robins and the level of randomness. The league simulation is initiated with start_season.

    CALLS: team_dictionary_generator, file_validity_checker, start_season
    """
    print("\nWELCOME TO THE LEAGUE SIMULATOR!!\n\n")
    num_of_teams = input("Please enter how many teams are in your league (must be greater than 1): ")
    # Ensures number of teams is an int > 1
    while not num_of_teams.isdigit() or num_of_teams in ["0", "1"]:
        num_of_teams = input("\nERROR: Please enter a proper number: ")
    num_of_teams = int(num_of_teams)
    print("\nHINT: Find the absolute path by going to your File Explorer, single-clicking\non the file you "
          "are using, and holding Ctrl + Shift + C at the same time.\nRemove the quotation marks before "
          "submitting it to the League Simulator.")
    file_path = input(f"\nPlease enter an absolute file path to a list of {num_of_teams} seeded teams in order "
                      f"(no quotation marks): ")
    # Ensures that the file exists, has proper seeding, and zero duplicate teams
    file_valid = file_validity_checker(file_path, num_of_teams)
    while file_valid is False:
        print("\nEnter 0 to quit.")
        file_path = input(f"\nERROR: Please enter a file that has all unique teams sorted 1 through {num_of_teams}. "
                          f"In the format:"
                          f"\n1: Team 1"
                          f"\n2: Team 2\n\n")
        if file_path == "0":
            sys.exit(0)
        file_valid = file_validity_checker(file_path, num_of_teams)
    print("\n\nRound-Robin: A setup in which each team plays in turn against every other.")
    rounds = input("\n\nPlease enter how many round-robins you would like to play with these teams (between 1 and 5): ")
    # Ensures that an appropriate amount of rounds is entered.
    while rounds not in ["1", "2", "3", "4", "5"]:
        rounds = input("\nERROR: Please enter an integer between 1 and 5 (inclusive): ")
    rounds = int(rounds)

    # Teams initially stored to dictionary in form team : seed
    teams_dictionary = team_dictionary_generator(file_path)

    print("\n- 1: The better seeded teams are heavily favored\n- 2: The better seeded teams are moderately favored\n"
          "- 3: The better seeded teams are slightly favored\n"
          "- 4: Every game is a toss up")
    level_of_randomness = input("\n\nEnter a level of randomness of 1-4: ")
    # Re-prompted until 1, 2, 3, or 4 is entered
    while level_of_randomness not in ["1", "2", "3", "4"]:
        level_of_randomness = input("\nERROR. Please enter a number 1 through 4: ")
    start_season(teams_dictionary, int(level_of_randomness), num_of_teams, rounds)


def start_season(teams_dictionary, level_of_randomness, num_of_teams, rounds):
    """
    Initiates the league season simulation. Creates Team objects from the provided dictionary, sets opponents,
    and plays rounds for the specified number of round-robins. The final standings are then sorted, ties are decided,
    and the league table is printed.

    CALLS: play_round, sort_final_table, decide_ties, print_table
    CALLED BY: main

    :param: teams_dictionary - contains all teams in format [str(team name) : int(seed)]
    :param: level_of_randomness - int suggesting how random the simulation is to be
    :param: num_of_teams - int
    :param: rounds - int representing how many round-robins are to be played
    """
    # temp_obj_list will hold all team objects without their opponent list filled in
    temp_obj_list = []
    for team in teams_dictionary:
        temp_obj_list.append(Team(team, teams_dictionary[team]))

    # temp_obj_list will hold all team objects WITH their opponent list filled in
    # NOTE: opponent lists are linear: team 1 holds all other 19 teams, team 2 holds 18 (all but self and team 1)...
    # To ensure that there are no duplicate matchups
    final_obj_list = []
    for i in range(len(temp_obj_list)):
        team = temp_obj_list[0]
        temp_obj_list.remove(team)
        team.set_opponent_list(temp_obj_list.copy())
        final_obj_list.append(team)
    temp_obj_list.clear()

    for i in range(rounds):
        play_round(final_obj_list, level_of_randomness, num_of_teams)

    # Final table is sorted in descending order of final points
    sort_final_table(final_obj_list, 0, len(final_obj_list) - 1)
    # Tiebreakers for if teams above are tied on GD
    decide_ties(final_obj_list)
    print_table(final_obj_list, rounds)
    num_of_teams_in_tourney = 0
    tournament = input("\nWould you like to play an end-of-season tournament? Enter 'y' for yes or 'n' for no: ")
    while tournament.lower() not in ['y', 'n']:
        tournament = input("\n\nERROR: Please enter 'y' or 'n': ")
    # Start of end-of-szn tournament
    if tournament.lower() == 'y':
        num_of_teams_in_tourney = get_teams(num_of_teams)
        bracket = generate_bracket(final_obj_list, num_of_teams_in_tourney)
        print(
            "\n- 1: The better seeded teams are heavily favored\n- 2: The better seeded teams are moderately favored\n"
            "- 3: The better seeded teams are slightly favored\n"
            "- 4: Every game is a toss up")
        level_of_randomness = input("\n\nEnter a level of randomness of 1-4: ")
        # Re-prompted until 1, 2, 3, or 4 is entered
        while level_of_randomness not in ["1", "2", "3", "4"]:
            level_of_randomness = input("\nERROR. Please enter a number 1 through 4: ")
        # Tournament simulation begins
        bracket_simulator(bracket, int(level_of_randomness), num_of_teams_in_tourney)
    end_of_sim_menu(final_obj_list, rounds, tournament.lower())


def end_of_sim_menu(final_obj_list, rounds, tournament):
    """
    Menu for viewing results of the simulation. Called after the simulation is over.

    CALLED BY: play_season
    CALLS: search_team_results, head_to_head_results, print_table

    :param final_obj_list: list of all Team objects
    :param rounds: number of round-robins played in the league regular season
    :param tournament - 'y' if one was played, 'n' if not

    """
    option = "1"
    while option != "0":
        print_menu()
        option = input("\nEnter 'A', 'B', 'C', 'D', OR '0' from the menu above: ")
        if option == 'A':
            search_team_results(final_obj_list)
        elif option == 'B':
            head_to_head_results(final_obj_list)
        elif option == 'C':
            print_table(final_obj_list, rounds)
        elif option == 'D':
            show_team_stats(final_obj_list, rounds, tournament)
        elif option != "0":
            print("\nPlease enter a valid selection.")


def show_team_stats(obj_list, rounds, tournament_played):
    """
        Shows in-depth statistics for each team's reg. season/playoff records

        CALLED BY: end_of_sim_menu
        CALLS: None

        :param obj_list: list of all Team objects
        :param rounds: number of round-robins played in the league regular season
        :param tournament_played - 'y' if one was played, 'n' if not
    """
    team = input("\nEnter a team name to view all of their statistics: ")
    # Ensures that entered teams is valid
    valid_team = False
    for obj in obj_list:
        if obj.get_team() == team:
            team = obj
            valid_team = True
            break
    # If the team is valid...
    if valid_team is True:
        print(f"\n{team.get_team()}:")
        print("---------------------")
        print(f"Regular Season Finish: {obj_list.index(team) + 1}")
        print(f"Regular Season Record (W-D-L): {team.get_wins()}-{team.get_draws()}-{team.get_losses()} "
              f"({(len(obj_list) - 1) * rounds} games)")
        print(f"Regular Season Goals: GF: {team.get_gf()}, GA: {team.get_ga()}, GD: {team.get_gd()}")
        # Prints tournament stats if a tournament was actually played
        if tournament_played == 'y':
            if len(team.get_playoff_game_list()) == 0:
                print(f"\n{team.get_team()} did not make the playoffs.")
            else:
                print("---------------------")
                print(f"Playoff Record (W-L): {team.get_playoff_wins()}-{team.get_playoff_losses()} ")
                print(f"Playoff Goals: GF: {team.get_playoff_gf()}, GA: {team.get_playoff_ga()}, "
                      f"GD: {team.get_playoff_gd()}")
    else:
        print("\nERROR: Invalid Team.")


def search_team_results(obj_list):
    """
    Prints the results of all of the entered team's games from the season/playoffs

    CALLED BY: end_of_sim_menu

    :param: final_obj_list - list of all team objects
    """
    team = input("\nEnter a team name to view all of their results: ")
    # Ensures that entered teams is valid
    valid_team = False
    for obj in obj_list:
        if obj.get_team() == team:
            team = obj
            valid_team = True
            break
    # If the team is valid...
    if valid_team is True:
        print("\nREGULAR SEASON:")
        print("-------------------")
        # Prints all regular season results via team1.get_game_list()
        for game in team.get_game_list():
            if team.get_team() == game.get_team1():
                print(game.get_team1(), " ", game.get_team1_goals(), " - ", game.get_team2_goals(), " ",
                      game.get_team2())
            else:
                print(game.get_team2(), " ", game.get_team2_goals(), " - ", game.get_team1_goals(), " ",
                      game.get_team1())
        # If they made the playoffs...
        if len(team.get_playoff_game_list()) != 0:
            print("\nPLAYOFFS:")
            print("-------------------")
            # Prints all regular season match-up results via team1.get_playoff_game_list()
            for game in team.get_playoff_game_list():
                if team.get_team() == game.get_team1():
                    print(game.get_team1(), " ", game.get_team1_goals(), " - ", game.get_team2_goals(), " ",
                          game.get_team2())
                else:
                    print(game.get_team2(), " ", game.get_team2_goals(), " - ", game.get_team1_goals(), " ",
                          game.get_team1())

    else:
        print("\nERROR: Invalid Team.")


def head_to_head_results(obj_list):
    """
    Prints the results of all head-to-head matchups between two given teams.

    CALLED BY: end_of_sim_menu

    :param: final_obj_list - list of all team objects
    """
    team1 = input("\nEnter the first team name: ")
    team2 = input("\nEnter the second team name: ")
    # Ensures that both team names entered are valid
    valid_team_count = 0
    for obj in obj_list:
        if obj.get_team() == team1:
            team1 = obj
            valid_team_count += 1
        elif obj.get_team() == team2:
            team2 = obj
            valid_team_count += 1
    # If both names are valid...
    if valid_team_count == 2:
        print("\nREGULAR SEASON:")
        print("-------------------")
        # Prints all regular season match-up results via team1.get_game_list()
        for game in team1.get_game_list():
            if team2.get_team() == game.get_team1():
                print(game.get_team1(), " ", game.get_team1_goals(), " - ", game.get_team2_goals(), " ",
                      game.get_team2())
            elif team2.get_team() == game.get_team2():
                print(game.get_team2(), " ", game.get_team2_goals(), " - ", game.get_team1_goals(), " ",
                      game.get_team1())
        # Checks to make sure both teams made playoffs
        if len(team1.get_playoff_game_list()) != 0 and len(team2.get_playoff_game_list()) != 0:
            # Prints all playoff match-up results via team1.get_playoff_game_list()
            print("\nPLAYOFFS:")
            print("-------------------")
            for game in team1.get_playoff_game_list():
                if team2.get_team() in [game.get_team1(), game.get_team2()]:
                    print(game.get_team1(), " ", game.get_team1_goals(), " - ", game.get_team2_goals(), " ",
                          game.get_team2())
    else:
        print("\nERROR: Invalid Team.")


def print_menu():
    """
        CALLED BY: end_of_sim_menu
    """
    print("\n\n*************** MENU ***************")
    print("\tA. Search Team Game Results")
    print("\tB. View Head to Head Records")
    print("\tC. Show Regular Season Table")
    print("\tD. Search Final Team Stats")
    print("\t0. Exit Menu")


def bracket_simulator(bracket, level_of_randomness, num_of_teams):
    """
    Simulates the bracket by putting teams from bracket against each other in select matchups and
    subsequently re-adding the winner to the next round. This is done until one team remains.

    CALLS: game_simulator, bracket_shell_printer, bracket_simulator (recursive)
    CALLED BY: start_season

    :param: bracket - list of all team objects in the order they'll play the first round of the tournament
    :param: level_of_randomness: The option (1, 2, 3, or 4) picked by the user.
    :param: num_of_teams: The number of teams in the bracket
    """
    # Prints which round of the tournament is being played.
    if len(bracket) >= 16:
        print(f"\n\nROUND OF {len(bracket)}: ")
    elif len(bracket) == 8:
        print("\n\nQUARTERFINALS: ")
    elif len(bracket) == 4:
        print("\n\nSEMIFINALS: ")
    elif len(bracket) == 2:
        print("\n\nCHAMPIONSHIP: ")
    # Simulates each individual game for the round.
    new_bracket = []
    for i in range(0, len(bracket), 2):
        # Decides which team lost the individual game being simulated via the game_simulator function.
        knocked_out = game_simulator(bracket[i], bracket[i + 1], level_of_randomness, num_of_teams)
        # Declares winner of the individual game being simulated as the team not stored in knocked_out.
        if bracket[i] == knocked_out:
            winner = bracket[i + 1]
        else:
            winner = bracket[i]
        # Updates Team objects
        get_score(winner, knocked_out, True)
        # Prints both teams from the game in a bracket shell with the winner included in the next round.
        print(f"\n\n{bracket[i].get_playoff_seed()}: {bracket[i].get_team()}")
        bracket_shell_printer(winner)
        print(f"{bracket[i + 1].get_playoff_seed()}: {bracket[i + 1].get_team()}")
        # Prints the champion and runner-up after the final game.
        if len(bracket) == 2:
            print(f"\n\nCHAMPION: {winner.get_playoff_seed()}: {winner.get_team()}")
            print(f"RUNNER-UP: {knocked_out.get_playoff_seed()}: {knocked_out.get_team()}")
        # Adds the winner to the bracket for the next round
        new_bracket.append(winner)

    bracket = new_bracket.copy()
    # Recursively calls bracket_simulator with the updated dictionary until only one team still stands in the
    # tournament.
    if len(bracket) != 1:
        bracket_simulator(bracket, level_of_randomness, num_of_teams)


def bracket_shell_printer(winner):
    """
    Prints the rectangular bracket shell for each individual game with the winner and their seed printed
    on a line to the right of the shell.

    CALLS: none
    CALLED BY: bracket_simulator

    :param: winner: The winner of the individual game.
    :param: seed: The seed of the winner of the individual game.
    """
    print(f"--------------------|\n\t\t\t\t\t|\n\t\t\t\t\t|\t{winner.get_playoff_seed()}: {winner.get_team()}\n\t\t\t"
          f"\t\t|--------------------"
          f"\n\t\t\t\t\t|\n--------------------|")


def game_simulator(team1, team2, level_of_randomness, num_of_teams):
    """
    Simulates each individual game in the tournament using weighted seeding differences and a generated scale
    factor.

    CALLS: scale_factor
    CALLED BY: bracket_simulator

    :param: team1/team2 - Team objects of the two teams playing
    :param: level_of_randomness - user selected option 1-4 (passed as int)
    :param: num_of_teams

    :return: knocked_out - Team object of the team that lost the game.
    """
    # Calculates the percent difference in seeds of the two teams playing (used for generating scale factor).
    weighted_seed_diff = abs(team2.get_playoff_seed() - team1.get_playoff_seed()) / num_of_teams
    # Figures out which of the two seeds is better (closer to 1).
    better_seed = min(team1.get_playoff_seed(), team2.get_playoff_seed())
    # If option 1, 2, or 3 was chosen by the user, a scale factor is generated alongside a random number
    # used for picking a winner based on weighted_seed_diff.
    if level_of_randomness in [1, 2, 3]:
        sf = scale_factor(weighted_seed_diff, level_of_randomness, num_of_teams)
        rand_num = random.randint(1, 100)
        # If the random number (between 1 and 100 inclusive) is less than the scale factor, the team that
        # has the worse seed of the two teams is returned.
        if rand_num <= sf:
            if better_seed == team1.get_playoff_seed():
                return team2
            else:
                return team1
        # If the random number (between 1 and 100 inclusive) is more than the scale factor, the team that
        # has the better seed of the two teams is returned. This is considered an "upset".
        else:
            if better_seed == team1.get_playoff_seed():
                return team1
            else:
                return team2
    # If the user picked option 4 (every game is a 50/50 shot) then either int 1 or 2 is randomly generated and
    # the team (team1 or team2) with that number is returned.
    elif level_of_randomness == 4:
        if random.randint(1, 2) == 1:
            return team1
        else:
            return team2


def scale_factor(difference, option, lowest_seed):
    """
    Determines a scale factor used for deciding which team will win the game being simulated. If the randomly
    generated number (1-100) in game_simulator is below sf, the favorite (better seed) will win but if it is above sf,
    the underdog (lower seed) will win.

    CALLS: none
    CALLED BY: game_simulator

    :param: difference: The percent difference in seeds of the two teams playing.
            - Equation = (worse seed - better seed) / lowest seed
    :param: option: The option the user picked in the previous menu.
    :param: lowest_seed: The seed of the worst team(s) in the bracket.

    :return: sf: Scale factor used for deciding who will win the game in game_simulator.
    :rtype: int
    """
    # Determines scale factor based on option and weighted difference. This can be thought of as assigning the
    # better seed a [sf] % chance of winning the individual match-up.
    if option == 1:
        if difference >= .75:
            sf = 99
        elif 0.5 <= difference < 0.75:
            sf = 90
        elif 0.25 <= difference < 0.5:
            sf = 82
        else:
            sf = 75
    elif option == 2:
        if difference >= .75:
            sf = 88
        elif 0.5 <= difference < 0.75:
            sf = 80
        elif 0.25 <= difference < 0.5:
            sf = 72
        else:
            sf = 68
    else:
        if difference >= .75:
            sf = 80
        elif 0.5 <= difference < 0.75:
            sf = 70
        elif 0.25 <= difference < 0.5:
            sf = 55
        else:
            sf = 50
    # Adds 10 to the scale factor if the lowest seed is a 32 or higher. This is to ensure that with a higher variability
    # of teams, the top teams still have a distinct advantage.
    if lowest_seed >= 32:
        sf += 10
    # Subtracts 5 from the scale factor if the option is 1 or 2 and the lowest seed is 8 or smaller. This is to
    # ensure that top teams aren't given a vastly disproportionate advantage.
    elif lowest_seed <= 8:
        if option in [1, 2]:
            sf -= 5
    return sf


def generate_bracket(final_obj_list, final_size):
    """
    Generates the seed structure for the bracket based on its proposed size
    and then associates the proper team object with each seed.

    CALLS: none
    CALLED BY: main
    :param: final_obj_list - final list of all Team objects in descending order of points
    :param: final_size - the proposed length of the final bracket

    :return: bracket list (see above description)
    """
    bracket = [1, 2]

    # Expands the bracket outwards (ex: [1,2] -> [1,4,2,3])
    while len(bracket) < final_size:
        new_bracket = [0] * len(bracket) * 2
        # Initializes even indices as already present seeds
        for i in range(len(bracket)):
            new_bracket[i * 2] = bracket[i]
        # Initializes odd indices as new seed to play against
        for i in range(len(bracket)):
            new_bracket[i * 2 + 1] = (len(new_bracket) + 1) - bracket[i]
        # Restores list to main location
        bracket = new_bracket.copy()

    # Changes the bracket list so that team objects are stored where there seeds were placed from above
    for i in range(len(bracket)):
        seed = bracket[i]
        for j in final_obj_list:
            if final_obj_list.index(j) + 1 == bracket[i]:
                bracket[i] = j
                j.set_playoff_seed(seed)

    return bracket


def get_teams(table_length):
    """
    Asks user for number of teams to be put into bracket and verifies that the number
    is valid (number must be in total_teams_list) via input validation.

    CALLS: none
    CALLED BY: main

    :param: table_length - the number of teams in the table

    :return: num_of_teams: Total number of teams to be put into the bracket.
    :rtype: int
    """
    num_of_teams = 0
    total_teams_list = (2, 4, 8, 16, 32, 64, 128, 256)
    # Will ask user to re-enter value until a number from total_teams_list is entered.
    while num_of_teams not in total_teams_list:
        print("\nOPTIONS: 2, 4, 8, 16, 32, 64, 128, 256")
        num_of_teams = input("\nHow many teams total in the bracket? (Pick a number from above that is less than"
                             f" or equal to {table_length}): ")
        if not num_of_teams.isdigit():
            print(f"\nERROR. Please give a number from the options list less than {num_of_teams}.")
        elif int(num_of_teams) not in total_teams_list or int(num_of_teams) > table_length:
            print(f"\nERROR. Please give a number from the options list less than {num_of_teams}.")
        else:
            num_of_teams = int(num_of_teams)
    return num_of_teams


def team_dictionary_generator(file):
    """
    The teams and seeds are read into dict_teams for storage and correlation in the format team_name: seed.

    CALLS: team_dictionary_generator, file_validity_checker, start_season
    CALLED BY: main

    :param: file - the absolute path to the verified file containing all teams and seeds

    :return: dict_teams (see first note)
    """
    file = open(file, "r")
    dict_teams = {}
    for line in file:
        line_list = line.split(":")
        dict_teams[line_list[1].strip()] = int(line_list[0].strip())
    file.close()
    return dict_teams


def print_table(final_obj_list, rounds):
    """
    Prints the league table with detailed statistics for each team including games played, wins, draws, losses,
    goals for, goals against, goal difference, and points.

    CALLED BY: start_season

    :param: final_obj_list - final list of all Team objects in descending order of points
    :param: rounds - int representing how many round-robins have been played
    """
    print("\n       TEAM                                                     "
          "GP       W         D        L       GF       GA       GD      PTS")
    print("---------------------------------------------------------------------------"
          "--------------------------------------------------------")
    count = 0
    for team in final_obj_list:
        count += 1
        print("{:>3}. {:<50} {:>10} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8} {:>8}".format(count, team.get_team(),
                                                                                      str((len(final_obj_list) - 1)
                                                                                          * rounds),
                                                                                      str(team.get_wins()),
                                                                                      str(team.get_draws()),
                                                                                      str(team.get_losses()),
                                                                                      str(team.get_gf()),
                                                                                      str(team.get_ga()),
                                                                                      str(team.get_gd()),
                                                                                      str(team.get_points())
                                                                                      ))


def decide_ties(final_obj_list):
    """
    Decides which teams are level on points, sending them to check_criteria to figure out proper order.

    CALLS: check_criteria, swap
    CALLED BY: decide_ties

    :param: final_obj_list - final list of all Team objects in descending order of points
    """
    team_pts = {}
    for i in final_obj_list:
        if i.get_points() not in team_pts.keys():
            team_pts[i.get_points()] = i
        else:
            check_criteria(final_obj_list, i)


def check_criteria(final_obj_list, tied_team):
    """
    Check tiebreaker criteria for teams with the same number of points. The criteria include highest goal difference
    (gd), most goals scored (gf), and least goals against (ga) (in that order). Teams are sorted accordingly.

    * Selection sort algorithm x 3 - picked because of small lists being passed

    CALLS: swap
    CALLED BY: decide_ties

    :param: final_obj_list - final list of all Team objects in descending order of points
    :param: tied_team - Team object of team that is tied on points with a team above it
    """
    same_pts = []
    for j in final_obj_list:
        if j.get_points() == tied_team.get_points():
            same_pts.append(j)

    # Check for GD - sorted accordingly
    still_tied_list = []
    decided = 0
    for i in range(len(same_pts)):
        j = i + 1
        while j < len(same_pts):
            if same_pts[i].get_gd() < same_pts[j].get_gd():
                swap(final_obj_list, final_obj_list.index(same_pts[i]), final_obj_list.index(same_pts[j]))
            elif same_pts[i].get_gd() == same_pts[j].get_gd():
                decided = 1
                still_tied_list.append(same_pts[i])
                still_tied_list.append(same_pts[j])
            j += 1

    # Check for GF if above is tied - sorted accordingly
    gf_still_tied_list = []
    if decided == 1:
        for i in range(len(still_tied_list)):
            j = i + 1
            while j < len(still_tied_list):
                if still_tied_list[i].get_gf() < still_tied_list[j].get_gf():
                    swap(final_obj_list, final_obj_list.index(still_tied_list[i]),
                         final_obj_list.index(still_tied_list[j]))
                elif still_tied_list[i].get_gf() == still_tied_list[j].get_gf():
                    decided = 2
                    gf_still_tied_list.append(still_tied_list[i])
                    gf_still_tied_list.append(still_tied_list[j])
                j += 1

    # Check for ga if above is still tied - sorted accordingly
    if decided == 2:
        for i in range(len(gf_still_tied_list)):
            j = i + 1
            while j < len(gf_still_tied_list):
                if gf_still_tied_list[i].get_ga() < gf_still_tied_list[j].get_ga():
                    swap(final_obj_list, final_obj_list.index(gf_still_tied_list[i]),
                         final_obj_list.index(gf_still_tied_list[j]))
                j += 1


def sort_final_table(final_obj_list, left, right):
    """
    Sorts the final list of teams based on their points in descending order using the quicksort algorithm.
    Teams with more points are placed higher in the list.

    CALLS: swap
    CALLED BY: start_season

    :param: final_obj_list - final list of all Team objects in descending order of points
    :param: rounds - int left/right - location of left/right (i and j respectively) incremental bounds in quicksort
    """
    if left < right:
        pivot_index = partition(final_obj_list, left, right)
        sort_final_table(final_obj_list, left, pivot_index - 1)
        sort_final_table(final_obj_list, pivot_index + 1, right)


def partition(final_obj_list, left, right):
    """
    Partitions the list for the quicksort algorithm. It selects a pivot value, rearranges the list
    so that elements less than the pivot are on the left, and elements greater than the pivot are on the right.

    CALLED BY: sort_final_table

    :param: final_obj_list - final list of all Team objects in descending order of points
    :param: rounds - int left/right - location of left/right (i and j respectively) incremental bounds in quicksort

    :return: i + 1 - int representing the next pivot value
    """
    pivot_value = final_obj_list[right].get_points()
    i = left - 1
    for j in range(left, right):
        if final_obj_list[j].get_points() >= pivot_value:
            i += 1
            swap(final_obj_list, i, j)
    swap(final_obj_list, i + 1, right)
    return i + 1


def swap(final_obj_list, i, j):
    """
    Swaps two elements in the team object list.

    CALLED BY: sort_final_table, check_criteria

    :param: final_obj_list - final list of all Team objects in descending order of points
    :param: rounds - int i/j - location of left/right (i and j respectively) incremental bounds in quicksort to be
    swapped
    """
    temp = final_obj_list[i]
    final_obj_list[i] = final_obj_list[j]
    final_obj_list[j] = temp


def play_round(final_obj_list, level_of_randomness, num_of_teams):
    """
    Calls play_game for each combination of teams.
    Every team plays every team once per round.

    CALLS: play_game
    CALLED BY: start_season

    :param: final_obj_list - final list of all Team objects in descending order of points
    :param: level_of_randomness - int suggesting how random the simulation is to be
    :param: num_of_teams - int
    """
    for team in final_obj_list:
        for opponent in team.get_opponent_list():
            play_game(team, opponent, level_of_randomness, num_of_teams)


def play_game(team1, team2, level_of_randomness, num_of_teams):
    """
    Simulates individual games, generating wins, draws, and losses based on random number generation.

    CALLS: play_game
    CALLED BY: start_season

    :param team1 - the first team playing the game.
    :param team2 - the second team playing the game.
    :param level_of_randomness - an integer representing the level of randomness in the game (1 to 4).
    :param num_of_teams - the total number of teams in the tournament.
    """
    weighted_seed_diff = float(abs(team1.get_seed() - team2.get_seed()) / num_of_teams)
    better_team = min(team1.get_seed(), team2.get_seed())
    if better_team == team1.get_seed():
        better_team = team1
        worse_team = team2
    else:
        better_team = team2
        worse_team = team1

    # Gets the chances for a win, loss, or tie from get_result
    odds_boundaries = get_result(weighted_seed_diff, level_of_randomness)
    win_ceiling = odds_boundaries[0]
    draw_ceiling = odds_boundaries[1]
    result = random.randint(1, 100)
    # If the random number is under odds_boundary[0], the better team wins
    if result <= win_ceiling:
        winning_team = better_team
        winning_team.incr_wins()
        losing_team = worse_team
        losing_team.incr_losses()
    # If the random number is between odds_boundary[0] and [1], a tie occurs
    elif result <= draw_ceiling:
        winning_team = None
        losing_team = None
        team1.incr_draws()
        team2.incr_draws()
    # If the random number is above odds_boundary[1], the worse team wins
    else:
        winning_team = worse_team
        winning_team.incr_wins()
        losing_team = better_team
        losing_team.incr_losses()
    get_score(winning_team, losing_team, False, team1, team2)


def get_score(winning_team, losing_team, playoffs, team1=None, team2=None):
    """
    Determines the score of a game based on the result (W, D, L).
    In the case of a draw, scores are randomly generated.
    Otherwise, goals are determined using a directed strategy of determining possible outcomes.

    CALLED BY: play_game

    :param winning_team - the team that wins the game (or None in the case of a draw).
    :param losing_team - the team that loses the game (or None in the case of a draw).
    :param team1 - the first team playing the game.
    :param team2 - the second team playing the game
    :param playoffs - True if playoff game, False otherwise
    """
    # Tuple is where score values are randomly picked from
    score_tuple = [0] * 19 + [1] * 22 + [2] * 11 + [3] * 7 + [4] * 2 + [5]

    # For if a tie has occurred
    if winning_team is None:
        # Random number chosen from score_tuple
        tie_goals = score_tuple[random.randint(0, len(score_tuple) - 1)]
        # Team objects updated accordingly
        team1.add_game(Game(team1.get_team(), tie_goals, team2.get_team(), tie_goals, "Draw"))
        team2.add_game(Game(team1.get_team(), tie_goals, team2.get_team(), tie_goals, "Draw"))
        team1.incr_gf(tie_goals)
        team1.incr_ga(tie_goals)
        team2.incr_gf(tie_goals)
        team2.incr_ga(tie_goals)
    else:
        # Random number chosen from score_tuple (can't be 5)
        losing_team_goals = score_tuple[random.randint(0, len(score_tuple) - 2)]
        # Random number chosen from score_tuple (can't be 0)
        winning_team_goals = score_tuple[random.randint(19, len(score_tuple) - 1)]
        # winning_team_goals regenerated until it is greater than losing_team_goals
        while winning_team_goals <= losing_team_goals:
            winning_team_goals = score_tuple[random.randint(20, len(score_tuple) - 1)]
        # Team objects updated accordingly
        if playoffs is False:
            team1.add_game(Game(winning_team.get_team(), winning_team_goals, losing_team.get_team(), losing_team_goals,
                                winning_team.get_team()))
            team2.add_game(Game(winning_team.get_team(), winning_team_goals, losing_team.get_team(), losing_team_goals,
                                winning_team.get_team()))
            winning_team.incr_gf(winning_team_goals)
            winning_team.incr_ga(losing_team_goals)
            losing_team.incr_gf(losing_team_goals)
            losing_team.incr_ga(winning_team_goals)
        else:
            winning_team.add_playoff_game(
                Game(winning_team.get_team(), winning_team_goals, losing_team.get_team(), losing_team_goals,
                     winning_team.get_team()))
            winning_team.incr_playoff_wins()
            winning_team.incr_playoff_gf(winning_team_goals)
            winning_team.incr_playoff_ga(losing_team_goals)
            losing_team.add_playoff_game(
                Game(winning_team.get_team(), winning_team_goals, losing_team.get_team(), losing_team_goals,
                     winning_team.get_team()))
            losing_team.incr_playoff_losses()
            losing_team.incr_playoff_gf(losing_team_goals)
            losing_team.incr_playoff_ga(winning_team_goals)


def get_result(weighted_seed_diff, level_of_randomness):
    """
    Determines the win, draw, and loss probabilities based on the level of randomness.

    win_probability = [(chance for better seed to win), (stacked chance for draw)] - anything beyond [1] means loss

    CALLED BY: play_game

    :param weighted_seed_diff - the weighted difference in seeds between two teams.
    :param level_of_randomness - an integer representing the level of randomness in the game (1 to 4).

    :return: a list of two numbers (see win_probability above)
    """
    if level_of_randomness == 1:
        if weighted_seed_diff >= 0.6:
            win_probability = [80, 90]
        elif weighted_seed_diff >= 0.2:
            win_probability = [70, 85]
        else:
            win_probability = [60, 75]
    elif level_of_randomness == 2:
        if weighted_seed_diff >= 0.6:
            win_probability = [70, 85]
        elif weighted_seed_diff >= 0.2:
            win_probability = [55, 75]
        else:
            win_probability = [45, 75]
    elif level_of_randomness == 3:
        if weighted_seed_diff >= 0.6:
            win_probability = [60, 75]
        elif weighted_seed_diff >= 0.2:
            win_probability = [45, 70]
        else:
            win_probability = [38, 70]
    else:
        win_probability = [33, 67]
    return win_probability


def file_validity_checker(file_path, num_of_teams):
    """
    Checks the validity of the provided file path and the format of the seeded teams.
    Verifies that the file contains unique teams sorted from 1 through num_of_teams.

    CALLED BY: main

    :param file_path - the absolute file path to the list of seeded teams.
    :param num_of_teams - the total number of teams in the tournament.

    :return: boolean value representing if the file is valid or not
    """
    valid = True
    count = 0
    team_repetition_checker = []
    try:
        file = open(file_path, 'r')
        for line in file:
            count += 1
            line_list = line.split(":")
            # Invalid if there isn't exactly 1 team for every seed 1-num_of_teams or duplicate team is found
            if line_list[0] != str(count) or line_list[1] in team_repetition_checker:
                valid = False
                break
            team_repetition_checker.append(line_list[1])
        file.close()
    except Exception:
        valid = False
    return valid and count == num_of_teams


if __name__ == '__main__':
    main()
