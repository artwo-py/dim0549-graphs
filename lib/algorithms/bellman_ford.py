"""
Algoritmo de Bellman-Ford
-------------------------
Implementa o cálculo de caminhos mínimos a partir de um vértice fonte.

Retorna:
    - dist: dicionário {id: distância}
    - pred: dicionário {id: predecessor}
    - ciclo_negativo: bool
"""

from math import inf as infinito

def bellman_ford(grafo, fonte_id):
    dist = {v.id: infinito for v in grafo.vertices}
    pred = {v.id: None for v in grafo.vertices}
    dist[str(fonte_id)] = 0
    V = len(grafo.vertices)
    arestas = grafo.arestas
    for _ in range(V - 1):
        mudou = False
        for a in arestas:
            u = a.v1.id
            v = a.v2.id
            w = a.peso

            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u
                mudou = True
        if not mudou:
            break
    for a in arestas:
        u = a.v1.id
        v = a.v2.id
        w = a.peso

        if dist[u] + w < dist[v]:
            return dist, pred, True
    return dist, pred, False

def formatar_caminho_bellman_ford(grafo, id_inicio: str, id_fim: str):
    """
    Executa Bellman-Ford, reconstrói o caminho e formata o texto.
    E: grafo (Grafo)
    E: id_inicio (str)
    E: id_fim (str)
    S: (str, list[str] or None)
    """
    titulo = f"\n==== (22) CAMINHO MAIS CURTO (BELLMAN-FORD {id_inicio} -> {id_fim}) ===="

    if not grafo.ponderado:
        return titulo + "\n  Algoritmo não aplicável (grafo não ponderado).", None
    try:
        dist, pred, ciclo_neg = bellman_ford(grafo, id_inicio)
        report = ""
        report += f"  Ciclo negativo? {ciclo_neg}\n"

        if dist[id_fim] == infinito:
            report += f"  Não há caminho entre {id_inicio} e {id_fim}."
            return titulo + "\n" + report, None
        caminho_ids = []
        atual = id_fim

        while atual is not None:
            caminho_ids.append(atual)
            atual = pred[atual]
        caminho_ids.reverse()
        custo = dist[id_fim]
        report += f"  Custo: {custo}\n"
        report += "  Caminho: " + " -> ".join(caminho_ids)
        vertices_map = {v.id: v for v in grafo.vertices}
        caminho_vertices = [vertices_map[v_id] for v_id in caminho_ids]
        return titulo + "\n" + report, caminho_vertices
    except Exception as e:
        return titulo + f"\n  Erro inesperado: {e}", None
