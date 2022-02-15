# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#    Data Structures and Algorithms in Python
#    Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#    John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

def modified_BFS(graph, source, discovered, target=None):
    """Perform BFS of the undiscovered portion of Graph g starting at Vertex s.

    discovered is a dictionary mapping each vertex to the edge that was used to
    discover it during the BFS (s should be mapped to None prior to the call).
    Newly discovered vertices will be added to the dictionary as a result.
    """

    level = [source]  # first level includes only s
    while len(level) > 0:
        next_level = []  # prepare to gather newly found vertices
        for u in level:
            for e in graph.incident_edges(u):  # for every outgoing edge from u
                v = e.opposite(u)
                if v not in discovered:  # v is an unvisited vertex
                    discovered[v] = e  # e is the tree edge that discovered v
                    next_level.append(v)  # v will be further considered in next pass
                if target == v and target is not None:
                    return
        level = next_level  # relabel 'next' level to become current
    return None
