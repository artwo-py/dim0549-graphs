from .quicksort import quicksort

class Vertex:
    def __init__(self, id):
        self.id = id
    
    def __str__(self):
        return self.id

class Edge:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    
    def __str__(self):
        return f"({self.v1},{self.v2})"

class Graph:
    def __init__(self, directed = False, file_name=""):
        self.vertices = []
        self.edges = []
        self.vertex_index = {}
        self.directed = directed
        self.file_name = file_name

    def add_vertex(self, id):
        if id not in self.vertex_index:
            v = Vertex(id)
            self.vertices.append(v)
            self.vertex_index[id] = v
    
    def get_vertices(self):
        return self.vertices

    def add_edge(self, v1, v2, directed=False):
        for e in self.edges:
            if not directed:
                if {e.v1, e.v2} == {v1, v2}:
                    return "Aresta já existe"
            else:
                if e.v1 == v1 and e.v2 == v2:
                    return "Aresta já existe"
            
        edge = Edge(v1, v2)
        self.edges.append(edge)
    
    def get_edges(self):
        return self.edges
    
class BFS_Tree:
    def __init__(self, vertex):
        self.root = vertex

class BFS_Node:
    def __init__(self, vertex):
        self.vertex = vertex
        self.children = []
