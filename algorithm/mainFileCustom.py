data = [
                ["Wisc", "Colo", 80],
                ["Colo", "Wisc", 70],
                ["NJ", "Colo", 200],
                ["Colo", "NJ", 340],
                ["Wisc", "NJ", 90],
                ["Wisc", "Ark", 40],
                ["Ark", "Wisc", 50],
                ["Ark", "Colo", 60],
                ["Colo", "Ark", 50],
                ["Ark", "NJ", 110],
                ["NJ", "Wisc", 80],
                ["Wash", "Wisc", 240],
                ["Wash", "Colo", 30],
                ["Wash", "Wisc", 530],
                ["Wash", "NJ", 300],
                ["Wisc", "Wash", 260],
                ["Colo", "Wash", 10],
                ["NJ", "Wash", 280],
                ["Ark", "Wash", 250]
            ]
airports = ["Colo", "Wisc", "Ark", "NJ", "Wash"]
n = len(airports)

hotels = [230, 130, 120, 300, 130]

maxCost = data[0][2]
for i in range(1, len(data)):
    if data[i][2] > maxCost:
        maxCost = data[i][2]

best = [[maxCost + 1 for i in range(n)] for j in range(n)]
prev = [[maxCost + 1 for i in range(n)] for j in range(n)]
for i in range(n):
    best[i][i] = 0
    prev[i][i] = i
for datum in data:
    if best[airports.index(datum[0])][airports.index(datum[1])] > datum[2]:
        best[airports.index(datum[0])][airports.index(datum[1])] = datum[2]
        prev[airports.index(datum[0])][airports.index(datum[1])] = airports.index(datum[0])



for k in range(n):
    for start in range(n):
        for dest in range(n):
            if best[start][k] + best[k][dest] < best[start][dest]:
                best[start][dest] = best[start][k] + best[k][dest]
                prev[start][dest] = prev[k][dest]


startingPoints = ["Wisc", "Wash", "NJ"]
numNights = 2

meetingCost = [0] * n
for airport in range(n):
    meetingCost[airport] += hotels[airport] * numNights
    for start in startingPoints:
        meetingCost[airport] += best[airports.index(start)][airport]
        meetingCost[airport] += best[airport][airports.index(start)]

def printSpot(prev, src, curr):
    if (src == curr):
        print(curr, end = " ")
        return
    printSpot(prev, src, prev[src][curr])
    print(curr, end = " ")

def printTrip(prev, startingPoints, finalDest):
    for start in startingPoints:
        print("[", end = "")
        printSpot(prev, airports.index(start), prev[airports.index(start)][finalDest])
        print(finalDest, "]", sep = "")

print(best)
print(meetingCost)
print(min(meetingCost))
printTrip(prev, startingPoints, meetingCost.index(min(meetingCost)))
