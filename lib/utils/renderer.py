"""
Módulo:    Rendererizador
Descriçao: Contém funções que utilizam a biblioteca `graphviz` para gerar
           representações visuais (imagens PNG) de objetos `Grafo`, bem como
           de resultados de algoritmos de busca (BFS e DFS).
"""
from graphviz import Digraph, Graph
from collections import defaultdict
from lib.core.graph import Grafo, Vertice

def renderizar_grafo(grafo: Grafo):
    """
    Info: (Função de renderização) Cria uma representação visual (dot object)
          de um grafo ou digrafo utilizando as informações de seus
          vértices e arestas.
    E: grafo (Grafo) - A instância do grafo a ser visualizada.
    S: dot (Graph/Digraph) - Um objeto `graphviz` que pode ser renderizado
       em um arquivo de imagem (e.g., PNG).
    """
    if grafo.direcionado:
        dot = Digraph(comment=f'Digrafo: {grafo.nome_arquivo}', format="png")
    else:
        dot = Graph(comment=f'Grafo: {grafo.nome_arquivo}', format="png")
        
    dot.graph_attr.update({
        "layout": "sfdp",
        "pad": "0.2",
        "normalize": "true",
        "sep": "+1",
        "rankdir": "TB",
        "splines": "true",
        "overlap": "scale",
        "K": "0.1"
    })

    dot.edge_attr.update({
        "len": "1.6"
    })

    for vertice in grafo.vertices:
        dot.node(str(vertice.id), style="solid", penwidth='2.0')

    for aresta in grafo.arestas:
        label = str(aresta.peso) if aresta.peso or aresta.peso == 0 else None
        dot.edge(str(aresta.v1.id), str(aresta.v2.id),
         style="solid",
         penwidth="2.0",
         label=label,
         constraint="true", 
         minlen="2", 
         fontcolor = "red",
         )
            
    return dot

def renderizar_agm(grafo: Grafo):
    """
    Info: (Função de renderização) Cria uma representação visual (dot object)
          de uma AGM utilizando as informações de seus
          vértices e arestas.
    E: grafo (Grafo) - A instância do grafo a ser visualizada.
    S: dot (Graph/Digraph) - Um objeto `graphviz` que pode ser renderizado
       em um arquivo de imagem (e.g., PNG).
    """
    if grafo.direcionado:
        dot = Digraph(comment=f'Digrafo: {grafo.nome_arquivo}', format="png")
    else:
        dot = Graph(comment=f'Grafo: {grafo.nome_arquivo}', format="png")
        
    dot.graph_attr.update({
        "layout": "dot", "rankdir": "LR", "splines": "true", "overlap": "false",
    })

    for vertice in grafo.vertices:
        dot.node(str(vertice.id), style="solid", penwidth='2.0')

    for aresta in grafo.arestas:
        label = str(aresta.peso) if aresta.peso or aresta.peso == 0 else None
        dot.edge(str(aresta.v1.id), str(aresta.v2.id), style="solid", penwidth='2.0', label=label, fontcolor = "red",)
            
    return dot

def renderizar_bfs(ordem, arestas_retorno=None, nome_grafo="BFS", ranksep=1.0, nodesep=0.6, direcionado=False):
    """
    Info: (Função de renderização) Cria uma representação visual da travessia
          realizada pelo algoritmo de Busca em Largura (BFS).
          As arestas de percurso (árvore BFS) são sólidas e as arestas
          de retorno (se fornecidas) são tracejadas. Os vértices são agrupados
          por nível (rank=same).
    E: ordem (list) - Lista de tuplas (vértice, pai) que define a ordem da BFS.
    E: arestas_retorno (set/list) - Conjunto opcional de tuplas (u, v)
       representando arestas de retorno (não-árvore).
    E: nome_grafo (str) - Nome do grafo/imagem.
    E: ranksep (float), nodesep (float) - Parâmetros de layout `graphviz`.
    E: direcionado (bool) - Indica se o gráfico deve ser um `Digraph` (True) ou `Graph` (False).
    S: dot (Graph/Digraph) - O objeto `graphviz` da visualização da BFS.
    """
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
    """
    Info: (Função de renderização) Cria uma representação visual da travessia
          realizada pelo algoritmo de Busca em Profundidade (DFS).
          As arestas de percurso (árvore DFS) são sólidas e as arestas
          de retorno (se fornecidas) são tracejadas.
    E: ordem (list) - Lista de tuplas (vértice, pai) que define a ordem da DFS.
    E: arestas_retorno (set/list) - Conjunto opcional de tuplas (u, v)
       representando arestas de retorno (back edges).
    E: nome_grafo (str) - Nome do grafo/imagem.
    E: direcionado (bool) - Indica se o gráfico deve ser um `Digraph` (True) ou `Graph` (False).
    S: dot (Graph/Digraph) - O objeto `graphviz` da visualização da DFS.
    """
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
    """
    Info: Função auxiliar para converter um objeto Aresta em uma tupla
          de strings (ID_v1, ID_v2) para uso com `graphviz`.
    E: aresta (Aresta) - Objeto aresta a ser convertido.
    S: tupla (str, str) - Tupla com os IDs dos vértices como strings.
    """
    return (str(aresta.v1.id), str(aresta.v2.id))

