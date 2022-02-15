import time

from first_exercise.more_implementations.d2greedy.utilities import _initialize_graph_and_vertices, calculate_gain
from first_exercise.more_implementations.k_flip.utilities import improve_k_flip
from first_exercise.more_implementations.kl.utilities import initialize_graph, KL_neighbourhood
from first_exercise.more_implementations.single_flip.utilities import improve, initialize_graph_single_flip
from first_exercise.more_implementations.single_swap.utilities import improve_swap

def facebook_enmy_KL(V, E):
    graph, max_cut = initialize_graph(V, E)
    cut_increment = KL_neighbourhood(graph)
    A = set()
    B = set()
    timeout = time.time() + 60 * 5
    while cut_increment[0] > 0 and time.time() < timeout:
        max_cut += cut_increment[0]

        for vertex in cut_increment[1]:
            vertex.invert_partition()

        for vertex in graph.vertices():
            vertex.lock(False)
        cut_increment = KL_neighbourhood(graph)

    for vertex in graph.vertices():
        if vertex.partition():
            A.add(vertex.element())
        else:
            B.add(vertex.element())

    return A, B


def facebook_enmy_single_flip(V, E):
    graph, actual_cut = initialize_graph_single_flip(V, E)
    A = set()
    B = set()
    vertex, max_cut = improve(graph, actual_cut)

    while vertex is not None:
        vertex.invert_partition()
        vertex, max_cut = improve(graph, max_cut)

    for vertex in graph.vertices():
        if vertex.partition():
            A.add(vertex)
        else:
            B.add(vertex)

    return A, B


def facebook_enmy_single_swap(V, E):
    graph, actual_cut = initialize_graph_single_flip(V, E)
    A = set()
    B = set()
    vertex, opposite, gain = improve_swap(graph)

    while vertex is not None:
        vertex.invert_partition()
        opposite.invert_partition()
        vertex, opposite, gain = improve_swap(graph)

    for vertex in graph.vertices():
        if vertex.partition():
            A.add(vertex)
        else:
            B.add(vertex)

    return A, B


def facebook_enmy_2dgreedy(V, E):
    graph, vertices = _initialize_graph_and_vertices(V, E)
    Democrats = []
    Republicans = V.copy()

    for voter in V:
        Democrats.append(voter)
        democrats_gain_1 = calculate_gain(Democrats, set(V) - set(Democrats), graph, vertices)
        Democrats.pop()
        democrats_gain_2 = calculate_gain(Democrats, set(V) - set(Democrats), graph, vertices)
        Republicans.remove(voter)
        republicans_gain_1 = calculate_gain(Republicans, set(V) - set(Republicans), graph, vertices)
        Republicans.add(voter)
        republicans_gain_2 = calculate_gain(Republicans, set(V) - set(Republicans), graph, vertices)

        if democrats_gain_1 - democrats_gain_2 >= republicans_gain_1 - republicans_gain_2:
            Democrats.append(voter)
        else:
            Republicans.remove(voter)
    return set(Democrats), set(V) - set(Democrats)


def facebook_enmy_k_flip(V, E):
    graph, actual_cut = initialize_graph_single_flip(V, E)
    A = set()
    B = set()
    vertex_to_flip = improve_k_flip(graph)
    while vertex_to_flip[0] is not None:
        for vertex in vertex_to_flip:
            if vertex is not None:
                vertex.invert_partition()
                vertex.lock(False)
        vertex_to_flip = improve_k_flip(graph)

    for vertex in graph.vertices():
        if vertex.partition():
            A.add(vertex)
        else:
            B.add(vertex)

    return A, B