from graphviz import Digraph, Graph
from collections import defaultdict
from lib.core.graph import Grafo

def encontrar_arestas_de_retorno(grafo: Grafo):
    """
    Realiza uma busca em profundidade (DFS) para encontrar as arestas de retorno
    em um grafo direcionado, que são aquelas que fecham um ciclo.
    """
    adj = grafo.lista_adj
    visitando = set()  # Vértices na pilha de recursão atual
    visitado = set()   # Vértices já completamente explorados
    arestas_retorno = set()

    def dfs_visit(vertice_obj):
        visitando.add(vertice_obj)
        for vizinho_obj in adj.get(vertice_obj, []):
            if vizinho_obj in visitando:
                # Se o vizinho está na pilha de recursão, é uma aresta de retorno
                arestas_retorno.add((str(vertice_obj.id), str(vizinho_obj.id)))
            elif vizinho_obj not in visitado:
                dfs_visit(vizinho_obj)
        
        visitando.remove(vertice_obj)
        visitado.add(vertice_obj)

    for vertice in grafo.vertices:
        if vertice not in visitado:
            dfs_visit(vertice)
            
    return arestas_retorno

def renderizar_grafo(grafo: Grafo):
    """
    Renderiza a estrutura completa de um grafo ou dígrafo.
    """
    # CORREÇÃO: Trocado grafo.nome por grafo.nome_arquivo para refletir o atributo correto.
    if grafo.direcionado:
        dot = Digraph(comment=f'Digrafo: {grafo.nome_arquivo}', format="png")
    else:
        dot = Graph(comment=f'Grafo: {grafo.nome_arquivo}', format="png")
        
    dot.graph_attr.update({
        "layout": "neato",
        "rankdir": "LR",
        "splines": "true",
        "overlap": "false",
    })

    for vertice in grafo.vertices:
        dot.node(str(vertice.id), style="solid", penwidth='2.0')

    arestas_de_retorno = set()
    if grafo.direcionado:
        arestas_de_retorno = encontrar_arestas_de_retorno(grafo)

    for aresta in grafo.arestas:
        v1_id = str(aresta.v1.id)
        v2_id = str(aresta.v2.id)
        if (v1_id, v2_id) in arestas_de_retorno:
            dot.edge(v1_id, v2_id, style="dashed", penwidth='1.5', color="gray50", constraint='false')
        else:
            dot.edge(v1_id, v2_id, style="solid", penwidth='2.0', constraint='true')
            
    return dot

def renderizar_bfs(ordem, arestas_retorno=None, nome_grafo="BFS", ranksep=1.0, nodesep=0.6):
    """
    Renderiza a árvore de percurso de uma busca em largura (BFS).
    """
    nivel = defaultdict(int)
    for v, p in ordem:
        nivel[v] = 0 if p == "-" else nivel[p] + 1
        
    dot = Digraph(nome_grafo,
                  graph_attr={
                      "rankdir": "TB",
                      "ranksep": str(ranksep),
                      "nodesep": str(nodesep)
                  }, format="png")

    for v, _ in ordem:
        if v == ordem[0][0]:
            dot.node(v, style="filled", fillcolor="lightgreen", penwidth="2.5")
        else:
            dot.node(v, style="solid", penwidth="2.0")
       
    arestas_percurso = {(p, v) for v, p in ordem if p != "-"}
    for v, p in ordem:
        if p != "-":
            dot.edge(p, v, style="solid", penwidth='2.0', constraint='true')

    if arestas_retorno:
        for u, v in arestas_retorno:
            if (u, v) not in arestas_percurso:
                dot.edge(u, v, style="dashed", penwidth='1.5', color="gray50", constraint='false')

    nivel_max = max(nivel.values()) if nivel else -1
    for k in range(nivel_max + 1):
        mesmo_rank = [v for v, nv in nivel.items() if nv == k]
        if mesmo_rank:
            dot.body.append("{rank=same; " + "; ".join(mesmo_rank) + "}")
            
    return dot

def renderizar_dfs(ordem, arestas_retorno=None, nome_grafo="DFS"):
    """
    Renderiza a árvore de percurso de uma busca em profundidade (DFS).
    """
    dot = Digraph(nome_grafo,
                  graph_attr={
                      "layout": "dot",
                      "rankdir": "TB",
                      "overlap": "false",
                      "splines": "ortho",
                      "nodesep": "1.5" 
                  },
                  format="png")

    for v, _ in ordem:
        if v == ordem[0][0]:
            dot.node(v, style="filled", fillcolor="lightgreen", penwidth="2.5")
        else:
            dot.node(v, style="solid", penwidth="2.0")
            
    arestas_percurso = {(p, v) for v, p in ordem if p != "-"}
    for v, p in ordem:
        if p != "-":
            dot.edge(p, v, style="solid", penwidth='2.0', constraint='true')
            
    if arestas_retorno:
        for u, v in arestas_retorno:
            if (u,v) not in arestas_percurso:
                dot.edge(u, v, style="dashed", penwidth='1.5', color="gray50", constraint='false')

    return dot

def renderizar_grafo_subjacente(digrafo):
    dot = Graph(comment='My Undirected Graph', format="png")
    dot.graph_attr.update({
        "layout": "neato",
        "rankdir": "LR",
        "splines": "true",
        "overlap": "false",
    })
    for vertice in digrafo.vertices:
        dot.node(str(vertice.id), style="solid", penwidth='2.0')

    # Adiciona arestas sem duplicar
    arestas_adicionadas = set()
    for aresta in digrafo.arestas:
        v1_id = str(aresta.v1.id)
        v2_id = str(aresta.v2.id)

        # Cria uma tupla ordenada para evitar duplicatas (A,B) == (B,A)
        aresta_ordenada = tuple(sorted([v1_id, v2_id]))

        if aresta_ordenada not in arestas_adicionadas:
            dot.edge(v1_id, v2_id, style="solid", penwidth='2.0', constraint='true')
            arestas_adicionadas.add(aresta_ordenada)
    return dot

def aresta_para_tupla(aresta):
    """
    Função auxiliar para converter um objeto Aresta em uma tupla de IDs.
    """
    return (aresta.v1.id, aresta.v2.id)

def renderizar_dfs_classificada(ordem_visita, arestas_arvore, arestas_retorno, 
                                arestas_avanco, arestas_cruzamento, nome_grafo="DFS_Classificada"):
    """
    Renderiza a árvore DFS com as arestas classificadas por tipo.
    """
    dot = Digraph(nome_grafo,
                  graph_attr={"rankdir": "TB"},
                  format="png")
    
    for v_id, _ in ordem_visita:
        label = f"{v_id}"
        dot.node(str(v_id), label=label)

    # Arestas de árvore (preto)
    for aresta in arestas_arvore:
        u_id, v_id = aresta_para_tupla(aresta)
        dot.edge(str(u_id), str(v_id), color="black")

    # Arestas de retorno (verde)
    for aresta in arestas_retorno:
        u_id, v_id = aresta_para_tupla(aresta)
        dot.edge(str(u_id), str(v_id), color="green4", style="dashed", constraint="false")

    # Arestas de avanço (rosa)
    for aresta in arestas_avanco:
        u_id, v_id = aresta_para_tupla(aresta)
        dot.edge(str(u_id), str(v_id), color="deeppink", style="dashed")

    # Arestas de cruzamento (roxo)
    for aresta in arestas_cruzamento:
        u_id, v_id = aresta_para_tupla(aresta)
        dot.edge(str(u_id), str(v_id), color="purple", style="dashed", constraint="false")
        
    return dot

