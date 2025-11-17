"""
Módulo:    Hierholzer - Ciclos
Objetivo:  Implementa o algoritmo de Hierholzer para encontrar um ciclo euleriano.
"""

from lib.core.graph import Grafo, Vertice
from lib.algorithms.is_connected import is_connected

def _verificar_condicoes_eulerianas(grafo):
    """
    Verifica se o grafo atende às condições necessárias para a existência de um ciclo euleriano.
    Condições:
    - Não-direcionado: Todos os vértices devem ter grau par.
    - Direcionado: Todos os vértices devem ter grau_entrada == grau_saida.

    Args:
        grafo (Grafo): O objeto grafo.

    Returns:
        bool: True se as condições forem atendidas, False caso contrário.
    """

    for v in grafo.vertices:
        grau = grafo.get_grau(v.id)
        if grafo.direcionado:
            grau_entrada, grau_saida = grau
            if grau_entrada != grau_saida:
                #print("grau_entrada != grau_saida")
                return False
        else:
            if grau % 2 != 0:
                #print("grau % 2 != 0")
                return False

    return True

def hierholzer_ciclos(grafo):
    """
    Implementa o algoritmo de Hierholzer para encontrar um ciclo euleriano.
    Args:
        grafo (Grafo): O objeto grafo.
    Returns:
        list: Lista de IDs de vértices em ordem que forma o ciclo euleriano.
    """

    if not _verificar_condicoes_eulerianas(grafo):
        #print("Ciclo euleriano não é possível: condições de grau não atendidas.")
        return None

    # Se o grafo tem arestas, ele deve ser conectado
    if grafo.num_arestas() > 0 and not is_connected(grafo):
        #print("Ciclo euleriano não é possível: grafo não é conectado.")
        return None

    if grafo.num_arestas() == 0:
        return []

    vertice_inicial = next((v for v in grafo.vertices if (grafo.get_grau(v.id) if not grafo.direcionado else grafo.get_grau(v.id)[0] + grafo.get_grau(v.id)[1]) > 0), None)

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
