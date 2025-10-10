"""
Módulo:    converter
Descriçao: Contém funções para converter e sincronizar as diferentes
           representações de dados de um objeto Grafo.
"""
import collections
from lib.core.graph import Grafo

def matriz_adj_para_lista_adj(grafo: Grafo):
    """
    Tarefa: (4) Conversão entre Matriz e Lista de Adjacências.
    Info: (Função de utilidade) Sobrescreve a lista de adjacências do grafo
          com base em sua matriz de adjacência atual.
    E: grafo (Grafo) - A instância do grafo a ser modificada.
    S: None
    """
    nova_lista_adj = collections.defaultdict(list)
    for i, vertice_i in enumerate(grafo.vertices):
        # Garante que todo vértice exista como chave, mesmo que sem arestas de saída
        nova_lista_adj[vertice_i] = []
        for j, vertice_j in enumerate(grafo.vertices):
            if grafo.matriz_adj[i][j] == 1:
                nova_lista_adj[vertice_i].append(vertice_j)
    grafo.lista_adj = nova_lista_adj

def lista_adj_para_matriz_adj(grafo: Grafo):
    """
    Tarefa: (4) Conversão entre Matriz e Lista de Adjacências.
    Info: (Função de utilidade) Sobrescreve a matriz de adjacências do grafo
          com base em sua lista de adjacência atual.
    E: grafo (Grafo) - A instância do grafo a ser modificada.
    S: None
    """
    n = grafo.num_vertices()
    grafo.matriz_adj = [[0] * n for _ in range(n)]
    for vertice, vizinhos in grafo.lista_adj.items():
        i = grafo.vertices.index(vertice)
        for vizinho in vizinhos:
            j = grafo.vertices.index(vizinho)
            grafo.matriz_adj[i][j] = 1

def arestas_para_matriz_inc(grafo: Grafo):
    """
    Info: (Função de utilidade) Sobrescreve a matriz de incidência do grafo com
          base em sua lista de vértices e arestas atual.
    E: grafo (Grafo) - A instância do grafo a ser modificada.
    S: None
    """
    num_v = grafo.num_vertices()
    num_a = grafo.num_arestas()
    grafo.matriz_incidencia = [[0] * num_a for _ in range(num_v)]

    for indice_aresta, aresta in enumerate(grafo.arestas):
        idx1 = grafo.vertices.index(aresta.v1)
        idx2 = grafo.vertices.index(aresta.v2)
        if grafo.direcionado:
            grafo.matriz_incidencia[idx1][indice_aresta] = 1
            grafo.matriz_incidencia[idx2][indice_aresta] = -1
        else:
            grafo.matriz_incidencia[idx1][indice_aresta] = 1
            grafo.matriz_incidencia[idx2][indice_aresta] = 1

def matriz_inc_para_arestas(grafo: Grafo):
    """
    Info: (Função de utilidade) Sobrescreve a lista de arestas do grafo com
          base na matriz de incidência atual.
    E: grafo (Grafo) - A instância do grafo a ser modificada.
    S: None
    """
    if not grafo.matriz_incidencia or not grafo.vertices:
        grafo.arestas = []
        return

    novas_arestas = []
    num_vertices = grafo.num_vertices()
    num_arestas_na_matriz = len(grafo.matriz_incidencia[0])

    for j in range(num_arestas_na_matriz):  # Itera sobre cada coluna (aresta)
        pontas = []
        origem, destino = None, None
        for i in range(num_vertices):  # Itera sobre cada linha (vértice)
            valor = grafo.matriz_incidencia[i][j]
            if grafo.direcionado:
                if valor == 1: origem = grafo.vertices[i]
                elif valor == -1: destino = grafo.vertices[i]
            elif valor == 1: # Não direcionado
                pontas.append(grafo.vertices[i])
        
        if grafo.direcionado:
            if origem and destino: novas_arestas.append(Aresta(origem, destino))
        elif len(pontas) == 2:
            novas_arestas.append(Aresta(pontas[0], pontas[1]))
    
    grafo.arestas = novas_arestas