import math
from lib.core.graph import Grafo
from lib.algorithms.is_bipartite import is_bipartite
from lib.algorithms.is_connected import is_connected
from lib.algorithms.lowpt import lowpt 
from lib.core.graph_converter import matriz_adj_para_lista_adj, lista_adj_para_matriz_adj, get_grafo_subjacente

def formatar_info_gerais(grafo: Grafo):
    output = [
        f"\n==== (7) NÚMERO TOTAL DE VÉRTICES ====\n{grafo.num_vertices()}",
        f"\n==== (8) NÚMERO TOTAL DE ARESTAS ====\n{grafo.num_arestas()}"
    ]
    return "\n".join(output)

def formatar_matriz_adj(grafo: Grafo):
    """Formata a matriz de adjacência com alinhamento dinâmico."""
    output = ["==== MATRIZ DE ADJACÊNCIA ===="]
    ids = [str(v.id) for v in grafo.vertices]
    if not ids:
        return "\n".join(output + ["Vazia."])

    max_width = max(len(id) for id in ids)
    header = f"{' ' * max_width} |" + "".join(f" {id:>{max_width}}" for id in ids)
    output.append(header)
    output.append(f"{'-' * (max_width + 1)}+{'-' * (len(ids) * (max_width + 1))}")

    for i, linha in enumerate(grafo.matriz_adj):
        row_str = f"{ids[i]:>{max_width}} |" + "".join(f" {val:>{max_width}}" for val in linha)
        output.append(row_str)
    return "\n".join(output)

def formatar_lista_adj(grafo: Grafo):
    """Formata a lista de adjacência com vértices e vizinhos ordenados."""
    output = ["\n==== LISTA DE ADJACÊNCIA ===="]
    if not grafo.vertices:
        return "\n".join(output + ["Vazia."])
        
    sorted_vertices = sorted(grafo.lista_adj.keys(), key=lambda v: str(v.id))
    for vertice in sorted_vertices:
        vizinhos_ids = sorted([str(v.id) for v in grafo.lista_adj.get(vertice, [])])
        output.append(f"{vertice.id}: {vizinhos_ids}")
    return "\n".join(output)

def formatar_bipartido(grafo: Grafo):
    """Verifica se o grafo é bipartido e formata a saída."""
    resultado = "Sim" if is_bipartite(grafo) else "Não"
    return f"\n(12) Bipartido: {resultado}"

def formatar_graus(grafo: Grafo):
    """Formata os graus dos vértices."""
    if grafo.direcionado:
        output = ["\n==== GRAUS DE ENTRADA E SAÍDA (Representação) ===="]
    else:
        output = ["\n==== (5) GRAU DE CADA VÉRTICE ===="]

    if not grafo.vertices:
        return "\n".join(output + ["Vazio."])

    sorted_vertices = sorted(grafo.vertices, key=lambda v: str(v.id))
    degree_strings = []
    
    for v in sorted_vertices:
        grau_info = grafo.get_grau(v.id)
        if grau_info is None: continue 

        if grafo.direcionado:
            grau_entrada, grau_saida = grau_info
            degree_strings.append(f"d+({v.id})={grau_saida}, d-({v.id})={grau_entrada}")
        else:
            grau = grau_info
            degree_strings.append(f"d({v.id}) = {grau}")

    num_cols = 3
    max_len = max(len(s) for s in degree_strings) if degree_strings else 0
    padded_strings = [s.ljust(max_len) for s in degree_strings]
    num_rows = math.ceil(len(padded_strings) / num_cols)
    for i in range(num_rows):
        row_parts = [padded_strings[i + j * num_rows] for j in range(num_cols) if i + j * num_rows < len(padded_strings)]
        output.append("   ".join(row_parts))
    return "\n".join(output)

def formatar_eh_conexo(grafo: Grafo):
    """Formata a resposta do grafo ser conexo ou não."""
    resultado = "Sim" if is_connected(grafo) else "Não"
    return f"\n(11) Conexo: {resultado}"
  
