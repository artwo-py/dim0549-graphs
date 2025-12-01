from lib.algorithms.local_searches import two_opt

def nearest_neighbor(grafo, inicio):
    """Implementa o algoritmo do vizinho mais próximo para encontrar um ciclo hamiltoniano aproximado.

    Args:
        grafo (Grafo): O grafo onde o ciclo será encontrado.
        inicio (str): O vértice de início para o ciclo.

    Returns:
        tuple: Uma tupla contendo a lista de vértices no ciclo e o custo total do ciclo.
    """
    visitados = set()
    ciclo = []
    custo_total = 0
    atual = inicio.id if hasattr(inicio, "id") else inicio

    while len(visitados) < len(grafo.vertices):
        visitados.add(atual)
        ciclo.append(atual)

        vizinhos = grafo.get_vizinhos(atual)
        proximo = None
        menor_custo = float('inf')

        for vizinho, peso in vizinhos.items():
            if vizinho not in visitados and peso < menor_custo:
                menor_custo = peso
                proximo = vizinho

        if proximo is None:
            break

        custo_total += menor_custo
        atual = proximo

    if inicio in grafo.get_vizinhos(atual):
        custo_total += grafo.get_peso(atual, inicio)
        ciclo.append(inicio)

    return ciclo, custo_total