def renderizar_bfs_classificada(ordem_visita, arestas_arvore, arestas_cruzamento, nome_grafo="BFS_Classificada"):
    """
    Info: (Função de renderização) Cria uma representação visual da BFS
          classificando as arestas em Arestas de Árvore e Arestas de Cruzamento.
          Arestas de Árvore são sólidas (preto), Arestas de Cruzamento são
          pontilhadas (azul-escuro). Os vértices são agrupados por nível.
    E: ordem_visita (list) - Lista de tuplas (vértice, pai).
    E: arestas_arvore (list) - Lista de objetos `Aresta` que formam a árvore BFS.
    E: arestas_cruzamento (list) - Lista de objetos `Aresta` classificadas
       como arestas de cruzamento.
    E: nome_grafo (str) - Nome do grafo/imagem.
    S: dot (Digraph) - O objeto `graphviz` da visualização da BFS classificada.
    """
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
    """
    Info: (Função de renderização) Cria uma representação visual da DFS
          classificando as arestas em Arestas de Árvore, Retorno, Avanço e Cruzamento.
          Cada tipo de aresta recebe uma cor e estilo distintos, e um rótulo
          (R, A ou C) para melhor identificação.
    E: ordem_visita (list) - Lista de tuplas (vértice, pai).
    E: arestas_arvore (list), arestas_retorno (list), arestas_avanco (list), 
       arestas_cruzamento (list) - Listas de objetos `Aresta` classificadas.
    E: nome_grafo (str) - Nome do grafo/imagem.
    S: dot (Digraph) - O objeto `graphviz` da visualização da DFS classificada.
    """
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
    """
    Info: (Função de renderização) Cria uma representação visual do grafo
          subjacente de um digrafo (grafo não-direcionado correspondente).
          Arestas paralelas entre os mesmos dois vértices no digrafo são
          representadas por uma única aresta no grafo subjacente.
    E: digrafo (Grafo) - A instância do digrafo.
    S: dot (Graph) - O objeto `graphviz` do grafo subjacente.
    """
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

def renderizar_caminho_curto(grafo: Grafo, caminho: list[Vertice], nome_grafo="Caminho_Curto"):
    """
    Info: (Função de renderização) Cria uma representação visual de um grafo
          destacando um caminho específico (ex: caminho mais curto).
    E: grafo (Grafo) - A instância do grafo a ser visualizada.
    E: caminho (list[Vertice]) - Uma lista ordenada de vértices que compõem o caminho.
    E: nome_grafo (str) - Nome do grafo/imagem.
    S: dot (Digraph) - O objeto `graphviz` da visualização.
    """
    dot = Digraph(comment=nome_grafo, format="png")
    dot.graph_attr.update({
        "layout": "sfdp", "pad": "0.2", "normalize": "true", "sep": "+1",
        "rankdir": "TB", "splines": "true", "overlap": "scale", "K": "0.1"
    })
    if not caminho:
        return renderizar_grafo(grafo)
    caminho_ids = {str(v.id) for v in caminho}
    caminho_arestas = set()
    for i in range(len(caminho) - 1):
        caminho_arestas.add((str(caminho[i].id), str(caminho[i+1].id)))
    start_id = str(caminho[0].id)
    end_id = str(caminho[-1].id)
    for v in grafo.vertices:
        v_id_str = str(v.id)
        if v_id_str == start_id:
            dot.node(v_id_str, style="filled", fillcolor="palegreen", penwidth="2.5", shape="doublecircle")
        elif v_id_str == end_id:
            dot.node(v_id_str, style="filled", fillcolor="tomato", penwidth="2.5", shape="doublecircle")
        elif v_id_str in caminho_ids:
            dot.node(v_id_str, style="filled", fillcolor="lightblue", penwidth="2.0")
        else:
            dot.node(v_id_str, style="solid", penwidth="1.0", color="gray")
    for a in grafo.arestas:
        v1_str, v2_str = str(a.v1.id), str(a.v2.id)
        label = str(a.peso) if a.peso is not None else None
        if (v1_str, v2_str) in caminho_arestas:
            dot.edge(v1_str, v2_str,
                     label=label,
                     color="green",
                     penwidth="3.0",
                     fontcolor="red")
        else:
            dot.edge(v1_str, v2_str,
                     label=label,
                     color="gray",
                     penwidth="1.0",
                     fontcolor="gray")
    return dot