"""
Algoritmo de Chu-Liu/Edmonds
Implementa uma Arborescência Geradora Mínima (AGM) em dígrafos.

Entrada:
    grafo (Grafo) – grafo direcionado e ponderado
    raiz (str/int) – identificador do vértice raiz

Saída:
    (novo_grafo, None) - se sucesso
    (None, mensagem_erro) - se falhar
"""

from math import inf as infinito
from lib.core.graph import Grafo


def chu_liu_edmonds(grafo, raiz):
    vertices = list(grafo.vertices)
    n = len(vertices)

    idx = {v.id: i for i, v in enumerate(vertices)}
    id_map = {i: v.id for i, v in enumerate(vertices)}
    r = idx[str(raiz)]

    edges = [(idx[a.v1.id], idx[a.v2.id], a.peso) for a in grafo.arestas]

    arestas_resultado, erro = _chu_liu_recursivo(edges, n, r, id_map)

    if not arestas_resultado:
        return None, erro

    novo = Grafo(direcionado=True, ponderado=True)
    novo.nome_arquivo = grafo.nome_arquivo.replace("DIGRAFO_", "AGM_")

    for v in grafo.vertices:
        novo.adicionar_vertice(v.id)

    for u_idx, v_idx, peso in arestas_resultado:
        novo.adicionar_aresta(id_map[u_idx], id_map[v_idx], peso)

    return novo, None


def _chu_liu_recursivo(edges, n, r, id_map=None):
    edges = [(u, v, custo) for (u, v, custo) in edges if v != r]
    min_in = [-1] * n
    min_cost = [infinito] * n

    for u, v, custo in edges:
        if custo < min_cost[v]:
            min_cost[v] = custo
            min_in[v] = u
    vertices_isolados = []
    for v in range(n):
        if v != r and min_in[v] == -1:
            if id_map:
                vertices_isolados.append(id_map[v])
            else:
                vertices_isolados.append(str(v))

    if vertices_isolados:
        erro = f"Vértices não alcançáveis da raiz: {', '.join(vertices_isolados)}"
        return [], erro

    cycle_vertex = None
    for v in range(n):
        if cycle_vertex is not None:
            break
        visited = set()
        next_v = v

        while next_v is not None and next_v != r:
            if next_v in visited:
                cycle_vertex = next_v
                break
            visited.add(next_v)
            next_v = min_in[next_v] if min_in[next_v] != -1 else None

    if cycle_vertex is None:
        resultado = []
        for v in range(n):
            if v != r and min_in[v] != -1:
                resultado.append((min_in[v], v, min_cost[v]))
        return resultado, None

    ciclo = set()
    ciclo.add(cycle_vertex)
    next_v = min_in[cycle_vertex]
    while next_v != cycle_vertex:
        ciclo.add(next_v)
        next_v = min_in[next_v]

    v_c = -(cycle_vertex ** 2 + 1)
    cycle_id = {}
    for v in range(n):
        if v in ciclo:
            cycle_id[v] = v_c
        else:
            cycle_id[v] = v

    cycle_min_cost = min(min_cost[v] for v in ciclo)

    new_edges = []
    correspondencia = {}

    for u, v, custo in edges:
        u_new = cycle_id[u]
        v_new = cycle_id[v]
        if u_new == v_new:
            continue

        e_new = (u_new, v_new)
        if v in ciclo and u not in ciclo:
            custo_ajustado = custo - (min_cost[v] - cycle_min_cost)
            if e_new in correspondencia:
                if correspondencia[e_new][2] < custo_ajustado:
                    continue

            correspondencia[e_new] = (u, v, custo)
            new_edges.append((u_new, v_new, custo_ajustado))
        elif u in ciclo and v not in ciclo:
            if e_new in correspondencia:
                u_old, v_old, custo_old = correspondencia[e_new]
                if custo_old < custo:
                    continue

            correspondencia[e_new] = (u, v, custo)
            new_edges.append((u_new, v_new, custo))
        else:
            correspondencia[e_new] = (u, v, custo)
            new_edges.append((u_new, v_new, custo))

    new_n = len(set(cycle_id.values()))
    new_r = r if r not in ciclo else v_c
    vertices_novos = sorted(set(cycle_id.values()))
    idx_map = {v: i for i, v in enumerate(vertices_novos)}
    idx_reverse = {i: v for v, i in idx_map.items()}

    new_edges_remapped = [
        (idx_map[u], idx_map[v], custo)
        for u, v, custo in new_edges
    ]
    new_r_remapped = idx_map[new_r]
    tree, erro = _chu_liu_recursivo(new_edges_remapped, new_n, new_r_remapped)

    if not tree:
        return [], erro

    aresta_remover = None

    for u_idx, v_idx, peso in tree:
        u_orig = idx_reverse[u_idx]
        v_orig = idx_reverse[v_idx]

        if v_orig == v_c:
            u_real, v_real, custo_real = correspondencia[(u_orig, v_orig)]
            aresta_remover = (min_in[v_real], v_real)
            break

    resultado = []
    for u_idx, v_idx, peso in tree:
        u_orig = idx_reverse[u_idx]
        v_orig = idx_reverse[v_idx]
        u_real, v_real, custo_real = correspondencia[(u_orig, v_orig)]
        resultado.append((u_real, v_real, custo_real))

    for v in ciclo:
        u = min_in[v]
        resultado.append((u, v, min_cost[v]))

    if aresta_remover:
        u_rem, v_rem = aresta_remover
        resultado = [(u, v, c) for (u, v, c) in resultado if not (u == u_rem and v == v_rem)]

    return resultado, None
