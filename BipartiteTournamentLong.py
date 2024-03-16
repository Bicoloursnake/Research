import random
import math
from HungarianAlgorithm import maximum_weight_matching


def determine_winner(player1: int, player2: int):
    win_sum = team1[player1] + team2[player2]
    random_number = random.randint(1, win_sum + 2)
    if random_number <= team1[player1] + 1:
        team1[player1] += 1
    else:
        team2[player2] += 1


def determine_weight(player1: int, player2: int) -> int:
    return int(math.fabs(team1[player1] - team2[player2]))


def determine_weights():
    for row_num in range(teamSize):
        for col_num in range(teamSize):
            if matrix[row_num][col_num] > 0:
                matrix[row_num][col_num] = determine_weight(row_num, col_num) + (2 ** teamSize)


def run_round():
    matching_matrix: list[list[int]] = maximum_weight_matching(matrix)
    print(matching_matrix)
    for row in range(len(matching_matrix)):
        for col in range(len(matching_matrix[0])):
            if matching_matrix[row][col] == 1:
                matrix[row][col] = 0
                determine_winner(row, col)
    determine_weights()


teamSize: int = 5
matrix: list[list[int]] = []
team1: list[int] = []
team2: list[int] = []

for i in range(teamSize):
    matrix.append([])
    team1.append(0)
    team2.append(0)
    for j in range(teamSize):
        matrix[i].append(2 ** teamSize)

for i in range(teamSize):
    run_round()
    print(matrix)
    print(team1)
    print(team2)