def _calcular_antecessores(grafo: Grafo):
    antecessores = {v: [] for v in grafo.vertices}
    for u, vizinhos in grafo.lista_adj.items():
        for v in vizinhos:
            antecessores[v].append(u)
    return antecessores

def formatar_adjacencias_por_vertice(grafo: Grafo):
    """Formata os adjacentes (ou sucessores/antecessores) de cada vértice."""
    if grafo.direcionado:
        output = ["\n==== SUCESSORES E ANTECESSORES (Representação) ===="]
    else:
        output = ["\n==== (6) ADJACÊNCIAS DE CADA VÉRTICE ===="]

    if not grafo.vertices:
        return "\n".join(output + ["Vazio."])

    sorted_vertices = sorted(grafo.vertices, key=lambda v: str(v.id))
    if grafo.direcionado:
        antecessores = _calcular_antecessores(grafo)
        for v in sorted_vertices:
            sucessores_ids = sorted([str(s.id) for s in grafo.lista_adj.get(v, [])])
            antecessores_ids = sorted([str(a.id) for a in antecessores.get(v, [])])
            output.append(f"{v.id}: Sucessores: {sucessores_ids}, Antecessores: {antecessores_ids}")
    else:
        for v in sorted_vertices:
            adjacentes_ids = sorted([str(adj.id) for adj in grafo.lista_adj.get(v, [])])
            output.append(f"Adjacentes de {v.id}: {adjacentes_ids}")
    return "\n".join(output)

def formatar_biconectividade(grafo: Grafo):
    """Formata a saída da análise de biconectividade."""
    output = ["\n==== (15) BICONECTIVIDADE (ARTICULAÇÕES E PONTES) ===="]
    
    if grafo.num_vertices() == 0:
        output.append("Grafo vazio.")
        return "\n".join(output)

    articulacoes, pontes = lowpt(grafo)
    
    if not articulacoes:
        output.append("Pontos de Articulação: Nenhum (o grafo é biconexo ou trivial).")
    else:
        articulacoes_sorted = sorted(list(articulacoes), key=str)
        output.append(f"Pontos de Articulação: {articulacoes_sorted}")
        
    if not pontes:
        output.append("Pontes: Nenhuma.")
    else:
        pontes_sorted = sorted(list(pontes))
        output.append(f"Pontes: {pontes_sorted}")
        
    return "\n".join(output)
    
def formatar_grafo_subjacente(grafo: Grafo):
    """Exibe a lista de adjacências do grafo subjacente."""
    output = ["\n==== (18) GRAFO SUBJACENTE ===="]
    subjacente = get_grafo_subjacente(grafo)
    output.append(formatar_lista_adj(subjacente).replace("\n==== LISTA DE ADJACÊNCIA ====\n", ""))
    return "\n".join(output)

def formatar_conversoes(grafo: Grafo):
    """Formata a demonstração de conversão entre matriz e lista."""
    output = ["\n==== (4) DEMONSTRAÇÃO DE CONVERSÃO ===="]
    lista_adj_original = {k: list(v) for k, v in grafo.lista_adj.items()}
    matriz_adj_original = [row[:] for row in grafo.matriz_adj]
    output.append("\n--- Matriz de Adjacências -> Lista de Adjacências ---")
    matriz_adj_para_lista_adj(grafo)
    output.append(formatar_lista_adj(grafo).replace("\n==== LISTA DE ADJACÊNCIA ====\n", ""))
    grafo.lista_adj = lista_adj_original
    output.append("\n--- Lista de Adjacências -> Matriz de Adjacências ---")
    lista_adj_para_matriz_adj(grafo)
    output.append(formatar_matriz_adj(grafo).replace("==== MATRIZ DE ADJACÊNCIA ====", ""))
    grafo.lista_adj = lista_adj_original
    grafo.matriz_adj = matriz_adj_original
    return "\n".join(output)

