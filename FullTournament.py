import random
import math


def determine_winner(player1: int, player2: int):
    print(player1, player2)
    win_sum = playerList[player1] + playerList[player2]
    random_number = random.randint(1, win_sum + 2)
    if random_number <= playerList[player1] + 1:
        playerList[player1] += 1
    else:
        playerList[player2] += 1


def determine_weight(player1: int, player2: int) -> int:
    return int(math.fabs(playerList[player1] - playerList[player2]))


def determine_weights():
    for entry in range(len(roundWeights)):
        if roundWeights[entry] >= 0:
            round_weight: int = 0
            if tournamentSize % 2 == 0:
                for i in range((tournamentSize // 2) - 1):
                    round_weight += \
                        determine_weight((i + 1 + entry) % (tournamentSize - 1),
                                         (entry - 1 - i) % (tournamentSize - 1))
                round_weight += determine_weight(entry, tournamentSize - 1)
            else:
                for i in range(tournamentSize // 2):
                    round_weight += \
                        determine_weight((i + 1 + entry) % tournamentSize,
                                         (entry - 1 - i) % tournamentSize)
            roundWeights[entry] = round_weight


def run_round():
    """Runs the round of greatest weight in the tournament.
    If it finds multiple, runs the round of lowest ordinal
     and greatest weight."""
    heaviest_round: int = 0
    for entry in range(len(roundWeights)):
        if roundWeights[entry] > roundWeights[heaviest_round]:
            heaviest_round = entry
    print(heaviest_round)
    roundWeights[heaviest_round] = -1
    if tournamentSize % 2 == 0:
        determine_winner(heaviest_round, tournamentSize-1)
        for i in range((tournamentSize // 2) - 1):
            player1: int = (i + 1 + heaviest_round) % (tournamentSize - 1)
            player2: int = (heaviest_round - i - 1) % (tournamentSize - 1)
            determine_winner(player1, player2)
    else:
        for i in range(tournamentSize // 2):
            player1: int = (i + 1 + heaviest_round) % tournamentSize
            player2: int = (heaviest_round - i - 1) % tournamentSize
            determine_winner(player1, player2)


tournamentSize: int = 4
playerList: list[int] = []
roundWeights: list[int] = []

for j in range(tournamentSize):
    playerList.append(0)

for j in range(tournamentSize + (tournamentSize % 2) - 1):
    roundWeights.append(0)

for j in range(tournamentSize + (tournamentSize % 2) - 1):
    print(playerList)
    print(roundWeights)
    run_round()
    determine_weights()
