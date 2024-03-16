from math import fabs

powerOfTwo: int = 3
listToAddTo: list[list[int]] = []
otherList: list[list[int]] = []
for i in range(2 ** powerOfTwo):
    listToAddTo.append([])
    otherList.append([])
    for j in range(2 ** powerOfTwo):
        listToAddTo[i].append(i ^ j)
        otherList[i].append(int(fabs((i ^ j) - i)))

for i in range(2 ** powerOfTwo):
    print(listToAddTo[i])

print()

for i in range(2 ** powerOfTwo):
    print(otherList[i])
