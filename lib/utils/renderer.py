from graphviz import Digraph, Graph
from collections import defaultdict
from lib.core.graph import Grafo

def renderizar_grafo(grafo: Grafo):
    if grafo.direcionado:
        dot = Digraph(comment=f'Digrafo: {grafo.nome_arquivo}', format="png")
    else:
        dot = Graph(comment=f'Grafo: {grafo.nome_arquivo}', format="png")
        
    dot.graph_attr.update({
        "layout": "neato", "rankdir": "LR", "splines": "true", "overlap": "false",
    })

    for vertice in grafo.vertices:
        dot.node(str(vertice.id), style="solid", penwidth='2.0')

    for aresta in grafo.arestas:
        dot.edge(str(aresta.v1.id), str(aresta.v2.id), style="solid", penwidth='2.0')
            
    return dot

def renderizar_bfs(ordem, arestas_retorno=None, nome_grafo="BFS", ranksep=1.0, nodesep=0.6, direcionado=False):
    graph_attrs = {"rankdir": "TB", "ranksep": str(ranksep), "nodesep": str(nodesep)}
    if direcionado:
        dot = Digraph(nome_grafo, graph_attr=graph_attrs, format="png")
    else:
        dot = Graph(nome_grafo, graph_attr=graph_attrs, format="png")
        
    if not ordem: return dot
    
    vertice_inicial = ordem[0][0]
    for v, _ in ordem:
        if v == vertice_inicial:
            dot.node(v, style="filled", fillcolor="palegreen", penwidth="2.5")
        else:
            dot.node(v, style="solid", penwidth="2.0")

    arestas_percurso = {(p, v) for v, p in ordem if p != "-"}
    for v, p in ordem:
        if p != "-":
            dot.edge(p, v, style="solid", penwidth='2.0', constraint='true')

    if arestas_retorno:
        for u, v in arestas_retorno:
            if (u, v) not in arestas_percurso:
                dot.edge(u, v, style="dashed", penwidth='1.5', constraint='false')

    nivel = defaultdict(int)
    for v,p in ordem: nivel[v] = 0 if p == '-' else nivel[p] + 1
    nivel_max = max(nivel.values()) if nivel else -1
    for k in range(nivel_max + 1):
        mesmo_rank = [v for v, nv in nivel.items() if nv == k]
        if mesmo_rank:
            dot.body.append("{rank=same; " + "; ".join(mesmo_rank) + "}")
            
    return dot

def renderizar_dfs(ordem, arestas_retorno=None, nome_grafo="DFS", direcionado=False):
    graph_attrs = {"layout": "dot", "rankdir": "TB", "overlap": "false", "splines": "true", "nodesep": "0.8"}
    dot = Graph(nome_grafo, graph_attr=graph_attrs, format="png")
        
    if not ordem: return dot

    vertice_inicial = ordem[0][0]
    for v, _ in ordem:
        if v == vertice_inicial:
            dot.node(v, style="filled", fillcolor="palegreen", penwidth="2.5")
        else:
            dot.node(v, style="solid", penwidth="2.0")

    arestas_percurso = {(p, v) for v, p in ordem if p != "-"}
    for v, p in ordem:
        if p != "-":
            dot.edge(p, v, style="solid", penwidth='2.0', constraint='true')

    if arestas_retorno:
        for u, v_id in arestas_retorno:
            if (str(u), str(v_id)) not in arestas_percurso:
                dot.edge(str(u), str(v_id), style="dashed", penwidth='1.5', color="firebrick3", constraint='false', label="R", fontcolor="firebrick3")
                
    return dot

def aresta_para_tupla(aresta):
    return (str(aresta.v1.id), str(aresta.v2.id))

def renderizar_bfs_classificada(ordem_visita, arestas_arvore, arestas_cruzamento, nome_grafo="BFS_Classificada"):
    dot = Digraph(nome_grafo, graph_attr={"rankdir": "TB"}, format="png")

    if not ordem_visita: return dot

    vertice_inicial = ordem_visita[0][0]
    for v_id, _ in ordem_visita:
        if v_id == vertice_inicial:
            dot.node(v_id, style="filled", fillcolor="palegreen", penwidth="2.5")
        else:
            dot.node(v_id, style="solid", penwidth="2.0")

    for aresta in arestas_arvore:
        dot.edge(*aresta_para_tupla(aresta), color="black", penwidth='2.0')

    for aresta in arestas_cruzamento:
        dot.edge(*aresta_para_tupla(aresta), color="darkcyan", style="dotted", constraint="false", label="C", fontcolor="darkcyan")

    nivel = defaultdict(int)
    for v,p in ordem_visita: nivel[v] = 0 if p == '-' else nivel[p] + 1
    nivel_max = max(nivel.values()) if nivel else -1
    for k in range(nivel_max + 1):
        mesmo_rank = [v for v, nv in nivel.items() if nv == k]
        if mesmo_rank:
            dot.body.append("{rank=same; " + "; ".join(mesmo_rank) + "}")
            
    return dot

def renderizar_dfs_classificada(ordem_visita, arestas_arvore, arestas_retorno, 
                                arestas_avanco, arestas_cruzamento, nome_grafo="DFS_Classificada"):
    dot = Digraph(nome_grafo, graph_attr={"rankdir": "TB"}, format="png")
    
    if not ordem_visita: return dot

    vertice_inicial = ordem_visita[0][0]
    for v_id, _ in ordem_visita:
        if v_id == vertice_inicial:
            dot.node(v_id, style="filled", fillcolor="palegreen", penwidth="2.5")
        else:
            dot.node(v_id, style="solid", penwidth="2.0")

    for aresta in arestas_arvore:
        dot.edge(*aresta_para_tupla(aresta), color="black", penwidth='2.0')
    for aresta in arestas_retorno:
        dot.edge(*aresta_para_tupla(aresta), color="firebrick3", style="dashed", constraint="false", label="R", fontcolor="firebrick3")
    for aresta in arestas_avanco:
        dot.edge(*aresta_para_tupla(aresta), color="royalblue3", style="dotted", constraint="false", label="A", fontcolor="royalblue3")
    for aresta in arestas_cruzamento:
        dot.edge(*aresta_para_tupla(aresta), color="darkolivegreen", style="dotted", constraint="false", label="C", fontcolor="darkolivegreen")
        
    return dot

def renderizar_grafo_subjacente(digrafo):
    dot = Graph(comment='My Undirected Graph', format="png")
    dot.graph_attr.update({"layout": "neato", "rankdir": "LR", "splines": "true", "overlap": "false"})
    for vertice in digrafo.vertices:
        dot.node(str(vertice.id), style="solid", penwidth='2.0')
    arestas_adicionadas = set()
    for aresta in digrafo.arestas:
        v1_id, v2_id = str(aresta.v1.id), str(aresta.v2.id)
        aresta_ordenada = tuple(sorted([v1_id, v2_id]))
        if aresta_ordenada not in arestas_adicionadas:
            dot.edge(v1_id, v2_id, style="solid", penwidth='2.0', constraint='true')
            arestas_adicionadas.add(aresta_ordenada)
    return dot

