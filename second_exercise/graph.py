from base_collections.graphs.graph import Graph


class Graph(Graph):
    class Edge(Graph.Edge):
        def set_element(self, element):
            self._element = element

        def add_element(self, x):
            self._element += x

    def get_backward_edge(self, edge):
        target, source = edge.endpoints()
        try:
            backward_edge = self.get_edge(source, target)
        except:
            return None
        return backward_edge

    def insert_vertex(self, x=None):
        return super().insert_vertex(x)

    def incident_valuable_edges(self, v, outgoing=True):
        """Return all (outgoing) edges incident to vertex v in the graph whose value is up to 0.

        If graph is directed, optional parameter used to request incoming edges.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            if edge.element() > 0:
                yield edge

    def update_path_edges(self, edge, bottleneck):
        """
           Given a value and an edge, the method decrements the value of the edge of bottleneck value and if it is 0 the edge is deleted.
           Moreover, the backward edge is created if absent and  its value is set to bottleneck, if not absent, the value is augmented of bottleneck.

           @param edge: the edge whose value has to be decremented
           @param bottleneck: the value
        """
        edge_flow = edge.element() - bottleneck
        backward_edge = self.get_backward_edge(edge)
        v = edge.endpoints()
        if edge_flow != 0:
            edge.set_element(edge_flow)
        else:
            del self._outgoing[v[0]][v[1]]
            del self._incoming[v[1]][v[0]]
            del edge
        if backward_edge is not None:
            backward_edge.add_element(bottleneck)
        else:
            self.insert_edge(v[1], v[0], bottleneck)
