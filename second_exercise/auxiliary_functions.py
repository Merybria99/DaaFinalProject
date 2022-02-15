from second_exercise.modifiedBFS import modified_BFS
from second_exercise.graph import Graph


def ford_fulkerson(graph, source, target):
    """
        The method applies the ford fulkerson algorithm to the given graph to calculate the max flow in the graph.
        The method calls the method modified_BFS_st_path in order to evaluate if there exists a possible
        st path in the previously modified graph.
        If so, the method updates the weights of the edges in the graph according to the obtained bottleneck value.

        @param graph: the graph where to perform the bottleneck
        @param source: the vertex that represents the source of the flow
        @param target: the vertex that represents the sink of the flow
    """

    st_path, bottleneck = modified_BFS_st_path(graph, source, target)
    while st_path is not None:
        for edge in st_path:
            graph.update_path_edges(edge, bottleneck)
        st_path, bottleneck = modified_BFS_st_path(graph, source, target)


def modified_BFS_st_path(graph, source, target):
    """
        The method provides a modified implementation of the BFS which fits the current problem.
        The BFS runs until the node target is found, then the method rebuilds teh st-path and calculated the bottleneck.

        @param graph: the graph were the st path has to be found
        @param source: the source vertex form which the path begins
        @param target: the target vertex where the path ends

        @returns st_path: the path from the source to the target represented through a list of edges
        @returns bottleneck: the value representative of the st path's bottleneck
    """
    forest = {}
    modified_BFS(graph, source, forest, target)

    bottleneck = float('inf')

    if target not in forest:
        return None, bottleneck

    st_path = []
    vertex = target
    while vertex != source:
        discovery_edge = forest[vertex]
        if discovery_edge.element() < bottleneck:
            bottleneck = discovery_edge.element()
        st_path.append(discovery_edge)
        vertex = discovery_edge.opposite(vertex)

    return st_path, bottleneck


def st_path_finder(graph, source, target):
    """
    The method provides a way to define a st path into a specified graph given its source and its target. The path
    is obtained by storing every visited vertex into a structure and visiting step-by-step all its neighbour
    vertices, until the target is found

        @param graph: the graph were to find the st path
        @param source: the source vertex of the flow
        @param target: the sink vertex in the flow network

        @returns a st path in the graph and the bottleneck associated to it
    """
    queue = [(source, float("inf"), [])]
    visited = set()

    while queue:
        actual_destination, actual_bottleneck, actual_path = queue.pop(0)
        visited.add(actual_destination)

        for edge in graph.incident_edges(actual_destination):
            opposite_vertex = edge.opposite(actual_destination)

            if opposite_vertex == target:
                return actual_path + [edge], min(actual_bottleneck, edge.element())
            else:
                if opposite_vertex not in visited:
                    visited.add(opposite_vertex)
                    queue.append((opposite_vertex, min(edge.element(), actual_bottleneck), actual_path + [edge]))


def initialize_graph_second_exercise(Vertices, Edges):
    """
        The method, given a set of vertices and edges initialises a directed graph where:
            * for each pair of connected vertices there are a backward edge and a forward edge that connect them
            with the same weight;
            * for each vertex it is connected to the super source through an edge that goes from to the super source
            to it, the weight is the likelihood dv specified;
            * for each vertex it is connected to the super target through an edge that goes from it to the super target,
            the weight is the likelihood rv specified;

        @param Vertices: set of vertices in the graph
        @param Edges: set of edges in the graph
        @returns graph: the graph initialized starting from Vertices and Edges

        @returns super_source: the super source vertex
        @returns super_target: the super target vertex
    """
    graph = Graph(True)
    super_source = graph.insert_vertex("S")
    super_target = graph.insert_vertex("T")
    vertices = {}
    vertices_set = set()

    for key, value in Vertices.items():
        vertex = graph.insert_vertex(key)
        vertices[key] = vertex
        vertices_set.add(key)
        if value[0] > 0:
            graph.insert_edge(super_source, vertex, value[0])
        if value[1] > 0:
            graph.insert_edge(vertex, super_target, value[1])

    for key, value in Edges.items():
        v1 = vertices[key[0]]
        v2 = vertices[key[1]]
        graph.insert_edge(v1, v2, value)
        graph.insert_edge(v2, v1, value)

    return graph, super_source, super_target, vertices_set


def get_partition_from_graph(graph, source):
    """
        The method gets a partition from the actual graph which is stored into the set partition.

        @param graph: it is the graph whose edges are updated according to the ford fulkerson algorithm
        @param source: the source node which is the root of the bfs launched on the graph

        @returns the partition which contains the nodes connected to the source
    """
    partition = set()
    level = [source]
    while len(level) > 0:
        next_level = []
        for u in level:
            for e in graph.incident_edges(u):
                v = e.opposite(u)
                if v.element() not in partition and v != source:
                    partition.add(v.element())
                    next_level.append(v)
        level = next_level
    return partition
