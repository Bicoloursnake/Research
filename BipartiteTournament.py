import random
import math
from scipy.optimize import linear_sum_assignment


def determine_winner(player1: int, player2: int):
    win_sum = team1Wins[player1] + team2Wins[player2] + 2
    random_number = random.randint(1, win_sum)
    if random_number <= team1Wins[player1] + 1:
        team1Wins[player1] += 1
        team2Losses[player2] += 1
    else:
        team2Wins[player2] += 1
        team1Losses[player1] += 1


def determine_weight(player1: int, player2: int) -> int:
    return int(math.fabs(team1Wins[player1] - team2Wins[player2]))


def determine_weights():
    for row_num in range(teamSize):
        for col_num in range(teamSize):
            if matrix[row_num][col_num] <= teamSize ** 2:
                matrix[row_num][col_num] = (teamSize ** 2) - determine_weight(row_num, col_num)


def update_ratings(round_number: int):
    for num in range(teamSize):
        team1Ratings[num] = (team1Wins[num] + 1) / (round_number + 2)
        team2Ratings[num] = (team2Wins[num] + 1) / (round_number + 2)


def run_round(round_number: int) -> int:
    row, col = linear_sum_assignment(matrix)
    final_sum: int = 0
    for index in range(teamSize):
        weight_for_sum: int = teamSize ** 2 - matrix[row[index]][col[index]]
        final_sum += weight_for_sum
        print(row[index], col[index], team1Wins[row[index]], team2Wins[col[index]], weight_for_sum)
        matrix[row[index]][col[index]] = math.inf
        determine_winner(row[index], col[index])
    determine_weights()
    update_ratings(round_number)
    return final_sum


teamSize: int = 4
matrix: list[list[float]] = []
team1Wins: list[int] = []
team2Wins: list[int] = []
team1Losses: list[int] = []
team2Losses: list[int] = []
team1Ratings: list[float] = []
team2Ratings: list[float] = []

for i in range(teamSize):
    matrix.append([])
    team1Wins.append(0)
    team2Wins.append(0)
    team1Losses.append(0)
    team2Losses.append(0)
    team1Ratings.append(1)
    team2Ratings.append(1)
    for j in range(teamSize):
        matrix[i].append(0)


for i in range(teamSize):
    print(run_round(i+1))
    ratingsSum = 0.0
    for rating in team2Ratings:
        ratingsSum += rating
    for rating in team1Ratings:
        ratingsSum += rating
