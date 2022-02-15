from base_collections.graphs.graph import Graph


def _initialize_graph_and_vertices(V, E):
    graph = Graph()
    vertices = {}
    for v in V:
        vertices[v] = graph.insert_vertex(v)
    for e in E.keys():
        graph.insert_edge(vertices[e[0]], vertices[e[1]], E.get(e))
    return graph, vertices


def calculate_gain(S, V, graph, vertices):
    gain = 0
    for s in S:
        for v1 in V:
            tmp = graph.get_edge(vertices[s], vertices[v1])
            if tmp is not None:
                gain += tmp.element()
    return gain