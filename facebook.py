from first_exercise.single_flip_2.utilities import initialize_graph_single_flip_2, vertex_cost_difference
from second_exercise.auxiliary_functions import initialize_graph_second_exercise, ford_fulkerson, get_partition_from_graph


def facebook_friend(Voters, Edges):
    graph, source, target, vertices = initialize_graph_second_exercise(Voters, Edges)

    ford_fulkerson(graph, source, target)

    first_partition = get_partition_from_graph(graph, source)

    return first_partition, vertices - first_partition


def facebook_enmy(Voters, Edges):
    graph, current_cut = initialize_graph_single_flip_2(Voters, Edges)

    current_gain = float('inf')

    while current_gain > 250:
        current_gain = 0
        for vertex in graph.vertices():
            vertex_gain = vertex_cost_difference(graph, vertex)

            if vertex_gain > 0:
                current_gain += vertex_gain
                graph.invert_vertex_partition(vertex)

    return graph.first_partition, graph.second_partition
