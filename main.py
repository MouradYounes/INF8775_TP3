import pandas as pd
import numpy as np

import sys
import math
import random

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
    print("ceil: ",k_ceiling)
    print("floor: ",k_floor)
    print("nb of ceil: ", nbOfCeil)
    print("max distance: ", maxDistance)
    print(data)
    already_picked = []
    district = []
    k = k_ceiling
    tempLength = 0
    iteration = 0
    first = (0,0,0)
    while len(answer) < numberOfCirconscriptions:
        if iteration > 5:
            lastDistrict = answer.pop()
            print(lastDistrict)
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
                #print(municipality)
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
    print("length of answer: ", len(answer))
    print(answer)
        

def main(argv):
    data = storeMunicipalities(argv[0])
    numberOfCirconscriptions = argv[1]
    initialSolution(data, int(numberOfCirconscriptions))
    if "-p" in argv:
        print("Solution")
    else:
        print("total number of circonscriptions who votes for the green party")

if __name__=="__main__":
    main(sys.argv[1:])