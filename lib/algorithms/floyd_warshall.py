"""
Módulo:    Floyd-Warshall
Objetivo:  Implementa o algoritmo de Floyd-Warshall para encontrar os caminhos mais curtos
           entre todos os pares de vértices em um grafo ponderado e direcionado.
           
Funções:   floyd_warshall(grafo)
           reconstruir_caminho(pred, vertices, i_idx, j_idx)
"""

import copy
from math import inf as infinito
from lib.core.graph import Grafo, Vertice

def floyd_warshall(grafo: Grafo):
    """
    Tarefa: (7) Algoritmo de Floyd-Warshall
    Info: Encontra os caminhos mais curtos entre todos os pares de vértices.
          Baseado no pseudocódigo fornecido.
    Args:
        grafo (Grafo): O objeto grafo, que deve ser ponderado.
    Returns:
        tuple: (dist, pred, vertices)
               dist (list[list]): Matriz n x n de distâncias mínimas.
               pred (list[list]): Matriz n x n de predecessores para reconstrução de caminhos.
               vertices (list[Vertice]): Lista de vértices para mapeamento de índices.
    """
    
    if not grafo.ponderado:
        raise ValueError("O algoritmo de Floyd-Warshall requer um grafo ponderado.")

    n = grafo.num_vertices()
    vertices = grafo.vertices
    dist = copy.deepcopy(grafo.matriz_adj) 
    pred = [[None for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(n):
            if dist[i][j] != infinito and i != j:
                pred[i][j] = i  
        dist[i][i] = 0
        pred[i][i] = i
    for k in range(n):     
        for i in range(n):  
            for j in range(n):  
                dist_via_k = dist[i][k] + dist[k][j]
                if dist_via_k < dist[i][j]:
                    dist[i][j] = dist_via_k
                    pred[i][j] = pred[k][j] 
    return dist, pred, vertices

def reconstruir_caminho(pred: list[list], vertices: list[Vertice], i_idx: int, j_idx: int):
    """
    Tarefa: (7) Recuperação de Caminhos
    Info: Reconstrói o caminho mais curto entre os vértices de índice i_idx e j_idx
          usando a matriz de predecessores (pred) gerada pelo Floyd-Warshall.
    Args:
        pred (list[list]): A matriz de predecessores.
        vertices (list[Vertice]): A lista de vértices (para mapear índices para objetos).
        i_idx (int): O índice do vértice inicial.
        j_idx (int): O índice do vértice final.
    Returns:
        list[Vertice] or None: Uma lista de objetos Vertice representando o caminho
                               de i para j, ou None se não houver caminho.
    """
    if pred[i_idx][j_idx] is None:
        return None 
    caminho = [vertices[j_idx]]
    atual_idx = j_idx
    while atual_idx != i_idx:
        predecessor_idx = pred[i_idx][atual_idx]
        if predecessor_idx is None:
            return None 
        caminho.append(vertices[predecessor_idx])
        atual_idx = predecessor_idx
    return caminho[::-1]