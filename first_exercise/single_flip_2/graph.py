from base_collections.graphs.graph import Graph


class Graph(Graph):
    class Vertex(Graph.Vertex):
        __slots__ = Graph.Vertex.__slots__, '_partition'

        def __init__(self, x, partition=False):
            super().__init__(x)
            self._partition = partition

        def get_partition(self):
            return self._partition

    __slots__ =  '_first_partition', '_second_partition'

    def __init__(self):
        super().__init__(directed=False)
        self._first_partition = set()
        self._second_partition = set()

    def insert_vertex(self, x=None, partition=False):
        vertex = self.Vertex(x, partition)
        if not vertex._partition:
            self._first_partition.add(vertex.element())
        else:
            self._second_partition.add(vertex.element())
        self._outgoing[vertex] = {}
        return vertex

    def invert_vertex_partition(self,v):
        if not v._partition:
            self._first_partition.remove(v.element())
            self._second_partition.add(v.element())
        else:
            self._second_partition.remove(v.element())
            self._first_partition.add(v.element())
        v._partition = not v._partition

    @property
    def first_partition(self):
        return self._first_partition

    @property
    def second_partition(self):
        return self._second_partition
