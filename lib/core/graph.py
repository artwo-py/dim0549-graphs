"""
Módulo:    Grafo, Vértices, Arestas+
Descriçao: Define as classes para a representação e manipulação de grafos. Serve como a base para as outras 
           operações do projeto, como algoritmos de busca, análise e renderização.
           
Classes:   - Vertice: Representa um único nó do grafo.
           - Aresta: Representa a conexão entre dois vértices.
           - Grafo: Classe principal que gerencia o grafo e suas operações.
           
Funções:   A classe Grafo inclui métodos para manipulação (adicionar vértice/
           aresta), consulta (obter número de vértices/arestas) e
           sincronização das estruturas de dados internas.
"""
import collections

from lib.algorithms.bfs import bfs

class Vertice:
    """Info: Representa um vértice (ou nó) em um grafo."""
    def __init__(self, id):
        self.id = id
    
    def __str__(self):
        return str(self.id)

class Aresta:
    """Info: Representa uma aresta (ou arco) que conecta dois vértices."""
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
    
    def __str__(self):
        return f"({self.v1},{self.v2})"

class Grafo:
    def __init__(self, direcionado=False, nome_arquivo=""):
        """
        Info: Representa um grafo, gerenciando suas estruturas de dados e operações.
        E: direcionado (bool), nome_arquivo (str)
        S: None
        """
        self.vertices = []
        self.arestas = []
        self.indice_vertices = {} 
        self.direcionado = direcionado
        self.nome_arquivo = nome_arquivo
        self.lista_adj = collections.defaultdict(list)
        self.matriz_adj = []

    def adicionar_vertice(self, id):
        """
        Tarefa: (9) Inclusão de um novo vértice.
        Info: Adiciona um novo vértice ao grafo se ele ainda não existir,
              atualizando todas as estruturas de dados internas.
        E: id (str/int) - Identificador único do vértice.
        S: Vertice - O objeto Vertice criado ou já existente.
        """
        if id not in self.indice_vertices:
            v = Vertice(id)
            self.vertices.append(v)
            self.indice_vertices[id] = v
            
            self.lista_adj[v] = []

            for linha in self.matriz_adj:
                linha.append(0)
            nova_linha = [0] * len(self.vertices)
            self.matriz_adj.append(nova_linha)

        return self.indice_vertices[id]
    
    def adicionar_aresta(self, v1_id, v2_id):
        """
        Tarefa: (1), (2), (16) Criação do Grafo a partir de arestas.
        Info: Adiciona uma aresta entre dois vértices existentes, atualizando
              a lista de arestas, a lista e a matriz de adjacência.
        E: v1_id, v2_id (str/int) - IDs dos vértices a serem conectados.
        S: None.
        """
        v1 = self.indice_vertices.get(str(v1_id))
        v2 = self.indice_vertices.get(str(v2_id))

        if not v1 or not v2:
            print(f"Alerta: Vértice não encontrado ao criar aresta ({v1_id}, {v2_id}).")
            return
        
        for a in self.arestas:
            if not self.direcionado:
                if (a.v1 == v1 and a.v2 == v2) or (a.v1 == v2 and a.v2 == v1): return
            else:
                if a.v1 == v1 and a.v2 == v2: return
            
        aresta = Aresta(v1, v2)
        self.arestas.append(aresta)

        self.lista_adj[v1].append(v2)
        if not self.direcionado:
            self.lista_adj[v2].append(v1)

        idx1 = self.vertices.index(v1)
        idx2 = self.vertices.index(v2)
        self.matriz_adj[idx1][idx2] = 1
        if not self.direcionado:
            self.matriz_adj[idx2][idx1] = 1

    def get_vertices(self):
        """
        Info: Retorna a lista de todos os objetos Vertice do grafo.
        E: None.
        S: list[Vertice] - A lista de vértices.
        """
        return self.vertices
    
    def get_arestas(self):
        """
        Info: Retorna a lista de todos os objetos Aresta do grafo.
        E: None.
        S: list[Aresta] - A lista de arestas.
        """
        return self.arestas

    def num_vertices(self):
        """
        Tarefa: (7) Função que determina o número total de vértices.
        Info: Calcula e retorna o número total de vértices no grafo.
        E: None.
        S: int - O número total de vértices.
        """
        return len(self.vertices)

    def num_arestas(self):
        """
        Tarefa: (8) Função que determina o número total de arestas.
        Info: Calcula e retorna o número total de arestas no grafo.
        E: None.
        S: int - O número total de arestas.
        """
        return len(self.arestas)

    def reconstruir_lista_pelas_arestas(self):
        """
        Tarefa: (4) Conversão entre Matriz e Lista de Adjacências.
        Info: (Função de utilidade) Limpa e recria a lista de adjacências
              baseando-se na lista de arestas atual.
        E: None.
        S: None.
        """
        nova_lista_adj = collections.defaultdict(list)
        for v in self.vertices:
            nova_lista_adj[v]
            
        for aresta in self.arestas:
            nova_lista_adj[aresta.v1].append(aresta.v2)
            if not self.direcionado:
                nova_lista_adj[aresta.v2].append(aresta.v1)
        
        self.lista_adj = nova_lista_adj
        print("Lista de adjacências reconstruída a partir das arestas.")

    def sincronizar_matriz_pela_lista(self):
        """
        Tarefa: (4) Conversão entre Matriz e Lista de Adjacências.
        Info: (Função de utilidade) Sincroniza o conteúdo da matriz de
              adjacências para refletir o estado atual da lista.
        E: None.
        S: None.
        """
        n = self.num_vertices()
        indice = {v: i for i, v in enumerate(self.vertices)}
        
        nova_matriz = [[0] * n for _ in range(n)]
        
        for vertice, vizinhos in self.lista_adj.items():
            i = indice[vertice]
            for vizinho in vizinhos:
                j = indice[vizinho]
                nova_matriz[i][j] = 1

        self.matriz_adj = nova_matriz
        print("Matriz de adjacências sincronizada a partir da lista.")

    def sincronizar_lista_pela_matriz(self):
        """
        Tarefa: (4) Conversão entre Matriz e Lista de Adjacências.
        Info: (Função de utilidade) Sincroniza o conteúdo da lista de
              adjacências para refletir o estado atual da matriz.
        E: None.
        S: None.
        """
        nova_lista_adj = collections.defaultdict(list)
        ordem = self.num_vertices()

        for i in range(ordem):
            vertice_i = self.vertices[i]
            nova_lista_adj[vertice_i]
            
            for j in range(ordem):
                if self.matriz_adj[i][j] == 1:
                    vertice_j = self.vertices[j]
                    nova_lista_adj[vertice_i].append(vertice_j)
        
        self.lista_adj = nova_lista_adj
        print("Lista de adjacências sincronizada a partir da matriz.")

    def imprimir_lista_adj(self):
        """
        Info: (Função de depuração) Imprime a lista de adjacências
              no console de forma legível.
        E: None.
        S: None.
        """
        print("\n--- Lista de Adjacências ---")
        if not self.lista_adj:
            print("Vazia.")
            return
        for vertice, vizinhos in self.lista_adj.items():
            vizinhos_ids = [v.id for v in vizinhos]
            print(f"{vertice.id}: {vizinhos_ids}")

    def imprimir_matriz_adj(self):
        """
        Info: (Função de depuração) Imprime a matriz de adjacências
              no console de forma legível.
        E: None.
        S: None.
        """
        print("\n--- Matriz de Adjacências ---")
        if not self.matriz_adj:
            print("Vazia.")
            return
        
        ids = [v.id for v in self.vertices]
        header = "  " + " ".join(map(str, ids))
        print(header)
        print("-" * len(header))

        for i, linha in enumerate(self.matriz_adj):
            print(f"{ids[i]}|", *linha)

    def eh_conexo(self):
        """
        Info: Para grafos não-direcionados, verifica se há um único componente conexo
            (grafo conexo) utilizando a ordem de visita retornada pela BFS. 
            Para grafos direcionados, verifica se o grafo subjacente não-direcionado 
            é conexo (conectividade fraca).
        E: None
        S: bool - True se o grafo for conexo (ou fraca conectividade para dígrafos), False caso contrário.
        """
        if self.num_vertices() <= 1: 
            return True

        ordem_visita, _ = bfs(self)

        num_componentes = 0
        for _, pai_id in ordem_visita:
            if pai_id == '-':
                num_componentes += 1
                
        if num_componentes == 1:
            return True
        else:
            return False