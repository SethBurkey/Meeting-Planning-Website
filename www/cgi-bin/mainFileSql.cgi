#!/usr/bin/python3
import sqlite3
import sys
import json
import os

#Gets input from the POST request sent to this file
inputData = ''
if int(os.environ.get('CONTENT_LENGTH', 0)) != 0:
    for i in range(int(os.environ.get('CONTENT_LENGTH', 0))):
        inputData += sys.stdin.read(1)
inputData = json.loads(inputData)

#Header for json data
print("Content-type: application/json\n\n")

#Connect to database
connection = sqlite3.connect('../html/API/apiData.db')
cursor = connection.cursor()

#Get hotel data from database
#If there are multiple locations with the same price, it should only return the minimum
cursor.execute("SELECT location, min(price) FROM hotels GROUP BY location;")
hotels = cursor.fetchall()

#Check that there were hotels returned
if len(hotels) == 0:
    print(json.dumps({"error": "Server error"}))
    cursor.close()
    connection.close()
    sys.exit()

#Convert the list of tuples into a dictionary with a format of {city: cost}
tempHotels = {}
try:
    for hotel in hotels:
        tempHotels[hotel[0]] = float(hotel[1])

except ValueError:
    #Print an error if the data from the database was not actually floats
    print(json.dumps({"error": "Server error"}))
    cursor.close()
    connection.close()
    sys.exit()
#Store the dictionary in the list
hotels = tempHotels

#Get flight data from database
#*The id field is currently (2024-03-08) not being used in the code but could be to get path data*
cursor.execute("SELECT origin_location, dest_location, price, id FROM flights;")
data = cursor.fetchall()

#Check that there were flights returned
if len(data) == 0:
    print(json.dumps({"error": "Server error"}))
    cursor.close()
    connection.close()
    sys.exit()
    
#Check to make sure that flight costs were all floats
for i in range(len(data)):
    if not isinstance(data[i][2], float):
        print(json.dumps({"error": "Server error"}))
        cursor.close()
        connection.close()
        sys.exit()

#Get all airports that exist either as source or destination
cursor.execute("SELECT origin_location FROM flights UNION SELECT dest_location FROM flights;")
airports = cursor.fetchall()
n = len(airports)
for i in range(n):
    #Remove the tuple that is currently wrapping around each airport
    airports[i] = airports[i][0]

#Close the connection to the database and cursor
cursor.close()
connection.close()

#Set up all-pairs shortest path algorithm
#*The prev table keeps track of the previous jump to get there and is used to print path
# data, which is currently (2024-03-08) not being used*
best = [[float("inf") for i in range(n)] for j in range(n)]
prev = [[n for i in range(n)] for j in range(n)]
for i in range(n):
    best[i][i] = 0.0
    prev[i][i] = i

#Set up the table with the cheapest flight from any place to any other place
#*The code currently assumes each trip is a round trip and able to go each direction in any order*
for datum in data:
    if best[airports.index(datum[0])][airports.index(datum[1])] > datum[2]:
        best[airports.index(datum[0])][airports.index(datum[1])] = datum[2]
        prev[airports.index(datum[0])][airports.index(datum[1])] = airports.index(datum[0])
    if best[airports.index(datum[1])][airports.index(datum[0])] > datum[2]:
        best[airports.index(datum[1])][airports.index(datum[0])] = datum[2]
        prev[airports.index(datum[1])][airports.index(datum[0])] = airports.index(datum[1])

#Run all-pairs shortest path algorithm using Floyd Warshall Algorithm
for k in range(n):
    for start in range(n):
        for dest in range(n):
            if best[start][k] + best[k][dest] < best[start][dest]:
                best[start][dest] = best[start][k] + best[k][dest]
                prev[start][dest] = prev[k][dest]

#Check input data to make sure data exists and types are correct
if "startCity" not in inputData:
    print(json.dumps({"error": "No starting cities given."}))
    sys.exit()
elif not isinstance(inputData["startCity"], list):
    print(json.dumps({"error": "Starting cities have bad format."}))
    sys.exit()
if "duration" not in inputData:
    print(json.dumps({"error": "No duration given."}))
    sys.exit()
elif not inputData["duration"].isdigit():
    print(json.dumps({"error": "Duration has bad format."}))
    sys.exit()

#Set input data
startingPoints = inputData["startCity"]
numNights = int(inputData["duration"])
numPoints = len(startingPoints)

#Make sure all input are real airports
for point in startingPoints:
    if point not in airports:
        print(json.dumps({"error": "Airport given not from list of flight data."}))
        sys.exit()

#Calculate cost of each airport
meetingCost = {}
for airport in airports:
    #Do not let the algorithm give data where hotels don't exist
    if airport not in hotels:
        meetingCost[airport] = float("inf")
        continue
    
    #Assuming each person gets their own room, calculate cost of rooms
    meetingCost[airport] = hotels[airport] * numNights * numPoints

    #Add cost of airfare for each city flown from
    for start in startingPoints:
        meetingCost[airport] += best[airports.index(start)][airports.index(airport)]

#Get only the top five airports to go to
bestCosts = sorted(meetingCost.values())[:5]
bestPairs = {}
for cost in bestCosts:
    #Don't let inifity be sent and displayed
    if cost == float('inf'):
        continue

    bestPairs[list(meetingCost.keys())
      [list(meetingCost.values()).index(cost)]] = round(cost, 2)
    
#Make sure all of the cities have a connection possible
if len(bestPairs) == 0:
    print(json.dumps({"error": "No connection can be found between all given cities."}))
    sys.exit()

#Send the data
print(json.dumps(bestPairs))
