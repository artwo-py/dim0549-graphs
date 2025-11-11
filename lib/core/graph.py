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

class Vertice:
    """Info: Representa um vértice (ou nó) em um grafo."""
    def __init__(self, id):
        self.id = id
    
    def __str__(self):
        return str(self.id)

class Aresta:
    """Info: Representa uma aresta (ou arco) que conecta dois vértices."""
    def __init__(self, v1, v2, peso=None):
        self.v1 = v1
        self.v2 = v2
        self.peso = peso
    
    def __str__(self):
        peso_str = f", peso={self.peso}" if self.peso is not None else ""
        return f"({self.v1},{self.v2}{peso_str})"

class Grafo:
    def __init__(self, direcionado=False, nome_arquivo="", vertices=None):
        """
        Info: Representa um grafo, gerenciando suas estruturas de dados e operações.
        E: direcionado (bool), nome_arquivo (str)
        S: None
        """
        self.direcionado = direcionado
        self.nome_arquivo = nome_arquivo
        self.vertices = list(vertices) if vertices else []
        self.arestas = []
        self.indice_vertices = {} 
        self.lista_adj = collections.defaultdict(list)
        self.matriz_adj = []
        self.matriz_incidencia = []

    # --------------------------------------------------------------------------
    # Interface Pública de Manipulação
    # --------------------------------------------------------------------------
    def adicionar_vertice(self, id):
        """
        Tarefa: (9) Inclusão de um novo vértice.
        Info: Orquestra a adição de um novo vértice ao grafo se ele ainda não existir,
              atualizando todas as estruturas de dados internas.
        E: id (str/int) - Identificador único do vértice.
        S: Vertice - O objeto Vertice criado ou já existente.
        """
        if id in self.indice_vertices:
            return self.indice_vertices[id]

        v = Vertice(id)
        self.vertices.append(v)
        self.indice_vertices[id] = v
        
        self._adicionar_vertice_lista_adj(v)
        self._adicionar_vertice_matriz_adj()
        self._adicionar_vertice_matriz_inc()

        return v
    
    def adicionar_aresta(self, v1_id, v2_id, w=None):
        """
        Tarefa: (1), (2), (16) Criação do Grafo a partir de arestas.
        Info: Orquestra a adição de uma aresta entre dois vértices existentes, atualizando
              a lista de arestas, a lista e a matriz de adjacência.
        E: v1_id, v2_id (str/int) - IDs dos vértices a serem conectados.
        w (int, opcional) - Peso da aresta.
        S: None.
        """
        v1 = self.indice_vertices.get(str(v1_id))
        v2 = self.indice_vertices.get(str(v2_id))

        peso = w

        if not v1 or not v2:
            print(f"Alerta: Vértice não encontrado ao criar aresta ({v1_id}, {v2_id}).")
            return
        
        for a in self.arestas:
            if not self.direcionado:
                if (a.v1 == v1 and a.v2 == v2) or (a.v1 == v2 and a.v2 == v1): return
            else:
                if a.v1 == v1 and a.v2 == v2: return

        nova_aresta = Aresta(v1, v2, peso)
        self.arestas.append(nova_aresta)
        self._adicionar_aresta_lista_adj(v1, v2)
        self._adicionar_aresta_matriz_adj(v1, v2)
        self._adicionar_aresta_matriz_inc(v1, v2)

    def remover_vertice(self, id):
        """
        Info: Orquestra a remoção de um vértice do grafo junto com todas as arestas associadas,
              atualizando todas as estruturas de dados internas.
        E: id (str/int) - Identificador único do vértice a ser removido.
        S: bool - True se o vértice foi removido, False caso contrário.
        """
        vertice_a_remover = self.indice_vertices.get(str(id))
        if not vertice_a_remover:
            print(f"Alerta: Vértice com ID '{id}' não encontrado para remoção.")
            return False

        indice_na_lista = self.vertices.index(vertice_a_remover)
        self.arestas = [a for a in self.arestas if vertice_a_remover not in (a.v1, a.v2)]

        self._remover_vertice_lista_adj(vertice_a_remover)
        self._remover_vertice_matriz_adj(indice_na_lista)
        self._remover_vertice_matriz_inc(indice_na_lista)
        
        del self.indice_vertices[str(id)]
        self.vertices.pop(indice_na_lista)
        
        return True

    # --------------------------------------------------------------------------
    # Métodos Auxiliares Internos
    # --------------------------------------------------------------------------
    def _adicionar_vertice_lista_adj(self, vertice):
        """
        Info: Inicializa a entrada para um novo vértice na lista de adjacência.
        E: vertice (Vertice) - O objeto do vértice a ser adicionado.
        S: None
        """
        self.lista_adj[vertice] = []

    def _adicionar_vertice_matriz_adj(self):
        """
        Info: Expande a matriz de adjacência com uma nova linha e coluna de zeros.
        E: None
        S: None
        """
        for linha in self.matriz_adj:
            linha.append(0)
        nova_linha = [0] * len(self.vertices)
        self.matriz_adj.append(nova_linha)

    def _adicionar_vertice_matriz_inc(self):
        """
        Info: Adiciona uma nova linha de zeros à matriz de incidência para o novo vértice.
        E: None
        S: None
        """
        num_arestas_existentes = self.num_arestas()
        nova_linha = [0] * num_arestas_existentes
        self.matriz_incidencia.append(nova_linha)

    def _adicionar_aresta_lista_adj(self, v1, v2):
        """
        Info: Adiciona a conexão entre dois vértices na lista de adjacência.
        E: v1 (Vertice), v2 (Vertice) - Os objetos dos vértices a serem conectados.
        S: None
        """
        self.lista_adj[v1].append(v2)
        if not self.direcionado:
            self.lista_adj[v2].append(v1)

    def _adicionar_aresta_matriz_adj(self, v1, v2):
        """
        Info: Adiciona a conexão entre dois vértices na matriz de adjacência.
        E: v1 (Vertice), v2 (Vertice) - Os objetos dos vértices para encontrar seus índices.
        S: None
        """
        idx1 = self.vertices.index(v1)
        idx2 = self.vertices.index(v2)
        self.matriz_adj[idx1][idx2] = 1
        if not self.direcionado:
            self.matriz_adj[idx2][idx1] = 1

    def _adicionar_aresta_matriz_inc(self, v1, v2):
        """
        Info: Adiciona uma nova coluna à matriz de incidência para a nova aresta.
        E: v1 (Vertice), v2 (Vertice) - Os vértices que a aresta conecta.
        S: None
        """
        idx1 = self.vertices.index(v1)
        idx2 = self.vertices.index(v2)
        for i, linha in enumerate(self.matriz_incidencia):
            if self.direcionado:
                if i == idx1: linha.append(1)   
                elif i == idx2: linha.append(-1) 
                else: linha.append(0)
            else:
                if i == idx1 or i == idx2: linha.append(1)
                else: linha.append(0)

    def _remover_vertice_lista_adj(self, vertice):
        """
        Info: Remove um vértice e todas as suas menções da lista de adjacência.
        E: vertice (Vertice) - O objeto do vértice a ser removido.
        S: None
        """
        if vertice in self.lista_adj:
            del self.lista_adj[vertice]
        
        for v_qualquer in self.lista_adj:
            self.lista_adj[v_qualquer] = [v for v in self.lista_adj[v_qualquer] if v != vertice]

    def _remover_vertice_matriz_adj(self, indice):
        """
        Info: Remove a linha e a coluna de um vértice da matriz de adjacência.
        E: indice (int) - O índice do vértice a ser removido.
        S: None
        """
        self.matriz_adj.pop(indice)
        for linha in self.matriz_adj:
            linha.pop(indice)

    def _remover_vertice_matriz_inc(self, indice_vertice):
        """
        Info: Remove a linha do vértice e as colunas das arestas associadas.
        E: indice_vertice (int)
        S: None
        """
        self.matriz_incidencia.pop(indice_vertice)
        self.sincronizar_matriz_inc_pelas_arestas()

    # --------------------------------------------------------------------------
    # Consultas e Propriedades
    # --------------------------------------------------------------------------
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

    def get_grau(self, vertice_id):
        """
        Tarefa: (5) Função que calcula o grau de um vértice.
        Info: Para grafos não direcionados, retorna o grau total (int).
              Para grafos direcionados, retorna uma tupla (grau de entrada, grau de saída).
        E: vertice_id (str/int) - O ID do vértice.
        S: int or tuple(int, int) or None - O grau, ou None se o vértice não existir.
        """
        vertice_obj = self.indice_vertices.get(str(vertice_id))
        if not vertice_obj:
            return None

        if not self.direcionado:
            return len(self.lista_adj.get(vertice_obj, []))
        else:
            grau_saida = len(self.lista_adj.get(vertice_obj, []))
            grau_entrada = 0
            for vizinhos in self.lista_adj.values():
                if vertice_obj in vizinhos:
                    grau_entrada += 1
            return (grau_entrada, grau_saida)
