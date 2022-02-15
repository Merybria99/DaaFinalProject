import random
from first_exercise.more_implementations.kl.graph import Graph


def KL_neighbourhood(graph, k=3):
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

            gain = get_gain(graph, vertices, vertices_1)
            if gain > max_gain[0]:
                max_gain = [gain, vertices, vertices_1]

    if max_gain[1] is not None:
        max_gain[1].lock()

    if max_gain[2] is not None:
        max_gain[2].lock()

    return max_gain[0] + local_max_gain


def initialize_graph(voters, enemy_relationship):
    graph = Graph(False)
    actual_cut = 0
    vertices = {}

    for voter in voters:
        vertices[voter] = graph.insert_vertex(voter)
    initialize_random_partition(graph)
    for key, value in enemy_relationship.items():
        v1 = vertices[key[0]]
        v2 = vertices[key[1]]
        graph.insert_edge(v1, v2, value)
        if v1.partition() != v2.partition():
            actual_cut += value

    return graph, actual_cut


def initialize_random_partition(graph):
    vertices_list = list(graph.vertices())
    random.shuffle(vertices_list)
    for i, vertex in enumerate(vertices_list):
        if i % 2 == 0:
            vertex.invert_partition()


def get_vertex_cost_difference(graph, vertex):
    in_cost = 0
    out_cost = 0
    for edge in graph.incident_edges(vertex):
        opposite_vertex = edge.opposite(vertex)
        if (opposite_vertex.partition() == vertex.partition()) ^ opposite_vertex.is_locked():
            in_cost += edge.element()
        else:
            out_cost += edge.element()
    return (-1) * (out_cost - in_cost)


def get_gain(graph, vertexA, vertexB):
    edgeAB = graph.get_edge(vertexA, vertexB)
    return get_vertex_cost_difference(graph, vertexA) + get_vertex_cost_difference(graph, vertexB) + 2 * (0 if edgeAB is None else edgeAB.element())