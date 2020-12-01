import pandas as pd
import numpy as np

import sys
import math
import random

def storeMunicipalities(fileName):
    return pd.read_csv(fileName, sep= "  ", skiprows=1, header=None, engine='python').values.tolist()

############ IGNORE THIS ############
# def algorithm(data, numberOfCirconscriptions):
#     answer = []
#     k_floor = 0
#     length = (len(data)*len(data[0]))/numberOfCirconscriptions
#     k_ceiling = math.ceil(length)
#     if length %2 != 0:
#         k_floor = math.floor(length)
#     print(k_ceiling)
#     print(data)
#     if not k_floor:
#         while len(answer) < k_ceiling:
#             score = 0       
#             district = []
#             max_score = 100*k_ceiling
#             x_municipality = random.choice(data)
#             x = data.index(x_municipality)
#             municipality = random.choice(x_municipality)
#             y = x_municipality.index(municipality)
#             if not len(district):
#                 district.append((x,y))
#                 score += municipality


#         print(x_municipality)
        

def main(argv):
    data = storeMunicipalities(argv[0])
    numberOfCirconscriptions = argv[1]
    #algorithm(data, int(numberOfCirconscriptions))
    if "-p" in argv:
        print("Solution")
    else:
        print("total number of circonscriptions who votes for the green party")

if __name__=="__main__":
    main(sys.argv[1:])