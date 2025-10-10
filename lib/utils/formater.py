import math
from lib.core.graph import Grafo
from lib.algorithms.is_bipartite import is_bipartite
from lib.algorithms.is_connected import is_connected
from lib.algorithms.lowpt import lowpt 
from lib.core.graph_converter import matriz_adj_para_lista_adj, lista_adj_para_matriz_adj, get_grafo_subjacente

def formatar_lista_adj(grafo: Grafo):
    titulo = "\n==== (1) REPRESENTAÇÃO POR LISTA DE ADJACÊNCIA ===="
    output = [titulo]
    if not grafo.vertices:
        output.append("Vazia.")
        return "\n".join(output)
    
    sorted_vertices = sorted(grafo.lista_adj.keys(), key=lambda v: str(v.id))
    for vertice in sorted_vertices:
        vizinhos_ids = sorted([str(v.id) for v in grafo.lista_adj.get(vertice, [])])
        output.append(f"{vertice.id}: {vizinhos_ids}")
    return "\n".join(output)

def formatar_matriz_adj(grafo: Grafo):
    titulo = "\n==== (2) REPRESENTAÇÃO POR MATRIZ DE ADJACÊNCIA ===="
    if grafo.direcionado:
        titulo = "\n==== (16) REPRESENTAÇÃO POR MATRIZ DE ADJACÊNCIA ===="

    output = [titulo]
    ids = [str(v.id) for v in grafo.vertices]
    if not ids:
        output.append("Vazia.")
        return "\n".join(output)
        
    max_width = max(len(id) for id in ids)
    header = f"{' ' * max_width} |" + "".join(f" {id:>{max_width}}" for id in ids)
    output.append(header)
    output.append(f"{'-' * (max_width + 1)}+{'-' * (len(ids) * (max_width + 1))}")
    for i, linha in enumerate(grafo.matriz_adj):
        row_str = f"{ids[i]:>{max_width}} |" + "".join(f" {val:>{max_width}}" for val in linha)
        output.append(row_str)
    return "\n".join(output)

def formatar_matriz_incidencia(grafo: Grafo):
    titulo = "\n==== (3) REPRESENTAÇÃO POR MATRIZ DE INCIDÊNCIA ===="
    if grafo.direcionado:
        titulo = "\n==== (17) REPRESENTAÇÃO POR MATRIZ DE INCIDÊNCIA ===="
    
    output = [titulo]
    if not grafo.vertices or not grafo.arestas:
        output.append("Vazia.")
        return "\n".join(output)

    v_ids = [str(v.id) for v in grafo.vertices]
    e_ids = [f"e{i+1}" for i in range(grafo.num_arestas())]
    
    max_width = 0
    if v_ids: max_width = max(max_width, max(len(id) for id in v_ids))
    if e_ids: max_width = max(max_width, max(len(id) for id in e_ids))

    header = f"{' ' * max_width} |" + "".join(f" {id:>{max_width}}" for id in e_ids)
    output.append(header)
    output.append(f"{'-' * (max_width + 1)}+{'-' * (len(e_ids) * (max_width + 1))}")

    for i, linha in enumerate(grafo.matriz_incidencia):
        row_str = f"{v_ids[i]:>{max_width}} |" + "".join(f" {val:>{max_width}}" for val in linha)
        output.append(row_str)
        
    return "\n".join(output)

def formatar_conversoes(grafo: Grafo):
    output = ["\n==== (4) CONVERSÃO ENTRE REPRESENTAÇÕES ===="]
    lista_adj_original = {k: list(v) for k, v in grafo.lista_adj.items()}
    matriz_adj_original = [row[:] for row in grafo.matriz_adj]
    output.append("\n--- Matriz -> Lista ---")
    matriz_adj_para_lista_adj(grafo)
    output.append(formatar_lista_adj(grafo).split('\n', 2)[-1])
    grafo.lista_adj = lista_adj_original
    output.append("\n--- Lista -> Matriz ---")
    lista_adj_para_matriz_adj(grafo)
    output.append(formatar_matriz_adj(grafo).split('\n', 2)[-1])
    grafo.lista_adj = lista_adj_original
    grafo.matriz_adj = matriz_adj_original
    return "\n".join(output)

def formatar_graus(grafo: Grafo):
    output = ["\n==== (5) GRAU DE CADA VÉRTICE ===="]
    if not grafo.vertices:
        output.append("Vazio.")
        return "\n".join(output)
    sorted_vertices = sorted(grafo.vertices, key=lambda v: str(v.id))
    degree_strings = []
    for v in sorted_vertices:
        grau = grafo.get_grau(v.id)
        if grau is not None and not isinstance(grau, tuple):
            degree_strings.append(f"d({v.id}) = {grau}")
    num_cols = 3
    max_len = max(len(s) for s in degree_strings) if degree_strings else 0
    padded_strings = [s.ljust(max_len) for s in degree_strings]
    num_rows = math.ceil(len(padded_strings) / num_cols)
    for i in range(num_rows):
        row_parts = [padded_strings[i + j * num_rows] for j in range(num_cols) if i + j * num_rows < len(padded_strings)]
        output.append("   ".join(row_parts))
    return "\n".join(output)

