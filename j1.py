# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 10:47:09 2024

@author: INTENT Lab
"""


import sys


class Graph:
    nodes = {}
    matrix = []

    def __init__(self, graph_dict):
        temp_dict = {}
        for i in range(len(graph_dict['nodes'])):
            self.nodes[i] = graph_dict['nodes'][i]
            temp_dict[graph_dict['nodes'][i]] = i

        self.matrix = [[0 for x in graph_dict['nodes']] for y in graph_dict['nodes']]
        for i in graph_dict['edges']:
            self.matrix[temp_dict.get(i[0])][temp_dict.get(i[1])] = i[2]
            self.matrix[temp_dict.get(i[1])][temp_dict.get(i[0])] = i[2]

    def getSize(self):
        return len(self.matrix)

    def getWeight(self, node1, node2):
        return self.matrix[node1][node2]

    def getNodeLabel(self, node):
        return self.nodes.get(node)


def createGraph():
   f= {
	"nodes": ["A", "B", "C", "D", "E", "F", "G", "H"], 

	"edges": [
				["A", "F", 120],
				["B", "C", 80],
				["C", "H", 30],
				["D", "B", 300],
				["E", "D", 100],
				["F", "C", 100],
				["G", "A", 100],
				["H", "A", 100]	
			]

      }
   #graph_dic = json.loads(f)

   return Graph(f)


def sumWeights(graph, internalSet, node):
    weights = 0
    for i in internalSet:
        weights += graph.getWeight(node, i)
    return weights


def reduction(graph, internal, external, node):
    return sumWeights(graph, external, node) - sumWeights(graph, internal, node)


def computeD(graph, A, B):
    D = {}
    for i in A:
        D[i] = reduction(graph, A, B, i)
    for i in B:
        D[i] = reduction(graph, B, A, i)
    return D


def maxSwitchCostNodes(graph, A, B, D):
    maxCost = -sys.maxsize - 1
    a = None
    b = None
    for i in A:
        for j in B:
            cost = D[i] + D[j] - 2 * graph.getWeight(i, j)
            if cost > maxCost:
                maxCost = cost
                a = i
                b = j

    return a, b, maxCost


def updateD(graph, A, B, D, a, b):
    for i in A:
        D[i] = D[i] + 2*(graph.getWeight(i, a) - graph.getWeight(i, b))
    for i in B:
        D[i] = D[i] + 2*(graph.getWeight(i, b) - graph.getWeight(i, a))
    return D


def getMaxCostAndIndex(costs):
    maxCost = -sys.maxsize - 1
    index = 0
    sum = 0

    for i in costs:
        sum += i
        print(maxCost)
        if sum > maxCost:
            maxCost = sum
            index = costs.index(i)

    return maxCost, index


def switch(graph, A, B):
    D = computeD(graph, A, B)
    print(D)
    costs = []
    X = []
    Y = []

    for i in range(int(graph.getSize()/ 2)):
        x, y, cost = maxSwitchCostNodes(graph, A, B, D)
        A.remove(x)
        B.remove(y)
        print(x,y,cost)
        costs.append(cost)
        X.append(x)
        Y.append(y)

        D = updateD(graph, A, B, D, x, y)

    maxCost, k = getMaxCostAndIndex(costs)
    print(maxCost,k,X,Y)
    if maxCost > 0:
        A = Y[:k + 1] + X[k + 1:]
        B = X[:k + 1] + Y[k + 1:]
        return A, B, False
    else:
        A = [i for i in X]
        B = [i for i in Y]
        return A, B, True


def k_lin():
    graph = createGraph()
    A = [i for i in range(int(graph.getSize() / 2))]
    B = [i for i in range(int(graph.getSize() / 2), graph.getSize())]
    done = False

    while not done:
        A, B, done = switch(graph, A, B)

    print ("Partition A: "),
    for i in A:
        print(graph.getNodeLabel(i)),
    print ("\nPartition B: "),
    for i in B:
        print(graph.getNodeLabel(i)),


def main():
    k_lin()


if __name__ == '__main__':
    main()