import random
import math
from scipy.optimize import linear_sum_assignment


class BipartiteTournament:
    """A class to facilitate running many Bipartite Round Robin Tournaments"""
    teamSize: int = 8
    matrix: list[list[float]] = []
    team1Wins: list[int] = []
    team2Wins: list[int] = []
    team1Losses: list[int] = []
    team2Losses: list[int] = []
    team1Ratings: list[float] = []
    team2Ratings: list[float] = []

    def __init__(self, number_of_players: int):
        self.teamSize: int = number_of_players
        self.matrix: list[list[float]] = []
        self.team1Wins: list[int] = []
        self.team2Wins: list[int] = []
        self.team1Losses: list[int] = []
        self.team2Losses: list[int] = []
        self.team1Ratings: list[float] = []
        self.team2Ratings: list[float] = []
        for number in range(number_of_players):
            self.matrix.append([])
            self.team1Wins.append(0)
            self.team2Wins.append(0)
            self.team1Losses.append(0)
            self.team2Losses.append(0)
            self.team1Ratings.append(1)
            self.team2Ratings.append(1)
            for j in range(number_of_players):
                self.matrix[number].append(0)

    def determine_winner(self, player1: int, player2: int):
        win_sum = self.team1Wins[player1] + self.team2Wins[player2] + 2
        random_number = random.randint(1, win_sum)
        if random_number <= self.team1Wins[player1] + 1:
            self.team1Wins[player1] += 1
            self.team2Losses[player2] += 1
        else:
            self.team2Wins[player2] += 1
            self.team1Losses[player1] += 1

    def determine_weight(self, player1: int, player2: int) -> int:
        return int(math.fabs(self.team1Wins[player1] - self.team2Wins[player2]))

    def determine_weights(self):
        for row_num in range(self.teamSize):
            for col_num in range(self.teamSize):
                if self.matrix[row_num][col_num] <= self.teamSize ** 2:
                    self.matrix[row_num][col_num] = (self.teamSize ** 2) - self.determine_weight(row_num, col_num)

    def update_ratings(self, current_round_number: int):
        for num in range(self.teamSize):
            self.team1Ratings[num] = (self.team1Wins[num] + 1) / (current_round_number + 2)
            self.team2Ratings[num] = (self.team2Wins[num] + 1) / (current_round_number + 2)

    def run_round(self, current_round_number: int) -> int:
        row, col = linear_sum_assignment(self.matrix)
        final_sum: int = 0
        for index in range(self.teamSize):
            weight_for_sum: int = self.determine_weight(row[index], col[index])
            final_sum += weight_for_sum
            self.matrix[row[index]][col[index]] = math.inf
            self.determine_winner(row[index], col[index])
        self.determine_weights()
        self.update_ratings(current_round_number)
        return final_sum


numberOfTournaments: int = 40
for tournamentNumber in range(numberOfTournaments):
    numberOfPlayers: int = 4
    tournament: BipartiteTournament = BipartiteTournament(numberOfPlayers)

    for round_number in range(numberOfPlayers):
        print("Tournament Number " + str(tournamentNumber + 1) +
              " Round " + str(round_number + 1) + " sum of rating differences: "
              + str(tournament.run_round(round_number+1)) + "/" + str(round_number+2))

