from random import random
from first_exercise.more_implementations.kl.graph import Graph


def improve(graph, actual_cut):
    for vertex in graph.vertices():
        gain = 0
        for incident_edge in graph.incident_edges(vertex):
            opposite_vertex = incident_edge.opposite(vertex)
            if opposite_vertex.partition() != vertex.partition():
                gain -= incident_edge.element()
            else:
                gain += incident_edge.element()
        if gain > 0:
            return vertex, actual_cut + gain
    return None, actual_cut


def initialize_graph_single_flip(voters, enemy_relationship):
    graph = Graph(False)
    actual_cut = 0
    vertices = {}
    for voter in voters:
        vertex = graph.insert_vertex(voter)
        vertices[voter] = vertex
        if random() < 0.5:
            vertex.invert_partition()

    for key, value in enemy_relationship.items():
        v1 = vertices[key[0]]
        v2 = vertices[key[1]]
        graph.insert_edge(v1, v2, value)
        if v1.partition() != v2.partition():
            actual_cut += value
    return graph, actual_cut
