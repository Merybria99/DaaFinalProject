def improve_k_flip(graph, k=3):
    vertex_to_flip = [None] * k
    for i in range(k):
        max_cost = 0
        for vertex in graph.vertices():
            if not vertex.is_locked():
                cost = 0
                for incident_edge in graph.incident_edges(vertex):
                    opposite_vertex = incident_edge.opposite(vertex)

                    if opposite_vertex.partition() != vertex.partition() ^ opposite_vertex.is_locked():
                        cost -= incident_edge.element()
                    else:
                        cost += incident_edge.element()
                if cost > max_cost:
                    max_cost = cost
                    if vertex_to_flip[i] is not None:
                        vertex_to_flip[i].lock(False)
                    vertex.lock(True)
                    vertex_to_flip[i] = vertex

    return vertex_to_flip
