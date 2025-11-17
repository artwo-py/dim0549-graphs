"""
Módulo:    Hierholzer - Caminhos
Objetivo:  Implementa o algoritmo de Hierholzer para encontrar um caminho euleriano.
"""

from lib.core.graph import Grafo, Vertice
from lib.algorithms.is_connected import is_connected

def _verificar_condicoes_eulerianas(grafo):
    """
    Verifica se o grafo atende às condições necessárias para a existência de um caminho euleriano.
    Condições:
    - Não-direcionado: todos os vértices possuem grau par ou no máximo dois vértices possuem grau ímpar.
    - Direcionado: no máximo um vértice tem grau (d^{+}-d^{-}=1) e no máximo um vértice 
        tem grau (d^{-}-d^{+}=1). Todos os demais vértices tem o mesmo grau de entrada e de saída.

    Returns:
        tuple (bool, Vertice or None): 
            - bool: True se as condições forem atendidas, False caso contrário.
            - Vertice or None: o vértice inicial de onde o caminho deve começar, ou None.
    """
    vertice_inicial = None

    if grafo.direcionado:
        d_pos_um = []
        d_neg_um = []

        for v in grafo.vertices:
            grau = grafo.get_grau(v.id)
            grau_entrada, grau_saida = grau
            diferenca = grau_saida - grau_entrada

            if diferenca == 1:
                d_pos_um.append(v)
            elif diferenca == -1:
                d_neg_um.append(v)
            elif diferenca != 0:
                return False, None

        if (len(d_pos_um) == 0 and len(d_neg_um) == 0):
            vertice_inicial = next((v for v in grafo.vertices if grafo.get_grau(v.id)[0] + grafo.get_grau(v.id)[1] > 0), None)
            return True, vertice_inicial
        elif (len(d_pos_um) == 1 and len(d_neg_um) == 1):
            vertice_inicial = d_pos_um[0]
            return True, vertice_inicial
        else:
            return False, None

    else: 
        graus_impares = []
        for v in grafo.vertices:
            grau = grafo.get_grau(v.id)
            if grau % 2 != 0:
                graus_impares.append(v)

        if len(graus_impares) == 0:
            vertice_inicial = next((v for v in grafo.vertices if grafo.get_grau(v.id) > 0), None)
            return True, vertice_inicial
        elif len(graus_impares) == 2:
            vertice_inicial = graus_impares[0]
            return True, vertice_inicial
        else:
            return False, None


def hierholzer_caminhos(grafo):
    """
    Implementa o algoritmo de Hierholzer para encontrar um caminho euleriano.

    Args:
        grafo (Grafo): O objeto grafo.
    Returns:
        list: Lista de IDs de vértices em ordem que forma o caminho euleriano.
    """

    is_eulerian_possible, vertice_inicial = _verificar_condicoes_eulerianas(grafo)

    if not is_eulerian_possible:
        #print("Caminho euleriano não é possível: condições de grau não atendidas.")
        return None

    if not is_connected(grafo):
        #print("Caminho euleriano não é possível: grafo não é conectado.")
        return None

    if grafo.num_arestas() == 0:
        return []
    
    circuito = [] 
    pilha = [vertice_inicial] 

    while pilha:
        u = pilha[-1]

        vizinhos = grafo.lista_adj.get(u, [])

        if vizinhos:
            v = vizinhos[0] 
            grafo.remover_aresta(u.id, v.id)
            pilha.append(v)

        else:
            circuito.append(u.id)
            pilha.pop()

    return circuito[::-1]