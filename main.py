
import numpy as np

import sys
import math
import random
import itertools
import copy

# def lessFitDistrict(answer):
#     indexDistrict = 0
#     lessFitScore = -1
#     for i, m in enumerate(answer):
#         tempScore = numberWonMun(m)
#         if lessFitScore == -1:
#             lessFitScore = tempScore
#         else:
#             if tempScore < lessFitScore:
#                 lessFitScore = tempScore
#                 indexDistrict = i
#     return indexDistrict

def storeMunicipalities(fileName):
    with open(fileName) as f:
        next(f)
        return np.array([[int(x) for x in row.split()] for row in f])

def manhattanDistance(municipality, district, maxDistance):
    for m in district:
        if municipality[0] == m[1]:
            if abs(municipality[0]- m[1]) + abs(municipality[1] - m[2]) > maxDistance-1:
                return False
        else:
            if abs(municipality[0]- m[1]) + abs(municipality[1] - m[2]) > maxDistance:
                return False
    return True

def numberWonMun(district):
    totalWon = 0
    for s in district:
        if s[0] > 50:
            totalWon += 1
    return totalWon
 
def numberWonDistricts(answer):
    wonDistricts = 0
    for  m in answer:
        if numberWonMun(m) > len(m)/2:
            wonDistricts += 1
    return wonDistricts
            
def scoreWonDistricts(answer):
    wonDistricts = numberWonDistricts(answer)
    score =  (wonDistricts/len(answer))*100
    return score

def initialSolution(data, numberOfCirconscriptions):
    answer = []
    k_floor = 0
    row = len(data)
    column = len(data[0])
    tempNbCeil = 0
    length = (row*column)/numberOfCirconscriptions
    k_ceiling = math.ceil(length)
    maxDistance = math.ceil((row*column)/(2*numberOfCirconscriptions))
    nbOfCeil = (row * column) % numberOfCirconscriptions
    if length %2 != 0:
        k_floor = math.floor(length)
    already_picked = []
    district = []
    k = k_ceiling
    tempLength = 0
    iteration = 0
    first = (0,0,0)
    while len(answer) < numberOfCirconscriptions:
        if iteration > 5:
            lastDistrict = answer.pop()
            for mun in lastDistrict:
                already_picked.remove(mun)
            for mun in district:
                already_picked.remove(mun)
            district = []
            district.append(first)
            already_picked.append(first)
            iteration = 0
        for i, row in enumerate(data):
            for j, municipality in enumerate(row):
                if (municipality,i,j) not in already_picked:
                    first = (municipality,i,j)
                    if not len(district):
                        district.append((municipality,i,j))
                        already_picked.append((municipality,i,j))
                    else:
                        if manhattanDistance((i,j), district, maxDistance):
                            district.append((municipality,i,j))
                            already_picked.append((municipality,i,j))
                        if len(district) == k:
                            answer.append(district)
                            district = []
                            tempNbCeil += 1
                            break
            if len(answer) > tempLength:
                tempLength = len(answer)
                iteration = 0
                if tempNbCeil == nbOfCeil:
                    k = k_floor
                break
        iteration += 1
    return answer, maxDistance

def getNeighbors(answer, maxDistance):
    neighbors = {}
    for i, district1 in enumerate(answer):
        for j, district2 in enumerate(answer):
            if district1 != district2:
                c = list(itertools.product(district1, district2))
                for pair in c:
                    if manhattanDistance(pair[0], district2, maxDistance) and manhattanDistance(pair[1], district1, maxDistance):
                        neighbors[(i, j)] = pair
    return neighbors

def printSolution(solution):
    for districts in solution:
        district_to_print = []
        for municipality in districts:
            district_to_print.append(str(municipality[1]))
            district_to_print.append(str(municipality[2]))
        print(" ".join(district_to_print))

def simulatedAnnealing(data, numberOfCirconscriptions):
    solution, maxDistance = initialSolution(data, numberOfCirconscriptions)
    iteration = 0
    nbOfGreenDistricts = numberWonDistricts(solution)
    temp = 60
    alpha = 0.1
    score = scoreWonDistricts(solution)
    tempSolution = copy.deepcopy(solution)
    while iteration < 10 and nbOfGreenDistricts < numberOfCirconscriptions/2:
        neighbors =  getNeighbors(solution, maxDistance)
        randomNeighbor = random.choice(neighbors)
        diff = score - scoreWonDistricts(randomNeighbor)
        if  diff <= 0:
            solution = randomNeighbor
        else:
            if iteration == 9:
                temp += 10
                iteration = 0
            if random.uniform(0,1) < math.exp(diff/temp):
                solution = randomNeighbor
                iteration = 0
            else:
                iteration += 1
        temp -= alpha
    return solution
        

def main(argv):
    data = storeMunicipalities(argv[0])
    numberOfCirconscriptions = argv[1]
    solution = simulatedAnnealing(data, int(numberOfCirconscriptions))
    if "-p" in argv:
        printSolution(solution)
    else:
        print(scoreWonDistricts(solution))

if __name__=="__main__":
    main(sys.argv[1:])