def formatar_biconectividade(grafo):
    output = []
    if not grafo.vertices:
        return "\n".join(output + ["Vazio."])

    if not grafo.direcionado:
        output.append("\n==== BICONECTIVIDADE ====")

        vertice_inicial = str(grafo.vertices[0].id)
        articulacoes, blocos = biconnectivity(grafo, vertice_inicial)
    
        vertice_inicial = str(grafo.vertices[0].id)
        articulacoes, blocos = biconnectivity(grafo, vertice_inicial)
        
        output.append("Articulações encontradas:")
        articulacoes_str = ", ".join(sorted([str(a) for a in articulacoes])) # Converte IDs em str e junta
        output.append(f"{{ {articulacoes_str} }}") 
        
        if not blocos:
            output.append("Nenhum bloco biconectado (Grafo Trivial ou Ponte Única).")
        else:
            output.append("Componentes biconectados (blocos):")
            for i, bloco in enumerate(blocos):
                bloco_str = [str(item) for item in bloco]
                output.append(f"Bloco {i+1} (Arestas): {bloco_str}")

    return "\n".join(output)

def formatar_busca_profundidade_classificacao(grafo):
    output = []
    if not grafo.vertices:
        return "\n".join(output + ["Vazio."])

    if grafo.direcionado:
        output.append("==== BUSCA EM PROFUNDIDADE ====")

        vertice_inicial = str(grafo.vertices[0].id)

        ordem_visita, arestas_arvore, arestas_retorno, arestas_avanco, arestas_cruzamento, pe_ids, ps_ids = busca_profundidade_com_classificacao(grafo, vertice_inicial)

        output.append(f"--- Resultado da Busca em Profundidade (DFS) a partir de '{vertice_inicial}' ---")

        # Classificação das Arestas
        output.append("Classificação das Arestas:")
        output.append(f"1. Arestas de Árvore ({len(arestas_arvore)}): {[str(a) for a in arestas_arvore]}")
        output.append(f"2. Arestas de Retorno ({len(arestas_retorno)}): {[str(a) for a in arestas_retorno]}")
        output.append(f"3. Arestas de Avanço ({len(arestas_avanco)}): {[str(a) for a in arestas_avanco]}")
        output.append(f"4. Arestas de Cruzamento ({len(arestas_cruzamento)}): {[str(a) for a in arestas_cruzamento]}")
        output.append("Resultados de PE e PS: ")
        output.append(f"PE: {pe_ids}")
        output.append(f"PS: {ps_ids}")
    return "\n".join(output)


def gerar_relatorio_completo(grafo: Grafo):
    """Gera um relatório completo e formatado com base no tipo de grafo."""
    header = [
        "*********************************************************************",
        f"Arquivo: {grafo.nome_arquivo}",
    ]

    if not grafo.direcionado:
        report_body = [
            "Análise para: GRAFO NÃO-DIRECIONADO",
            formatar_matriz_adj(grafo),
            formatar_lista_adj(grafo),
            formatar_conversoes(grafo),           
            formatar_graus(grafo),              
            formatar_adjacencias_por_vertice(grafo), 
            formatar_info_gerais(grafo),
            formatar_eh_conexo(grafo),            
            formatar_bipartido(grafo),            
            formatar_biconectividade(grafo),      
            "\nINFO: As buscas BFS (13) e DFS (14) são executadas e renderizadas visualmente."
        ]
    else:
        report_body = [
            "Análise para: DÍGRAFO",
            formatar_matriz_adj(grafo),
            formatar_lista_adj(grafo),
            formatar_graus(grafo),               
            formatar_adjacencias_por_vertice(grafo),
            formatar_grafo_subjacente(grafo),     
            "\nINFO: As buscas BFS (19) e DFS (20) são executadas e renderizadas visualmente."
        ]
    
    return "\n".join(header + report_body)