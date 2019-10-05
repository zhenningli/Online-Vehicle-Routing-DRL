# -*- coding: utf-8 -*-
# @Time    : 2019/10/5 13:54
# @Author  : obitolyz
# @FileName: TourGraphCreation.py
# @Software: PyCharm

from math import inf
from itertools import product
from GenetateBigGraph import generate_big_graph
from NodeAndEdge import Road


def single_car_tour_graph(graph):
    """
    :param graph: a list of Node{serial_number, coordinate, type, edges{a list of Road{to, length, time, energy}}}
    :return:
    """
    node_num = len(graph)

    # generate the matrix of distance
    dist = [[inf] * node_num for _ in range(node_num)]
    for node in graph:
        for road in node.edges:
            dist[node.serial_number][road.to] = road.length

    # utilize floyd_warshall algorithm to obtain the shortest distance between any two points
    for k, i, j in product(range(node_num), repeat=3):
        sum_ik_kj = dist[i][k] + dist[k][j]
        if sum_ik_kj > dist[i][j]:
            dist[i][j] = sum_ik_kj

    # re-create the graph for single car
    tour_graph = []
    D = {'Start': ['Pick', 'Depot'],
         'Pick': ['Pick', 'Delivery', 'Depot'],
         'Delivery': ['Pick', 'Delivery', 'Depot', 'Destination'],
         'Depot': ['Pick', 'Delivery', 'Depot', 'Destination'],
         'Destination': []}
    for i, node in enumerate(graph):
        if node.type.name in D.keys():
            node.edges = []
            for j, node_c in enumerate(graph):
                if node_c.type.name in D[node.type.name] and (i != j):
                    length = time = energy = dist[i][j]
                    node.edges.append(Road(j, length, time, energy))
            tour_graph.append(node)

    return tour_graph


if __name__ == '__main__':
    graph, _ = generate_big_graph(node_num=10, lower_bound=1, high_bound=100, request_num=3, depot_num=1)
    single_car_tour_graph(graph)