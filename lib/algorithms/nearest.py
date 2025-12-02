from lib.algorithms.local_searches import two_opt
from lib.utils.converter import get_decimal
from decimal import Decimal

def nearest_neighbor(grafo, inicio=0):
    """Implementa o algoritmo do vizinho mais próximo para encontrar um ciclo hamiltoniano aproximado.

    Args:
        grafo (Grafo): O grafo onde o ciclo será encontrado.
        inicio (str): O vértice de início para o ciclo.

    Returns:
        tuple: Uma tupla contendo a lista de vértices no ciclo e o custo total do ciclo.
    """
    visitados = set()
    ciclo = []
    custo_total = get_decimal(0)
    atual = inicio.id if hasattr(inicio, "id") else inicio

    while len(visitados) < len(grafo.vertices):
        visitados.add(atual)
        ciclo.append(atual)

        vizinhos = grafo.get_vizinhos(atual)
        proximo = None
        menor_custo = Decimal('Infinity')

        for vizinho, peso in vizinhos.items():
            peso = get_decimal(peso)
            if vizinho not in visitados and peso < menor_custo:
                menor_custo = peso
                proximo = vizinho

        if proximo is None:
            break
        
        custo_total += menor_custo
        atual = proximo

    custo_total += grafo.get_peso(atual, inicio)
    ciclo.append(inicio)

    return ciclo, custo_total