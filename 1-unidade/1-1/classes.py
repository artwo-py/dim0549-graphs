class Vertex:
    def __init__(self, id):
        self.id = id
    
    def __str__(self):
        return self.id

class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    
class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)
        print(f"Vértice {vertex} adicionado.")

    def remove_vertex(self, vertex_id):
        for v in self.vertices:
            if v.id == vertex_id:
                self.vertices.remove(v)

        self.edges = [e for e in self.edges if e.v1.id != vertex_id and e.v2.id != vertex_id]

    def add_edge(self, v1, v2):
        for e in self.edges:
            if {e.v1, e.v2} == {v1, v2}:
                return "Aresta já existe"
            
        edge = Edge(v1, v2)
        self.edges.append(edge)

    def remove_edge(self, v1, v2):
        self.edges = [e for e in self.edges if {e.v1, e.v2} != {v1, v2}]
    
    def get_edges(self):
        return [(edge.v1.id, edge.v2.id) for edge in self.edges]
    
    def get_vertices(self):
        return [vertex.id for vertex in self.vertices]

class AdjacencyList():
    def __init__(self, vertex):
        self.vertex = vertex
        self.adjacencies = []
    
    def __str__(self):
        return self.vertex