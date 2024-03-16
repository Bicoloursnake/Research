import math

roundsPlayed: int = 400
numerator: int = 0
denominator: int = 2 ** (2 * roundsPlayed)
for i in range(roundsPlayed + 1):
    for j in range(roundsPlayed + 1):
        numerator += math.comb(roundsPlayed, i) * math.comb(roundsPlayed, j) * int(math.fabs(i - j))

print(numerator/denominator)
