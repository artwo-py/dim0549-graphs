class Vertice:
    def __init__(self, id):
        self.id = id
    
    def __str__(self):
        return self.id

class Aresta:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    
    def __str__(self):
        return f"({self.v1},{self.v2})"

class Grafo:
    def __init__(self, direcionado = False, nome_arquivo=""):
        self.vertices = []
        self.arestas = []
        self.indice_vertices = {}
        self.direcionado = direcionado
        self.nome_arquivo = nome_arquivo

    def adicionar_vertice(self, id):
        if id not in self.indice_vertices:
            v = Vertice(id)
            self.vertices.append(v)
            self.indice_vertices[id] = v
    
    def get_vertices(self):
        return self.vertices

    def adicionar_aresta(self, v1, v2, direcionado=False):
        for a in self.arestas:
            if not direcionado:
                if {a.v1, a.v2} == {v1, v2}:
                    return "Aresta já existe"
            else:
                if a.v1 == v1 and a.v2 == v2:
                    return "Aresta já existe"
            
        aresta = Aresta(v1, v2)
        self.arestas.append(aresta)
    
    def get_arestas(self):
        return self.arestas

