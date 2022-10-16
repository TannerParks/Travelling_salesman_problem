# Tanner Parks
# CS325

import sys
import math
import numpy as np
import timeit

"""Have a good break!"""

class Edge:
    def __init__(self, edge: list, distance: int):
        self.edge = edge
        self.dist = distance


def getData(dataFile):
    """Turns the data from the file into a list of lists."""
    dataList = []

    with open(dataFile, "r") as file:
        fileData = file.read().splitlines()
        for item in fileData:
            data = item.split()
            dataList.append([int(item) for item in data])  # Turns data into a list of integers

    return dataList


def adjacencyMatrix(coords: list):
    """Makes an adjacency matrix of the coordinates."""
    # print(coords)
    edges = []  # List of edges and their weights
    matrix = [[0 for column in coords] for row in coords]  # Makes matrix of correct size for weights to be added to
    for i, coord in enumerate(coords):  # for index, coordinate in list of coordinates
        for j in range(i + 1, len(coords)):
            edges.append(Edge([coords[i], coords[j]], round(math.dist(coords[i], coords[j]))))
    for edge in edges:
        # Puts the weights in the matrix on both ends so if (0,1)-(1,0) has a weight of 4 it puts 4 at those indexes
        matrix[coords.index(edge.edge[0])][coords.index(edge.edge[1])] = edge.dist
        matrix[coords.index(edge.edge[1])][coords.index(edge.edge[0])] = edge.dist
    return matrix


def check_unvisited_node(unvisited):
    """How we keep track of where we've been to."""
    for u in unvisited:
        if u == 1:
            return True
    return False


def toFile(node_no, travel_route, min_distance, outFile):
    """Outputs everything to a file."""
    fastestRoute = travel_route[0]
    totalCost = min_distance[0]
    for start_node in range(0, node_no):
        if min_distance[start_node] < totalCost:
            totalCost = min_distance[start_node]
            fastestRoute = travel_route[start_node]

    with open(outFile + ".tour", "w+") as file:
        file.write(str(totalCost) + "\n")
        for route in fastestRoute:
            file.write(str(route) + "\n")

    print("min distance is: " + str(totalCost))
    print(f"travel route is: {fastestRoute}")

    return totalCost, fastestRoute


# This function isn't all mine. I had most the pieces but I couldn't figure out how to put it together by myself so
# I asked friends, reddit, discord, etc for help!
def nearestNeighbor(matrix, outFile):
    """Nearest Neighbor algorithm picks the least expensive edge and goes to it as long as it doesn't complete the circuit
    without going to all vertices."""
    matrixLength = len(matrix)

    min_distance = np.zeros(matrixLength)  # distances with starting node as min_distance[i]
    alt = 0

    map = [[0 for x in range(0, matrixLength)] for y in range(0, matrixLength)]

    for start in range(0, matrixLength):

        unvisited = np.ones((matrixLength,), dtype=int)  # How we keep track of where we've been
        unvisited[start] = 0    # Set first node to visited
        map[start][0] = start  # starting point

        node = start
        count = 1
        while count < matrixLength:
            check_unvisited_node(unvisited)


            closeEdge = math.inf
            closeNode = matrixLength

            for node2 in range(0, matrixLength):
                if unvisited[node2] == 1 and 0 < matrix[node][node2] < closeEdge:
                    closeEdge = matrix[node][node2]
                    closeNode = node2

            node = closeNode
            unvisited[node] = 0
            min_distance[start] = min_distance[start] + closeEdge

            map[start][count] = node
            count = count + 1

        if not math.isinf(min_distance[start]):
            last_visited = map[start][matrixLength-1]
            if matrix[last_visited][start] > 0:
                min_distance[start] = min_distance[start] + matrix[last_visited][start]
            else:
                min_distance[start] = math.inf

    [shortest_min_distance, shortest_travel_route] = toFile(matrixLength, map, min_distance, outFile)

    return shortest_min_distance, shortest_travel_route


def main(inFile, outFile):
    data = getData(inFile)
    numCities = data[0][0]
    cities = data[1:]
    for i in cities:
        i.pop(0)
    matrix = adjacencyMatrix(cities)
    nearestNeighbor(matrix, outFile)



if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])