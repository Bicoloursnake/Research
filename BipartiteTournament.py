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
        """Randomly chooses a winner between competitors based on their respective ratings"""
        win_sum = self.team1Wins[player1] + self.team2Wins[player2] + 2
        random_number = random.randint(1, win_sum)
        if random_number <= self.team1Wins[player1] + 1:
            self.team1Wins[player1] += 1
            self.team2Losses[player2] += 1
        else:
            self.team2Wins[player2] += 1
            self.team1Losses[player1] += 1

    def determine_weight(self, player1: int, player2: int) -> int:
        """Determines weight of a match based on difference of ratings multiplied by the denominator in order
        to be able to work with integers only"""
        return int(math.fabs(self.team1Wins[player1] - self.team2Wins[player2]))

    def determine_weights(self):
        """Uses entry weights to fill in the matrix. The multiplication by negative 1 happens to convert
        the minimum linear assignment problem into a maximum linear assignment problem, and a large constant
        is used to keep all values positive"""
        for row_num in range(self.teamSize):
            for col_num in range(self.teamSize):
                if self.matrix[row_num][col_num] <= self.teamSize ** 2:
                    self.matrix[row_num][col_num] = (self.teamSize ** 2) - self.determine_weight(row_num, col_num)

    def update_ratings(self, current_round_number: int):
        """Used to store ratings as floating point values, but to avoid compounding floating point errors, doesn't
        use its previous value to determine the new value, instead using the integer win count"""
        for num in range(self.teamSize):
            self.team1Ratings[num] = (self.team1Wins[num] + 1) / (current_round_number + 2)
            self.team2Ratings[num] = (self.team2Wins[num] + 1) / (current_round_number + 2)

    def run_round(self, current_round_number: int) -> int:
        """Runs a round, using the various other functions to determine a winner, update the weight matrix, and
        update the ratings and win counts"""
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


numberOfTournaments: int = 1000
numberOfPlayers: int = 10
for tournamentNumber in range(numberOfTournaments):
    tournament: BipartiteTournament = BipartiteTournament(numberOfPlayers)
    stringToWrite: str = ""
    for round_number in range(numberOfPlayers):
        stringToWrite += str(tournament.run_round(round_number+1)) + ","
    stringToWrite = stringToWrite[0: len(stringToWrite) - 1]
    stringToWrite += "\n"
    with open("results.csv", "a") as targetFile:
        targetFile.write(stringToWrite)
