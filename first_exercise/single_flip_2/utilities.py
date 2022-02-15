from random import random
from first_exercise.single_flip_2.graph import Graph


def initialize_graph_single_flip_2(voters, enemy_relationship):
    graph = Graph()
    current_cut = 0
    vertices = {}
    for v in voters:
        vertices[v] = graph.insert_vertex(v, random() < 0.5)

    for key, value in enemy_relationship.items():
        v1 = vertices[key[0]]
        v2 = vertices[key[1]]
        graph.insert_edge(v1, v2, value)
        if v1.get_partition() != v2.get_partition():
            current_cut += value
    return graph, current_cut


def vertex_cost_difference(graph, vertex):
    incoming_cost = 0
    outgoing_cost = 0
    for edge in graph.incident_edges(vertex):
        opposite_vertex = edge.opposite(vertex)
        if opposite_vertex.get_partition() == vertex.get_partition():
            incoming_cost += edge.element()
        else:
            outgoing_cost += edge.element()
    return incoming_cost - outgoing_cost











