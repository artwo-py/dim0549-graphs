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
from math import inf as infinito
from lib.utils.converter import get_decimal
from decimal import Decimal

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
    def __init__(self, direcionado=False, nome_arquivo="", vertices=None, ponderado=False):
        """
        Info: Representa um grafo, gerenciando suas estruturas de dados e operações.
        E: direcionado (bool), nome_arquivo (str)
        S: None
        """
        self.direcionado = direcionado
        self.ponderado = ponderado
        self.nome_arquivo = nome_arquivo
        self.vertices = list(vertices) if vertices else []
        self.arestas = []
        self.indice_vertices = {} 
        self.lista_adj = collections.defaultdict(list)
        self.matriz_adj = []
        self.matriz_incidencia = []
        self.vazio = infinito if self.ponderado else 0

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
        Adiciona ou ATUALIZA uma aresta.
        Se a aresta existir, ela verifica se o novo peso 'w' é menor.
        """
        v1 = self.indice_vertices.get(str(v1_id))
        v2 = self.indice_vertices.get(str(v2_id))
        peso = w

        if not v1 or not v2:
            print(f"Alerta: Vértice não encontrado ao criar aresta ({v1_id}, {v2_id}).")
            return
        
        aresta_existente = None
        for a in self.arestas:
            if self.direcionado:
                if a.v1 == v1 and a.v2 == v2:
                    aresta_existente = a
                    break
            else:
                if (a.v1 == v1 and a.v2 == v2) or (a.v1 == v2 and a.v2 == v1):
                    aresta_existente = a
                    break
        if aresta_existente:
            if peso is not None and peso < aresta_existente.peso:
                print(f"  DEBUG: Atualizando peso de ({v1_id}, {v2_id}). Antigo: {aresta_existente.peso}, Novo: {peso}")
                aresta_existente.peso = peso
                self._adicionar_aresta_matriz_adj(v1, v2, peso)
            else:
                return
        else:
            nova_aresta = Aresta(v1, v2, peso)
            self.arestas.append(nova_aresta)
            self._adicionar_aresta_lista_adj(v1, v2)
            self._adicionar_aresta_matriz_adj(v1, v2, peso)
            self._adicionar_aresta_matriz_inc(v1, v2)

    def remover_aresta(self, v1_id, v2_id):
        v1 = self.indice_vertices.get(str(v1_id))
        v2 = self.indice_vertices.get(str(v2_id))

        if not v1 or not v2:
            print(f"Alerta: Vértice não encontrado ao remover aresta ({v1_id}, {v2_id}).")
            return False

        aresta_remover = None
        for a in self.arestas:
            if not self.direcionado:
                if (a.v1 == v1 and a.v2 == v2) or (a.v1 == v2 and a.v2 == v1):
                    aresta_remover = a
                    break
            else:
                if a.v1 == v1 and a.v2 == v2:
                    aresta_remover = a
                    break

        if not aresta_remover:
            print(f"Alerta: Aresta ({v1_id}, {v2_id}) não encontrada para remoção.")
            return False

        idx_aresta = self.arestas.index(aresta_remover)
        self.arestas.remove(aresta_remover)

        self.lista_adj[v1] = [v for v in self.lista_adj[v1] if v != v2]
        if not self.direcionado:
            self.lista_adj[v2] = [v for v in self.lista_adj[v2] if v != v1]

        i1 = self.vertices.index(v1)
        i2 = self.vertices.index(v2)
        self.matriz_adj[i1][i2] = 0
        if not self.direcionado:
            self.matriz_adj[i2][i1] = 0

        for linha in self.matriz_incidencia:
            linha.pop(idx_aresta)

        return True

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
            linha.append(self.vazio)
        nova_linha = [self.vazio] * len(self.vertices)
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

    def _adicionar_aresta_matriz_adj(self, v1, v2, w=None):
        """
        Info: Adiciona ou ATUALIZA a conexão na matriz de adjacência,
              garantindo que o MENOR peso seja armazenado.
        E: v1 (Vertice), v2 (Vertice) - Os objetos dos vértices para encontrar seus índices.
        S: None
        """
        
        peso = 1 if w is None else w
        idx1 = self.vertices.index(v1)
        idx2 = self.vertices.index(v2)
        
        peso_atual = self.matriz_adj[idx1][idx2]
        
        if peso_atual == self.vazio or peso < peso_atual:
            self.matriz_adj[idx1][idx2] = peso
            if not self.direcionado:
                self.matriz_adj[idx2][idx1] = peso

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
    
    def get_aresta(self, v1_id, v2_id):
        """
        Info: Recupera a aresta indicada pelos vértices, se houver.
        E: v1_id, v2_id (str/int): Id's dos vértices terminais da aresta 
            sendo buscada
        S: aresta (Aresta) ou None
        """

        s1 = str(v1_id)
        s2 = str(v2_id)

        for a in self.arestas:
            a1 = str(a.v1.id)
            a2 = str(a.v2.id)

            if not self.direcionado:
                if (a1 == s1 and a2 == s2) or (a1 == s2 and a2 == s1):
                    return a
            else:
                if a1 == s1 and a2 == s2:
                    return a

        return None
    
    def get_vizinhos(self, vertice_id):
        """
        Info: Retorna um dicionário dos vizinhos de um vértice e seus pesos.
        E: vertice_id (str/int) - O ID do vértice.
        S: dict - Dicionário onde as chaves são os IDs dos vizinhos e os valores são os pesos das arestas.
        """
        vertice_obj = self.indice_vertices.get(str(vertice_id))
        if not vertice_obj:
            return {}

        vizinhos = {}
        for vizinho in self.lista_adj.get(vertice_obj, []):
            aresta = self.get_aresta(vertice_obj.id, vizinho.id)
            peso = aresta.peso if aresta and aresta.peso is not None else 1
            vizinhos[vizinho.id] = peso

        return vizinhos
    
    def get_peso(self, v1_id, v2_id):
        """
        Info: Retorna o peso da aresta entre dois vértices, ou infinito se não houver conexão.
        E: v1_id, v2_id (str/int): Id's dos vértices terminais da aresta 
            sendo buscada
        S: peso (float) ou infinito
        """
        aresta = self.get_aresta(v1_id, v2_id)
        if aresta and aresta.peso is not None:
            return get_decimal(aresta.peso)
        else:
            return Decimal('Infinity')

    