def formatar_adjacencias_por_vertice(grafo: Grafo):
    output = ["\n==== (6) ADJACÊNCIAS DE CADA VÉRTICE ===="]
    if not grafo.vertices:
        output.append("Vazio.")
        return "\n".join(output)
    sorted_vertices = sorted(grafo.vertices, key=lambda v: str(v.id))
    for v in sorted_vertices:
        adjacentes_ids = sorted([str(adj.id) for adj in grafo.lista_adj.get(v, [])])
        output.append(f"Adjacentes de {v.id}: {adjacentes_ids}")
    return "\n".join(output)

def formatar_info_gerais(grafo: Grafo):
    output = [
        f"\n==== (7) NÚMERO TOTAL DE VÉRTICES ====\n{grafo.num_vertices()}",
        f"\n==== (8) NÚMERO TOTAL DE ARESTAS ====\n{grafo.num_arestas()}"
    ]
    return "\n".join(output)

def formatar_eh_conexo(grafo: Grafo):
    output = ["\n==== (11) CONECTIVIDADE ===="]
    resultado = "Sim" if is_connected(grafo) else "Não"
    output.append(f"O grafo é conexo? {resultado}")
    return "\n".join(output)

def formatar_bipartido(grafo: Grafo):
    output = ["\n==== (12) BIPARTIÇÃO (OPC) ===="]
    resultado = "Sim" if is_bipartite(grafo) else "Não"
    output.append(f"O grafo é bipartido? {resultado}")
    return "\n".join(output)

def formatar_biconectividade(grafo: Grafo):
    output = ["\n==== (15) BICONECTIVIDADE (ARTICULAÇÕES E PONTES) ===="]
    if grafo.num_vertices() == 0:
        output.append("Grafo vazio.")
        return "\n".join(output)
    articulacoes, pontes = lowpt(grafo)
    if not articulacoes:
        output.append("Pontos de Articulação: Nenhum.")
    else:
        output.append(f"Pontos de Articulação: {sorted(list(articulacoes), key=str)}")
    if not pontes:
        output.append("Pontes: Nenhuma.")
    else:
        output.append(f"Pontes: {sorted(list(pontes))}")
    return "\n".join(output)
    
def formatar_grafo_subjacente(grafo: Grafo):
    output = ["\n==== (18) GRAFO SUBJACENTE (OPC) ===="]
    subjacente = get_grafo_subjacente(grafo)
    # Chama a função formatar_lista_adj, que agora só tem o título (1), e remove esse título
    texto_lista = formatar_lista_adj(subjacente).split('\n', 2)[-1]
    output.append(texto_lista)
    return "\n".join(output)

def gerar_relatorio_completo(grafo: Grafo):
    header = [
        "*********************************************************************",
        f"Arquivo: {grafo.nome_arquivo}",
    ]
    if not grafo.direcionado:
        report_body = [
            "Análise para: GRAFO NÃO-DIRECIONADO",
            formatar_lista_adj(grafo),                 # (1)
            formatar_matriz_adj(grafo),                # (2)
            formatar_matriz_incidencia(grafo),         # (3)
            formatar_conversoes(grafo),                # (4)
            formatar_graus(grafo),                     # (5)
            formatar_adjacencias_por_vertice(grafo),   # (6)
            formatar_info_gerais(grafo),               # (7) e (8)
            "\n==== (9) e (10) INCLUSÃO E EXCLUSÃO DE VÉRTICES ====\nINFO: Funções implementadas na classe Grafo para manipulação dos dados.",
            formatar_eh_conexo(grafo),                 # (11)
            formatar_bipartido(grafo),                 # (12)
            "\n==== (13) e (14) BUSCAS BFS E DFS ====\nINFO: As buscas são executadas e seus resultados renderizados visualmente.",
            formatar_biconectividade(grafo),           # (15)
        ]
    else:
        report_body = [
            "Análise para: DÍGRAFO",
            formatar_matriz_adj(grafo),                # (16)
            formatar_matriz_incidencia(grafo),         # (17)
            formatar_grafo_subjacente(grafo),          # (18)
            "\n==== (19) e (20) BUSCAS BFS E DFS ====\nINFO: As buscas são executadas e seus resultados (com classificação completa de arestas para DFS) são renderizados visualmente.",
        ]
    return "\n".join(header + report_body)

