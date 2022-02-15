import random

from first_exercise.more_implementations.kl.graph import Graph


def improve_swap(graph):
    gain = 0
    for vertex in graph.vertices():
        for edge in graph.incident_edges(vertex):
            opposite = edge.opposite(vertex)
            if vertex.partition() != opposite.partition():
                gain = _get_gain(graph, vertex, opposite, edge)
                if gain > 0:
                    return vertex, opposite, gain
    return None, None, 0


def _get_gain(graph, vertexA, vertexB, edgeAB):
    cost_differenceA = _vertex_cost_difference(graph, vertexA)
    cost_differenceB = _vertex_cost_difference(graph, vertexB)

    return cost_differenceA + cost_differenceB + 2 * edgeAB.element()


def _vertex_cost_difference(graph, vertex):
    in_cost = 0
    out_cost = 0
    for edge in graph.incident_edges(vertex):
        opposite_vertex = edge.opposite(vertex)
        if opposite_vertex.partition() == vertex.partition():
            in_cost += edge.element()
        else:
            out_cost += edge.element()
    return in_cost - out_cost


def improve(graph, actual_cut):
    for vertex in graph.vertices():
        costo = 0
        for incident_edge in graph.incident_edges(vertex):
            opposite_vertex = incident_edge.opposite(vertex)
            if opposite_vertex.partition() != vertex.partition():
                costo -= incident_edge.element()
            else:
                costo += incident_edge.element()
        if costo > 0:
            return vertex, actual_cut + costo
    return None, actual_cut


def _KL_neighbourhood(graph, k=3):
    max_gain = [-float('inf'), set()]
    local_max_gain = 0
    for _ in range(k):
        local_max_gain = _KL_single_neighbourhood(graph, local_max_gain)
        if local_max_gain > max_gain[0]:
            max_gain[0] = local_max_gain
            for vertex in graph.locked_vertex_iterator():
                max_gain[1].add(vertex)
    return max_gain


def _KL_single_neighbourhood(graph, local_max_gain):
    max_gain = [-float('inf'), None, None]

    for vertices in graph.partition_iterator(True):
        for vertices_1 in graph.partition_iterator(False):

            gain = _get_gain(graph, vertices, vertices_1)
            if gain > max_gain[0]:
                max_gain = [gain, vertices, vertices_1]

    if max_gain[1] is not None:
        max_gain[1].lock()

    if max_gain[2] is not None:
        max_gain[2].lock()

    return max_gain[0] + local_max_gain


def _inizialize_graph(voters, enemy_relationship):
    graph = Graph(False)
    actual_cut = 0
    vertices = {}

    for voter in voters:
        vertices[voter] = graph.insert_vertex(voter)
    _inizialize_random_partition(graph)
    for key, value in enemy_relationship.items():
        v1 = vertices[key[0]]
        v2 = vertices[key[1]]
        graph.insert_edge(v1, v2, value)
        if v1.partition() != v2.partition():
            actual_cut += value

    return graph, actual_cut


def _inizialize_random_partition(graph):
    vertices_list = list(graph.vertices())
    random.shuffle(vertices_list)
    for i, vertex in enumerate(vertices_list):
        if i % 2 == 0:
            vertex.invert_partition()
