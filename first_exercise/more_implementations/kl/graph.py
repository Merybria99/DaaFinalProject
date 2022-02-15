from base_collections.graphs.graph import Graph


class Graph(Graph):
    class Vertex(Graph.Vertex):
        __slots__ = Graph.Vertex.__slots__, '_partition', '_locked'

        def __init__(self, x, partition=True, locked=False):
            super().__init__(x)
            self._partition = partition
            self._locked = locked

        def partition(self):
            return self._partition

        def is_locked(self):
            return self._locked

        def lock(self, value=True):
            self._locked = value

        def invert_partition(self):
            self._partition = not self._partition

    def partition_iterator(self, partition=True):
        for v in self.vertices():
            if v.partition() == partition and not v.is_locked():
                yield v

    def locked_vertex_iterator(self):
        for v in self.vertices():
            if v.is_locked():
                yield v
